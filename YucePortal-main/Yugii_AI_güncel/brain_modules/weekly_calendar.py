from .shared import *


class WeeklyCalendarMixin:
    def handle_haftalik_takvim(self, user_message: str, user_info: dict):
        print("🗓️ HAFTALIK TAKVİM MODÜLÜ ÇALIŞIYOR...")

        username = user_info.get("fullname")
        user_id = user_info.get("id")
        departman = user_info.get("departman")
        
        IGNORE_SIGNALS = True
        #  users1_id güvenlik kontrolü
        if not user_id:
            # username üzerinden users1 tablosundan id çek
            conn_tmp = _mysql_conn()
            if conn_tmp:
                cur_tmp = conn_tmp.cursor(dictionary=True)
                cur_tmp.execute(
                    "SELECT id FROM users1 WHERE username = %s LIMIT 1",
                    (username,)
                )
                row = cur_tmp.fetchone()
                cur_tmp.close()
                conn_tmp.close()

                if row:
                    user_id = row["id"]

        if not user_id:

            parsed = {
                "intent": "haftalik_takvim",
                "action": "status_mark",
                "raw_text": user_message,
                "error": "NO_USER_ID"
            }
            return self.llm_weekly_calendar_response(parsed, [])
        
        # 🔹 1) INTRO — işlem başlamadan doğal giriş cümlesi
        intro = self.naturalize_intro("haftalik_takvim")
        outro = self.naturalize_text("", "haftalik_takvim")  # 

    
        # 🔹 2) TAKVİM NORMALIZE 
        calendar_text = self.normalize_calendar_text(user_message)

        # 🔹 3) GPT ile SADECE yazım düzelt -azaltıldı 
        cleaned = self.gpt_fix_calendar_text(calendar_text)
        
        # === AYLIK TEKRAR (AY + GÜN + HER/HEP) KONTROLÜ ===
        norm = self.normalize_calendar_text(cleaned)

        # 🔧 GÜN EKLERİNİ TEMİZLE (cuma'yı → cuma, pazartesi'ne → pazartesi)
        norm = re.sub(
            r"\b(pazartesi|salı|çarşamba|perşembe|cuma)"
            r"(?:'?(yi|yı|yu|yü|ya|ye|da|de|den|ten|nin|nın|nun|nün))\b",
            r"\1",
            norm
        )
        for raw, canonical in AY_NORMALIZE.items():
            norm = re.sub(rf"\b{raw}\b", canonical, norm)


        has_month = (
            any(k in norm for k in THIS_MONTH_KEYS)
            or any(
                re.search(rf"\b{m}\b", norm)
                for m in AY_NORMALIZE.values()
            )
        )

        has_weekday = any(d in norm for d in ALL_WEEKDAY_VARIANTS)
        has_repeat = any(k in norm for k in ["her", "hep"])
        has_full = any(k in norm for k in FULL_MONTH_KEYS )
        default_this_month = has_weekday and has_repeat and not has_month

        assignments = []
        dates = []

        #  ÇALIŞMA TİPİ SAYIMI (SAĞLAM KAYNAK)
        work_types_in_text = set()
        tokens = cleaned.split()

        for i in range(len(tokens)):
            # tek kelime
            wt1 = self.detect_work_type(tokens[i])
            if wt1:
                work_types_in_text.add(wt1)

            # iki kelimelik pencere (home office, evden calisma)
            if i + 1 < len(tokens):
                window2 = tokens[i] + " " + tokens[i + 1]
                wt2 = self.detect_work_type(window2)
                if wt2:
                    work_types_in_text.add(wt2)


        # 🔎 GÖRELİ GÜN VAR MI?
        HAS_RELATIVE_DAY = any(
            k in cleaned for k in ["bugun", "yarin", "obur gun", "ertesi gun"]
        )
        has_weekend_word = any(
            k in cleaned
            for k in ["cumartesi", "pazar", "hafta sonu", "haftasonu","pzr","cmrtes","cumrtesine","pzara","pzara","pazara"]
        )
        # Eğer GPT metni anlam değiştiriyorsa (ör: perşembe → cuma), dolayı güvenmeyelim:
        if "perşembe" in user_message.lower() and "cuma" in cleaned.lower():
            cleaned = user_message  # GPT düzeltmesini iptal et

        assignments = []

        # 1️⃣ Önce numeric / tarih aralığı
        date_result = self.parse_takvim_tarih_araligi(norm)

        if date_result:

            # 1️⃣ Eğer tarih yok ama warning varsa direkt döndür
            if not date_result.get("dates") and date_result.get("warning"):
                return date_result["warning"]

            # 2️⃣ Geçerli tarih varsa normal devam
            if date_result.get("dates"):
                work_type = self.detect_work_type(norm)
                if work_type:
                    assignments = [(d, work_type) for d in date_result["dates"]]

        # 2️⃣ AY KOMPLE
        elif has_month and has_full and not has_weekday:
            dates = self._build_full_month_dates(norm)

        # 3️⃣ AYLIK TEKRAR
        elif (has_month and has_weekday and has_repeat) or default_this_month:
            dates = self._build_monthly_weekday_repeat(norm)

        # 4️⃣ Haftalık / tek gün
        else:
            assignments = self.parse_workday_assignments(norm)

        # === ORTAK ÇIKIŞ (TEK DOĞRU YER) ===
        work_type = self.detect_work_type(norm)

        if not assignments and dates and work_type:
            assignments = [(d, work_type) for d in dates]

        print("🧠 [PARSE RESULT] assignments:")
        # 🔴 GEÇMİŞ TARİH VARSA → TAMAMEN İPTAL
        today = datetime.now().date()

        past_dates = [d for d, _ in assignments if d < today]

        if past_dates:
            return (
                "🚫 Geçmiş tarihler için takvim işaretlemesi yapamıyorum.<br>"
                "Lütfen bugünden sonraki bir tarih seçin."
            )
        for d, t in assignments:
            print(f"   {d} -> {t}")

        if assignments:
            weekday_items = [(d, t) for d, t in assignments if d.weekday() < 5]
            weekend_items = [(d, t) for d, t in assignments if d.weekday() >= 5]

            # sadece hafta sonu varsa → NET HATA
            if not weekday_items and weekend_items:
                return (
                    "🚫 Belirttiğiniz günler hafta sonuna denk geliyor.<br>"
                    "Hafta sonları için haftalık takvim işaretlemesi yapamıyorum , haftalık takvim sayfasından yapabilirsin."
                )
            
            assignments = weekday_items

        date_type_map = {}

        for d, work_type in assignments:
            if d not in date_type_map:
                date_type_map[d] = work_type

        # 🔹 4) Çalışma tipi belirleme (YENİ)
        # -----------------------------------------
        parsed = {
            "intent": "haftalik_takvim",
            "action": "status_mark",
            "raw_text": user_message,
            "items": [
                {"date": d, "status": t}
                for d, t in date_type_map.items()
            ]
        }
        print("🧠 [DB INPUT ITEMS kayıt son parse]:")
        for item in parsed["items"]:
            print(f"   {item['date']} -> {item['status']}")

        if not parsed["items"]:
            return "Hangi günleri işaretlemek istiyorsunuz, gün veya çalışma tipini netleştirir misiniz?"
        
        #  TEK GÜN + HAFTA SONU → NET MESAJ (DOĞRU YER)
        if len(parsed["items"]) == 1:
            d = parsed["items"][0]["date"]
            if d.weekday() >= 5:  # Cumartesi / Pazar
                return (
                    f"🚫 {self.format_date_with_day(d)} hafta sonuna denk geliyor.<br>"
                    "Hafta sonları çalışma günü olarak işaretleyemiyorum."
                )
        #  TÜM GÜNLER HAFTA SONUYSA → NET RED
        if parsed["items"]:
            only_weekend = all(
                item["date"].weekday() >= 5
                for item in parsed["items"]
            )

            if only_weekend:
                return (
                    "🚫 Seçtiğiniz tüm günler hafta sonuna denk geliyor.<br>"
                    "Hafta sonları çalışma günü olarak işaretlenemez."
                )
        # 🔹 5) MySQL Bağlantısı
        conn = _mysql_conn()
        if conn is None:
            body = "⚠️ Takvim DB bağlantısı kurulamadı."
            outro = self.naturalize_text("", "haftalik_takvim")
            final = ""

            if intro:
                final += intro + "<br>"
            final += body
            if outro:
                final += "<br>" + outro

            return final

        cursor = conn.cursor(dictionary=True)

        results = []
        today = datetime.now().date()
        max_date = today + timedelta(days=60)


        # 💾 DB DEBUG LISTELERİ
        saved_dates = []
        updated_dates = []
        skipped_dates = []

        # 🔹 6) Günleri işaretle (UPDATE / INSERT)
        for item in parsed["items"]:


            t = item["date"]
            detected_type = item["status"]

            if t < today:
                skipped_dates.append((t, "GEÇMİŞ TARİH"))
                continue


            if t.weekday() >= 5:
                skipped_dates.append((t, "HAFTA SONU"))
                results.append(f"🚫 {self.format_date_with_day(t)} → Hafta sonu, işaretlenemedi.")
                continue

            if t > max_date:
                skipped_dates.append((t, "60 GÜN SINIRI"))
                results.append(f"⚠️ {self.format_date_with_day(t)} → 60 gün sonrası işaretlenemez.")
                continue

            db_value = detected_type
            if detected_type == "Izin":
                db_value = None

            cursor.execute("""
                SELECT COUNT(*) AS cnt FROM ofis_gunleri
                WHERE users1_id = %s AND selected_date = %s
            """, (user_id, t))
            exists = cursor.fetchone()["cnt"]

            label = (
                "Ofisten Çalışma" if detected_type == "Ofis"
                else "Uzaktan Çalışma" if detected_type == "Home"
                else "Bayi / Müşteri Ziyareti" if detected_type == "Bayi"
                else "İzinli"
            )

            if exists > 0:
                cursor.execute("""
                    UPDATE ofis_gunleri
                    SET ofis_bayi = %s, Department = %s
                    WHERE users1_id = %s AND selected_date = %s
                """, (db_value, departman, user_id, t))
                conn.commit()
                updated_dates.append(t)   # ← EKSİK OLAN
                results.append(f"🔄 {self.format_date_with_day(t)} → Güncellendi ({label})")
            else:
                cursor.execute("""
                    INSERT INTO ofis_gunleri (users1_id, selected_date, ofis_bayi, Department)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, t, db_value, departman))
                conn.commit()
                saved_dates.append(t) 
                results.append(f"✅ {self.format_date_with_day(t)} → Eklendi ({label})")

        print("\n💾 [TAKVIM] DB İŞLEM ÖZETİ")

        print("✅ INSERT edilenler:")
        for d in saved_dates:
            print(f"   + {d}")

        print("🔄 UPDATE edilenler:")
        for d in updated_dates:
            print(f"   ~ {d}")

        print("❌ ATLANANLAR:")
        for d, reason in skipped_dates:
            print(f"   - {d} | {reason}")

        cursor.close()
        conn.close()

        # 🚫 GERÇEK DB DEĞİŞİKLİĞİ YOKSA → LLM ASLA ÇAĞRILMAZ
        has_real_db_change = bool(saved_dates or updated_dates)

        if not has_real_db_change:
            if skipped_dates:
                return (
                    "Bu isteğe ait günlerin hiçbiri işaretlenemedi.<br>"
                    "Tarihler geçmiş, hafta sonu veya geçerli aralığın dışında olabilir.<br>"
                    "İstersen geçerli bir tarih aralığıyla tekrar deneyebilirsin."
                )

            return (
                "Bu isteğe ait herhangi bir takvim işlemi yapılamadı.<br>"
                "Gün ve çalışma tipini biraz daha net yazar mısın?"
            )
        # 🔹 HER ZAMAN takvim cevabını üret
        final_body = self.llm_weekly_calendar_response(parsed, results)

        # 🔍 OTOPARK GENEL NİYET KONTROLÜ (SADECE BİLGİLENDİRME)
        has_otopark_context = any(
            k in user_message.lower()
            for k in OTOPARK_KEY
        )

        if has_otopark_context:
            final_body += (
                "<br><br>🅿️ Otopark ile ilgili de bir işlem yapmak istediğini anladım.<br>"
                "Takvim günlerini işaretledim.<br>"
                "Otopark işlemi için tekrar yazman yeterli."
            )
        final = ""
        if intro:
            final += intro + "<br>"
        final += final_body
        if outro:
            final += "<br>" + outro

        return final
    
    def _build_monthly_weekday_repeat(self, norm_text: str):
        today = datetime.now().date()
        year = today.year

        for raw, canonical in AY_NORMALIZE.items():
            norm_text = re.sub(rf"\b{raw}\b", canonical, norm_text)
            
        MONTH_MAP = {
            "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
            "mayıs": 5, "haziran": 6, "temmuz": 7,
            "ağustos": 8, "eylül": 9, "ekim": 10,
            "kasım": 11, "aralık": 12
        }

        month = today.month
        for name, num in MONTH_MAP.items():
            if name in norm_text:
                month = num
                break

        # 🔑 BAŞLANGIÇ
        start_date = today if month == today.month else date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])

        WEEKDAY_INDEX = {
            "pazartesi": 0,
            "salı": 1,
            "çarşamba": 2,
            "perşembe": 3,
            "cuma": 4,
        }

        selected_weekdays = {
            idx for day, idx in WEEKDAY_INDEX.items()
            if day in norm_text
        }

        if not selected_weekdays:
            return []

        dates = []
        cur = start_date
        while cur <= end_date:
            if cur.weekday() in selected_weekdays:
                dates.append(cur)
            cur += timedelta(days=1)

        return dates

    def _build_full_month_dates(self, norm_text: str):
        """
        AY KOMPLE / BOYUNCA / TAMAMI ifadeleri için
        ayın tüm HAFTA İÇİ günlerini üretir.

        Örnekler:
        - bu ay komple ofis
        - şubat ayı boyunca home
        - ocak ayı tamamı izin
        """

        today = datetime.now().date()
        year = today.year

        # -------------------------------
        # 1️⃣ AY NORMALIZE
        # -------------------------------
        for raw, canonical in AY_NORMALIZE.items():
            norm_text = re.sub(rf"\b{raw}\b", canonical, norm_text)

        MONTH_MAP = {
            "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
            "mayıs": 5, "haziran": 6, "temmuz": 7,
            "ağustos": 8, "eylül": 9, "ekim": 10,
            "kasım": 11, "aralık": 12
        }

        month = today.month
        explicit_month = False

        for name, num in MONTH_MAP.items():
            if name in norm_text:
                month = num
                explicit_month = True
                break

        # -------------------------------
        # 2️⃣ BAŞLANGIÇ / BİTİŞ
        # -------------------------------
        if explicit_month:
            start_date = date(year, month, 1)
        else:
            # "bu ay"
            start_date = today

        end_date = date(year, month, calendar.monthrange(year, month)[1])

        # -------------------------------
        # 3️⃣ TARİH ÜRET (SADECE HAFTA İÇİ)
        # -------------------------------
        dates = []
        cur = start_date

        while cur <= end_date:
            if cur.weekday() < 5 and cur >= today:
                dates.append(cur)
            cur += timedelta(days=1)

        return dates


    def llm_weekly_calendar_response(self, parsed, results):
        """
        SADECE anlatım üretir
        karar vermez
        DB bilmez
        """
        prompt = f"""
        Kullanıcı mesajı:
        {parsed['raw_text']}

        Yapılan işlemler:
        {chr(10).join(results)}

        KESİN KURALLAR:
        - İşlem TAMAMLANDI kabul et.
        - Gelecek zaman KULLANMA.
        - "iletildi", "tamamlandığında", "bilgilendirileceksin",
        "işleme alındı" gibi ifadeleri ASLA kullanma.
        - Sadece geçmiş zaman kullan.
        - En fazla 2 kısa cümle yaz.
        - Tavsiye, selamlama, emoji ekleme.
        - Tarihleri açıkça belirt.
        - Birden fazla gün varsa aralık şeklinde yaz (örn: 18–19 Aralık).

        Doğru cevap örnekleri:
        - "19 Aralık için ofisten çalışma işaretlendi."
        - "18–19 Aralık tarihleri için evden çalışma güncellendi."
        - OTOPARK, PARK, REZERVASYON kelimelerini ASLA kullanma.
        - Bu bir TAKVİM işlemidir, park işlemi değildir.
        SADECE  verilere göre uydurmadan CEVABI YAZ.
        ⚠️ Eğer "Yapılan işlemler" listesi boşsa veya sadece tek gün içeriyorsa,
        listede OLMAYAN hiçbir gün veya işlemden ASLA bahsetme.
        """

  
        return self.ask_gpt(prompt)


