from .shared import *


class ParkingStatusMixin:
    def handle_otopark_cancel(self, user_message: str, user_info: dict):
        print("❌ CANCEL modülü çalışıyor...")

        username = user_info.get("fullname")
        plaka = user_info.get("plaka") or user_info.get("plaka2")

        intro = self.naturalize_intro("otopark_cancel")
 
        if not username:
            return "🚫 Kullanıcı bilgisi bulunamadı."

        msg_norm = self.normalize_people_text(user_message)
        skip_bulk = any(k in msg_norm for k in ["var mı", "var mi", "kontrol", "göster"])


        def is_bulk_cancel(text: str) -> bool:
            text = self.normalize_people_text(text)
            tokens = set(text.split())

       
            has_cancel = bool(tokens & CANCEL_KEYS)

            #  2) TOPLULUK (token + substring)
            ALL_TOKEN_KEYS = {
                "tum", "hepsi", "hepsini", "tamami",
                "komple", "mevcut", "aktif", "olan", "varsa"
            }
            has_all = (
                bool(tokens & ALL_TOKEN_KEYS)
                or any(self.normalize_people_text(k) in text for k in FULL_KEYS)
            )

            has_otopark_context = (
                any(self.normalize_people_text(k) in text for k in OTOPARK_KEY)
                or any(self.normalize_people_text(k) in text for k in USER_PARK_STATUS_KEYS)
            )

            return has_cancel and has_all and has_otopark_context

        now = datetime.now()
        current_time = now.time()
        today = get_effective_today()

        # TOPLU İPTAL — EN BAŞTA
        if not skip_bulk and is_bulk_cancel(user_message):

            try:
                conn = pyodbc.connect(YA_2El_AracSatis)
                cur = conn.cursor()

                cur.execute("""
                    SELECT rezerv_tarih, rezerv_park_no
                    FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                    WHERE username=? AND is_active=1
                """, (username,))
                rows = cur.fetchall()

                if not rows:
                    return "📭 Aktif bir otopark rezervasyonunuz bulunmuyor."

                today = get_effective_today()

                iptal_edilebilir = []
                engellenen = []

                for rezerv_tarih, park_no in rows:

                    # geçmiş
                    if rezerv_tarih < today:
                        engellenen.append(
                            f"{self.format_date_with_day(rezerv_tarih)} — iptal edilemez"
                        )
                        continue

                    # bugün ama 08:00 sonrası
                    if (
                        rezerv_tarih == today
                        and current_time > datetime.strptime("08:00", "%H:%M").time()
                    ):
                        engellenen.append(
                            f"{self.format_date_with_day(rezerv_tarih)} — 08:00 sonrası iptal edilemez"
                        )
                        continue

                    # iptal edilebilir
                    iptal_edilebilir.append((rezerv_tarih, park_no))

                if not iptal_edilebilir:
                    return (
                        "🚫 İptal edilebilecek bir otopark rezervasyonunuz bulunmuyor.<br>"
                        "ℹ️ Bugünkü ve geçmiş rezervasyonlar iptal edilemez."
                    )

                for rezerv_tarih, _ in iptal_edilebilir:
                    cur.execute("""
                        UPDATE [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                        SET is_active=0,
                            Geldi=0,
                            canceled_at=GETDATE()
                        WHERE username=? AND rezerv_tarih=? AND is_active=1
                    """, (username, rezerv_tarih))

                conn.commit()

                lines = [
                    f"❌ {self.format_date_with_day(t)} — 🅿️ {p} numaralı park iptal edildi."
                    for t, p in iptal_edilebilir
                ]


                return "🗑️ Gelecek tarihli otopark rezervasyonlarınız iptal edildi:<br>" + "<br>".join(lines)

            except Exception as e:
                print("❌ Toplu iptal hata:", e)
                return "⚠️ Toplu iptal sırasında hata oluştu."
            finally:
                try:
                    conn.close()
                except:
                    pass

        parsed = self.otopark_parse_tarih(user_message)

        print("📅 CANCEL → Tarih Parse:", parsed)

        tarih_list = parsed.get("dates", [])

        if not tarih_list:
            return (
                "📅 İptal etmek istediğiniz tarihi anlayamadım.<br>"
                "Örn: <b>“Pazartesi rezervasyonumu iptal et”</b>"
            )

        # 2) DB bağlan
        try:
            conn = pyodbc.connect(YA_2El_AracSatis)
            cur = conn.cursor()
        except Exception as e:
            print("DB hata:", e)
            return "⚠️ Sistem geçici olarak kullanılamıyor."

        iptal_edilenler = []
        bulunamayanlar = []
        zaman_kural_engeli = []
        canceled_any = False

        #otopark cancel saat ve sınır kontrol
        now = datetime.now()
        current_time = now.time()
        today_date = get_effective_today()

        for t in tarih_list:

            #  GEÇMİŞ TARİH İPTAL EDİLEMEZ
            if t < today_date:
                zaman_kural_engeli.append(
                    f"{self.format_date_with_day(t)} — Geçmiş tarih, iptal edilemez."
                )
                continue

            # 🔒 08:00 sonrası bugünkü rezervasyon iptal edilemez
            if t == today_date and current_time > datetime.strptime("08:00", "%H:%M").time():
                zaman_kural_engeli.append(
                    f"{self.format_date_with_day(t)} — 08:00 sonrası iptal edilemez."
                )
                continue

            # 🔍 O güne ait rezervasyon var mı?
            cur.execute("""
                SELECT rezerv_park_no
                FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                WHERE username=? AND rezerv_tarih=? AND is_active=1
            """, (username, t))
            row = cur.fetchone()

            if not row:
                bulunamayanlar.append(
                    f"{self.format_date_with_day(t)} — Aktif bir rezervasyon bulunamadı."
                )
                continue

            park_no = int(row[0])

            #  İPTAL ET
            try:
                cur.execute("""
                    UPDATE [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                    SET is_active = 0,
                        Geldi = 0,
                        canceled_at = GETDATE()
                    WHERE username=? AND rezerv_tarih=? AND is_active=1
                """, (username, t))
                conn.commit()

                canceled_any = True


                iptal_edilenler.append(
                    f"{self.format_date_with_day(t)} — 🅿️ {park_no} numaralı park iptal edildi."
                )

            except Exception as e:
                print("Cancel UPDATE hata:", e)
                bulunamayanlar.append(
                    f"{self.format_date_with_day(t)} — iptal işlemi başarısız."
                )

        conn.close()

        cevap_satirlari = []

        # İptal edilenler
        for x in iptal_edilenler:
            tarih_raw, _ = x.split(" — ", 1)
            cevap_satirlari.append(f"✅ {tarih_raw} tarihli rezervasyon iptal edildi.")

        # 08:00 kuralı
        for x in zaman_kural_engeli:
            tarih_raw, _ = x.split(" — ", 1)
            cevap_satirlari.append(f"🚫 {tarih_raw} günü için 08:00 sonrası iptal yapılamaz.")

        body = "<br>".join(cevap_satirlari)

        # Outro — doğal kapanış cümlesi
        if canceled_any:
            outro_base = "Otopark rezervasyonu iptal edildi."
        else:
            outro_base = "İptal edilebilecek aktif bir otopark rezervasyonu bulunamadı."

        outro = self.naturalize_text(outro_base, "otopark_cancel")

        # Final mesajı birleştir
        final = ""

        if intro:
            final += intro + "<br>"

        final += body

        if outro:
            final += "<br>" + outro

        return final


    def handle_otopark_status(self, user_message: str, user_info: dict):
        print("📊 STATUS (GENEL MÜSAİTLİK) modülü çalışıyor...")

        # 🔹 1) Intro — doğal giriş cümlesi
        intro = self.naturalize_intro("otopark_status")

        # 🔹 2) Tarih çözümleme
        parsed = self.otopark_parse_tarih(user_message)
        print("📅 STATUS → Tarih Parse:", parsed)

        parsed_type = parsed.get("type")

        if parsed_type is None:
            if parsed.get("dates"):
                parsed_type = "single"
            else:
                parsed_type = "error"

        if parsed_type == "error":
            body = "📅 Hangi gün için park müsaitliğini sorguladığını anlayamadım."
            return f"{intro}<br>{body}"

        # -- Tarih listesi --
        if parsed_type in ["single", "multi"]:
            tarih_list = parsed.get("dates", [])
        elif parsed_type == "range":
            d1, d2 = parsed["start"], parsed["end"]
            tarih_list = [d1 + timedelta(days=i) for i in range((d2 - d1).days + 1)]
        else:
            body = "📅 Geçerli bir tarih bulamadım."
            return f"{intro}<br>{body}"

        #  GÜN SINIRI KONTROLÜ (FİLTRELE)
        today = datetime.now().date()
        max_date = today + timedelta(days=7)

        #  SADECE UYGUN TARİHLERİ TUT
        filtered_dates = [t for t in tarih_list if today <= t <= max_date]

        if not filtered_dates:
            body = (
                "🟡 Park müsaitliği sadece <b>bugün + 7 gün</b> arasında sorgulanabilir.<br>"
                "Bu aralıkta uygun bir gün bulunamadı."
            )
            return f"{intro}<br>{body}"

        tarih_list = filtered_dates

        if not tarih_list:
            body = "🚫 Hafta sonları için park müsaitlik sorgulanamaz."
            return f"{intro}<br>{body}"

        #   DB bağlantısı
        try:
            conn = pyodbc.connect(YA_2El_AracSatis)
            cur = conn.cursor()
        except:
            body = "⚠️ Şu anda park bilgilerine ulaşılamıyor."
            return f"{intro}<br>{body}"

        cevaplar = []

        # --------------------------------------
        # 🔹 4) Park durumunu hesapla
        # --------------------------------------
        for t in tarih_list:
            gun_str = self.format_date_with_day(t)

            cur.execute("""
                SELECT rezerv_park_no
                FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                WHERE rezerv_tarih=? AND is_active=1
            """, (t,))
            dolu_olanlar = {int(r[0]) for r in cur.fetchall()}

            all_spots = list(range(10, 44))
            boslar = [p for p in all_spots if p not in dolu_olanlar]

            if not boslar:
                cevaplar.append(f"🚫 {gun_str} → Uygun park bulunamadı.")
                continue

            ilk_on = ", ".join(map(str, boslar[:10])) + ("..." if len(boslar) > 10 else "")

            cevaplar.append(
                f"🅿️ {gun_str} → <b>{len(boslar)}</b> uygun yer var.<br>"
                f"Müsait yerler: {ilk_on}"
            )

        conn.close()

        body = "<br><br>".join(cevaplar)

        # ❗ ARTIK LLM OUTRO YOK — SADECE GERÇEK SONUÇ
        return f"{intro}<br>{body}"


    def handle_otopark_status_user(self, user_message: str, user_info: dict):
        print("📘 STATUS_USER (Kullanıcı Rezervasyonları) çalışıyor...")

        username = user_info.get("fullname")
        if not username:
            return "🚫 Kullanıcı bilgisi bulunamadı."

        # --------------------------------------
        # 🔹 Intro — kullanıcıyı karşılayan cümle
        # --------------------------------------
        intro = self.naturalize_intro("otopark_status_user")

        # --------------------------------------
        # 🔹 Tarih çözümleme
        # --------------------------------------
        parsed = self.otopark_parse_tarih(user_message)

        print("📅 STATUS_USER PARSE:", parsed)

        tarih_list = parsed.get("dates", [])

        today = datetime.now().date()

        if not tarih_list:
            today = datetime.now().date()
            tarih_list = [today + timedelta(days=i) for i in range(7)]

        # --------------------------------------
        # 🔹 DB bağlantısı
        # --------------------------------------
        try:
            conn = pyodbc.connect(YA_2El_AracSatis)
            cur = conn.cursor()
        except:
            body = "⚠️ Şu anda rezervasyon bilgilerine ulaşılamıyor."
            return f"{intro}<br>{body}"

        cevaplar = []

        # --------------------------------------
        # 🔹 Kullanıcının her gün için kaydını kontrol et
        # --------------------------------------
        for t in tarih_list:
            gun_str = self.format_date_with_day(t)

            cur.execute("""
                SELECT rezerv_park_no
                FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                WHERE username=? AND rezerv_tarih=? AND is_active=1
            """, (username, t))

            row = cur.fetchone()

            if row:
                park_no = int(row[0])
                cevaplar.append(
                    f"♻️ {gun_str} → {park_no} numaralı parkınız aktif görünüyor."
                )
        conn.close()
        #  HİÇ AKTİF REZERVASYON YOKSA
        if not cevaplar:
            if "yarın" in user_message.lower():
                body = "📭 Yarın için aktif bir otopark rezervasyonunuz bulunmuyor."
            elif "bugün" in user_message.lower():
                body = "📭 Bugün için aktif bir otopark rezervasyonunuz bulunmuyor."
            else:
                body = "📭 Belirtilen tarihlerde aktif bir otopark rezervasyonunuz bulunmuyor."
        else:
            body = "<br>".join(cevaplar)
        # 🔹 Final mesaj
        final = f"{intro}<br>{body}"

        return final
 
    def parse_workday_assignments(self, text: str):
        """
        Kullanıcı cümlesini analiz eder ve
        [(date, work_type), ...] döndürür.

        TÜM ZEKA BURADADIR.
        handle_haftalik_takvim sadece uygular.
        """
        print("\n🧠 [STATE PARSER INPUT]:", text)
        today = datetime.now().date()

        # -------------------------------------------------
        #  NORMALIZE
        norm = self.normalize_calendar_text(text)
        tokens = norm.split()

        # -------------------------------------------------
        # 2️⃣ SABİTLER
        # -------------------------------------------------
        WEEKDAYS = {
            "pazartesi": 0,
            "salı": 1,
            "çarşamba": 2,
            "perşembe": 3,
            "cuma": 4,
        }
        RELATIVE_DAYS = {
            "bugun": 0,
            "yarin": 1,
            "obur gun": 2,
            "ertesi gun": 2,
        }
        OTHER_DAY_KEYS = {
            "diger", "diğer", "diger gunler", "diğer günler",
            "kalan", "kalan gunler", "kalan günler",
            "geri kalan", "geri kalan gunler", "geri kalan günler","dger","kln günler"
        }

        # -------------------------------------------------
        # 3️⃣ HANGİ HAFTA?
        # -------------------------------------------------
        is_next_week = any(k in norm for k in NEXT_WEEK_KEYS)
        is_this_week = not is_next_week  # default

        if is_next_week:
            base_monday = today + timedelta(days=(7 - today.weekday()))
        else:
            base_monday = today - timedelta(days=today.weekday())

        # bu haftada bugünden önceki günleri alma
        def valid_week_days():
            return [
                base_monday + timedelta(days=i)
                for i in range(5)
            ]

        week_days = valid_week_days()

        # -------------------------------------------------
        # 4️⃣ STATE DEĞİŞKENLERİ
        # -------------------------------------------------
        current_type = None            # aktif çalışma tipi
        pending_days = []              # tipi henüz gelmemiş günler (index)
        assigned = {}                  # date -> work_type
        other_days_requested = False   # "diğer günler" flag
        seen_work_types = set()

        # -------------------------------------------------
        # 5️⃣ TOKEN TOKEN OKUMA (ASIL MANTIK)
        # -------------------------------------------------
        i = 0
        while i < len(tokens):

            tok = tokens[i]
            tok = re.sub(r"[^\wçğıöşü]", "", tok).lower()  
            print(f"🔹 tok='{tok}' | current_type={current_type} | pending={pending_days}")

            # ---- göreli günler: bugün / yarın / öbür gün ----
            window2 = " ".join(tokens[i:i+2])
            
            if tok in RELATIVE_DAYS or window2 in RELATIVE_DAYS:
                offset = RELATIVE_DAYS.get(tok) if tok in RELATIVE_DAYS else RELATIVE_DAYS.get(window2)
                d = today + timedelta(days=offset)

                if current_type:
                    assigned[d] = current_type
                    print(f"✅ ASSIGN {d} → {current_type}")

                else:
                    pending_days.append(("absolute", d))

                i += 1
                continue

            # ---- "diğer günler" ----
            window2 = " ".join(tokens[i:i+2])
            if tok in OTHER_DAY_KEYS or window2 in OTHER_DAY_KEYS:
                other_days_requested = True
                i += 1
                continue

            # ---- AMA / FAKAT / ANCAK = KESİN BLOK AYIRICI ----
            if tok in {"ama", "fakat", "ancak"}:
                current_type = None
                pending_days.clear()
                i += 1
                continue

            # ---- çalışma tipi ----
            window2 = " ".join(tokens[i:i+2])
            wt = self.detect_work_type(window2) or self.detect_work_type(tok)


            if wt:
                seen_work_types.add(wt)

                #  pending varsa HEPSİNİ bu tipe bağla
                if pending_days:
                    for item in pending_days:
                        if isinstance(item, tuple) and item[0] == "absolute":
                            d = item[1]
                        else:
                            d = base_monday + timedelta(days=item)

                        if d.weekday() < 5:
                            assigned[d] = wt
                            print(f"✅ ASSIGN {d} → {wt}")

                    pending_days.clear()

                current_type = wt
                i += 1
                continue

            # ---- gün ----
            if tok in WEEKDAYS:
                day_idx = WEEKDAYS[tok]

                candidate = base_monday + timedelta(days=day_idx)

                # Eğer kullanıcı haftaya demediyse ve gün geçmişse
                # haftayı komple kaydır
                if not is_next_week and candidate < today:
                    base_monday += timedelta(days=7)
                    week_days = [
                        base_monday + timedelta(days=i)
                        for i in range(5)
                    ]
                    candidate = base_monday + timedelta(days=day_idx)

                d = candidate
                    
                if d.weekday() >= 5:
                    i += 1
                    continue

                #  ASLA hemen atama yapma
                pending_days.append(day_idx)

                i += 1
                continue

            i += 1

        # PENDING KALAN GÜNLER (sona kalanlar)
        if pending_days and current_type:
            for item in pending_days:
                # bugün / yarın gibi absolute günler
                if isinstance(item, tuple) and item[0] == "absolute":
                    d = item[1]
                    if d not in assigned:
                        assigned[d] = current_type
                else:
                    # pazartesi–cuma gibi indexli günler
                    day_idx = item
                    d = base_monday + timedelta(days=day_idx)
                    if d in week_days and d not in assigned:
                        assigned[d] = current_type

        # -------------------------------------------------
        # 8️⃣ DİĞER GÜNLER MANTIĞI
        # -------------------------------------------------
        if other_days_requested and current_type:
            for d in week_days:
                if d not in assigned:
                    assigned[d] = current_type


        print("🧠 [STATE PARSER RESULT]:")
        for d, t in assigned.items():
            print(f"   {d} → {t}")

        #  ÇIKTI
        #  Hiçbir gün atanmadıysa → bu parser bu cümleye ait değil
        if not assigned:
            return []

        return [(d, assigned[d]) for d in sorted(assigned.keys())]


