from .shared import *


class CalendarParserMixin:
    def parse_takvim_tarih_araligi(self, message: str):
        """
        Haftalık takvim için doğal dilde geçen 'bu hafta', 'haftaya', 'hafta içi', 'hafta sonu',
        'bu haftayı full işaretle', 'haftaya hafta sonu' vb. ifadeleri tarih listesine çevirir.
        Geçmiş günleri atlar, gerekiyorsa uyarı mesajı döndürür.
        """
        print("🔍 [DEBUG] parse_takvim_tarih_araligi() ÇALIŞTI → Mesaj:", message)

        msg_lower = (message or "").lower().strip()
        today = datetime.now().date()
        year = today.year
        #  HER ZAMAN VAR olmalı
        found_days = []

        MONTHS = {
            "ocak":1,"şubat":2,"mart":3,"nisan":4,"mayıs":5,
            "haziran":6,"temmuz":7,"ağustos":8,
            "eylül":9,"ekim":10,"kasım":11,"aralık":12
        }
        # 🔹 Bugün / Yarın ifadeleri
        if re.search(r"\bbug[uü]n(e|ü|u|un|ün)?\b", msg_lower):
            return {"dates": [today], "warning": None}

        if re.search(r"\byar[iı]n(a|e|ı|i|un|ün)?\b", msg_lower):
            yarin = today + timedelta(days=1)
            if yarin.weekday() < 5:
                return {"dates": [yarin], "warning": None}
            else:
                return {"dates": [], "warning": "🚫 Yarın hafta sonu, işaretlenmedi."}
    
        #  EN ÖNCELİKLİ: HAFTAYA BUGÜN (SADECE TEK GÜN İSE)
        if any(k in msg_lower for k in [
            "haftaya bugün",
            "haftaya bugun",
            "haftaya bugünü",
            "haftaya bugunu","haftya bugn","haftaya bgn","önümüzdeki hafta bugün","önüzümüzde ki hafta bugün","haftaya bu gün","ileriki hafta bugün","gelecek hafta bu gün","gelecek hafta bugün"
        ]):
            # başka gün var mı?
            other_days = found_days.copy()

            # "bugün" canonical bir gün değil, onu hariç tut
            # found_days sadece pazartesi-salı vb. içerir
            if not other_days:
                t = today + timedelta(days=7)
                if t.weekday() >= 5:
                    return {
                        "dates": [],
                        "warning": "🚫 Haftaya bugün hafta sonuna denk geliyor."
                    }
                return {"dates": [t], "warning": None}
            
        VARIANT_TO_CANONICAL_DAY = {}

        for d in PAZARTESI_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "pazartesi"
        for d in SALI_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "salı"
        for d in CARSAMBA_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "çarşamba"
        for d in PERSEMBE_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "perşembe"
        for d in CUMA_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "cuma"
        for d in CUMARTESI_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "cumartesi"
        for d in PAZAR_VARIANTS:
            VARIANT_TO_CANONICAL_DAY[d] = "pazar"

        CANONICAL_DAY_TO_INDEX = {
            "pazartesi": 0,
            "salı": 1,
            "çarşamba": 2,
            "perşembe": 3,
            "cuma": 4,
            "cumartesi": 5,
            "pazar": 6,
        }


        for day in ALL_WEEKDAY_VARIANTS:
            if day in msg_lower:
                canonical = VARIANT_TO_CANONICAL_DAY.get(day)
                if canonical:
                    found_days.append(canonical)

        # tekrarları temizle
        found_days = list(dict.fromkeys(found_days))

            
        has_context = any(
            k in msg_lower
            for k in (BU_WEEK_DAY_PREFIXES + NEXT_WEEK_KEYS + THIS_MONTH_KEYS)
        )
        if found_days and not has_context:

            monday = today - timedelta(days=today.weekday())
            tarih_listesi = []

            for g in found_days:
                idx = CANONICAL_DAY_TO_INDEX.get(g)
                if idx is None:
                    continue

                t = monday + timedelta(days=idx)

                # bu hafta geçtiyse → haftaya kaydır
                if t < today:
                    t += timedelta(days=7)

                if t.weekday() < 5:
                    tarih_listesi.append(t)

            return {"dates": tarih_listesi, "warning": None}
        
        
        #  AY VAR AMA GÜN YOKSA → AYIN TÜM İŞ GÜNLERİ
        found_months = [
            ay for ay in MONTHS
            if re.search(rf"\b{ay}\b", msg_lower)
        ]

        has_day_info = bool(found_days) or bool(re.search(r"\d{1,2}", msg_lower))


        if found_months and not has_day_info:
            dates = []
            year_match = re.search(r"\b(20\d{2})\b", msg_lower)
            yil = int(year_match.group(1)) if year_match else today.year

            for ay in found_months:
                ay_num = MONTHS[ay]

                # aynı ay ise bugünden başla
                if yil == today.year and ay_num == today.month:
                    start_date = today
                else:
                    start_date = date(yil, ay_num, 1)

                end_date = date(
                    yil,
                    ay_num,
                    calendar.monthrange(yil, ay_num)[1]
                )

                cur = start_date
                while cur <= end_date:
                    if cur.weekday() < 5:  # sadece hafta içi
                        dates.append(cur)
                    cur += timedelta(days=1)

            return {"dates": sorted(set(dates)), "warning": None}

        for ay_adi, ay_num in MONTHS.items():

            if ay_adi in msg_lower and any(k in msg_lower for k in FULL_MONTH_KEYS):

                # yıl
                year_match = re.search(r"\b(20\d{2})\b", msg_lower)
                yil = int(year_match.group(1)) if year_match else year

                # başlangıç
                if yil == today.year and ay_num == today.month:
                    start_date = today
                else:
                    start_date = datetime(yil, ay_num, 1).date()

                # bitiş
                end_date = datetime(
                    yil,
                    ay_num,
                    calendar.monthrange(yil, ay_num)[1]
                ).date()

                dates = []
                cur = start_date
                while cur <= end_date:
                    if cur.weekday() < 5:   # hafta sonu yok
                        dates.append(cur)
                    cur += timedelta(days=1)

                print(f"📅 AY FULL ALGILANDI → {ay_adi} {yil}")
                return {"dates": dates, "warning": None}
            
        # BİRDEN FAZLA AY + TAMAMI / FULL / KOMPLE 
        ay_full_triggers = ["full", "komple", "tamami", "tamamı", "tümü", "hepsi", "ful", "boyunca"]

        all_dates = []
        matched_any_month = False

        # YIL TESPİTİ (tek kez)
        year_match = re.search(r"\b(20\d{2})\b", msg_lower)
        yil = int(year_match.group(1)) if year_match else year

        for ay_adi, ay_num in MONTHS.items():
            if ay_adi in msg_lower and any(k in msg_lower for k in ay_full_triggers):
                matched_any_month = True

                #  AY BAŞLANGICI
                if yil == today.year and ay_num == today.month:
                    start_date = today
                else:
                    start_date = datetime(yil, ay_num, 1).date()

                #  AY SONU
                end_date = datetime(
                    yil,
                    ay_num,
                    calendar.monthrange(yil, ay_num)[1]
                ).date()

                cur = start_date
                while cur <= end_date:
                    if cur.weekday() < 5:  # 🚫 hafta sonu yok
                        all_dates.append(cur)
                    cur += timedelta(days=1)

                print(f"📅 AY FULL ALGILANDI → {ay_adi} {yil}")

        #  EN SONDA TEK RETURN
        if matched_any_month:
            all_dates = sorted(set(all_dates))  # duplicate temizle
            return {"dates": all_dates, "warning": None}

        # 🔹 "5 ekim ve 10 ekim" gibi, sadece iki farklı günü ifade eden durumları yakala
        if (" ve " in msg_lower or "," in msg_lower) and not any(x in msg_lower for x in ["arası", "arasında", "kadar", "ile", "–", "-"]):
            match_coklu = re.findall(
                r"(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)?",
                msg_lower
            )
            if match_coklu and len(match_coklu) >= 2:
                tarih_listesi = []
                gecmis_tarihler = []
                for gun, ay in match_coklu:
                    try:
                        gun = int(gun)
                        ay_num = MONTHS.get(ay, today.month)
                        yil = year
                        tarih = datetime(yil, ay_num, gun).date()
                        if tarih.weekday() < 5:  # sadece hafta içi
                            if tarih < today:
                                gecmis_tarihler.append(tarih)
                            else:
                                tarih_listesi.append(tarih)
                    except Exception as e:
                        print(f"⚠️ Çoklu tarih çözüm hatası: {e}")
                        continue

                # 🎯 Kullanıcıya hem geçmiş hem güncel tarihleri bildir
                if gecmis_tarihler or tarih_listesi:
                    lines = []
                    for t in tarih_listesi:
                        lines.append(f"✅ {t.strftime('%d.%m.%Y (%a)')} → Güncellendi.")
                    warning_text = "📅 Takvim işlemi tamamlandı:<br>" + "<br>".join(lines)
                    print(warning_text)
                    return {"dates": tarih_listesi, "warning": warning_text}


        # 🔹 "5 kasım 11 kasım 15 kasım" gibi birden fazla ay adı içeren tarihleri yakala
        if not any(x in msg_lower for x in ["arası", "arasında", "kadar", "ile", "–", "-"]):
            # Tüm sayı + ay çiftlerini sırayla yakala
            month_pattern = "|".join(MONTHS.keys())
            match_multi_ay = re.findall(
                rf"(\d{{1,2}})\s+({month_pattern})",
                msg_lower
            )

            if len(match_multi_ay) >=2:
                tarih_listesi = []
                gecmis_tarihler = []
                for gun, ay in match_multi_ay:
                    try:
                        gun = int(gun)
                        ay_num = MONTHS[ay]
                        yil = year
                        tarih = datetime(yil, ay_num, gun).date()
                        if tarih.weekday() < 5:
                            if tarih < today:
                                gecmis_tarihler.append(tarih)
                            else:
                                tarih_listesi.append(tarih)
                    except Exception as e:
                        print(f"⚠️ Çoklu ay çözüm hatası: {e}")
                        continue

                if tarih_listesi:
                    lines = [f"✅ {t.strftime('%d.%m.%Y (%a)')} → Güncellendi." for t in tarih_listesi]
                    warning_text = "📅 Takvim işlemi tamamlandı:<br>" + "<br>".join(lines)
                    return {"dates": tarih_listesi, "warning": warning_text}

                if gecmis_tarihler and not tarih_listesi:
                    return {
                        "dates": [],
                        "warning": "🚫 Belirttiğiniz tarihler geçmişte, işaretlenemez."
                    }

        # ===============================================================
        # 🧩 TÜRKÇE TAM DESTEKLİ TARİH ARALIĞI ALGILAMA (örnek: 5 kasımdan 15 kasıma kadar)
        # ===============================================================
        match_aralik_yeni = re.search(
            r"(?P<g1>\d{1,2})"                                # ilk gün (ör: 5)
            r"\s*[,\.']*\s*"                                   # olası ayırıcılar (, . veya ')
            r"(?P<ay1>ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)?"  # ilk ay (opsiyonel)
            r"(?:['’]?(?:dan|den|tan|ten|a|e|ya|ye|ın|in|un|ün))?"  # Türkçe ekler (ör: kasımdan, kasıma)
            r"\s*(?:-|–|,|ile|ve|’|’dan|’den|’a|’e|’ya|’ye|’dan|’den|’tan|’ten|\s)+\s*"  # bağlaçlar veya tire
            r"(?P<g2>\d{1,2})"                                # ikinci gün (ör: 15)
            r"\s*[,\.']*\s*"                                   # ayırıcılar
            r"(?P<ay2>ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)?"  # ikinci ay (opsiyonel)
            r"(?:['’]?(?:a|e|ya|ye|dan|den|tan|ten|kadar|arası|arasında)?)?",            # ikinci kelime ekleri
            msg_lower,
            flags=re.IGNORECASE  # büyük/küçük harf duyarsız
        )


        if match_aralik_yeni:
            try:
                g1 = int(match_aralik_yeni.group("g1"))
                g2 = int(match_aralik_yeni.group("g2"))
                ay1 = match_aralik_yeni.group("ay1") or match_aralik_yeni.group("ay2") or None
                month = MONTHS.get(ay1, today.month)
                start_date = datetime(year, month, g1).date()
                end_date = datetime(year, month, g2).date()

                if end_date < start_date:
                    end_date = start_date  # yanlış sıra yazılmışsa düzelt

                tarih_listesi = []
                for d in range((end_date - start_date).days + 1):
                    t = start_date + timedelta(days=d)
                    if t.weekday() < 5:
                        tarih_listesi.append(t)

                # 🔹 Geçmiş / Gelecek / Limit Kontrolü (iyileştirilmiş versiyon)
                valid_dates = []
                message_lines = []
                max_end = today + timedelta(days=30)

                for t in tarih_listesi:
                    if t < today:
                        message_lines.append(f"❌ {t.strftime('%d.%m.%Y (%A)')} → Geçmiş tarih, işaretlenemedi.")
                        continue
                    if t > max_end:
                        message_lines.append(f"⚠️ {t.strftime('%d.%m.%Y (%A)')} → 30 gün sınırını aşıyor, eklenmedi.")
                        continue
                    if t.weekday() >= 5:
                        message_lines.append(f"🚫 {t.strftime('%d.%m.%Y (%A)')} → Hafta sonu, eklenmedi.")
                        continue

                    valid_dates.append(t)
                    message_lines.append(f"✅ {t.strftime('%d.%m.%Y (%A)')} → Güncellendi.")

                # 🔸 Hiç geçerli tarih yoksa tamamen iptal
                if not valid_dates:
                    warning_text = "📅 Takvim işlemi tamamlanamadı:<br>" + "<br>".join(message_lines)
                    print(warning_text)
                    return {"dates": [], "warning": warning_text}

                # 🔸 Hem geçmiş hem geçerli tarih varsa (kısmi başarı)
                if len(valid_dates) < len(tarih_listesi):
                    warning_text = "📅 Takvim işlemi kısmen tamamlandı:<br>" + "<br>".join(message_lines)
                else:
                    warning_text = "📅 Takvim işlemi tamamlandı:<br>" + "<br>".join(message_lines)

                print(warning_text)
                return {"dates": valid_dates, "warning": None}


            except Exception as e:
                print(f"⚠️ Yeni aralık çözüm hatası: {e}")


        #  HAFTAYA + SAYI (haftaya 5 gün, ilk 3 gün vb.)
        count = self._detect_weekday_count_scope(msg_lower)

        if count and any(k in msg_lower for k in NEXT_WEEK_KEYS):
            next_monday = today + timedelta(days=(7 - today.weekday()))

            # maksimum 5 iş günü
            count = min(count, 5)

            dates = [
                next_monday + timedelta(days=i)
                for i in range(count)
                if (next_monday + timedelta(days=i)).weekday() < 5
            ]

            return {"dates": dates, "warning": None}
        
        norm = BrainAIYugii().normalize_calendar_text(msg_lower)

        if any(k in norm for k in NEXT_WEEK_KEYS):

            next_monday = today + timedelta(days=(7 - today.weekday()))

            # 1️⃣ haftaya + full / hafta içi
            if any(k in norm for k in FULL_KEYS):
                dates = [next_monday + timedelta(days=i) for i in range(5)]
                return {"dates": dates, "warning": None}

            # 2️⃣ haftaya + BELİRLİ GÜNLER (canonical)
            if found_days:
                dates = []
                for g in found_days:              # g = "salı", "çarşamba"
                    idx = CANONICAL_DAY_TO_INDEX.get(g)
                    if idx is None:
                        continue
                    dates.append(next_monday + timedelta(days=idx))

                return {"dates": dates, "warning": None}

            # 3️⃣ sadece "haftaya"
            return {
                "dates": [next_monday + timedelta(days=i) for i in range(5)],
                "warning": None
            }

        # ===============================================================
        # 🔹 Çoklu tekil tarih desteği (örnek: 11 kasım 12 kasım 13 kasım)
        # ===============================================================
        match_coklu_tekil = re.findall(
            r"(\d{1,2})\s*(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)?",
            msg_lower
        )
        if match_coklu_tekil and len(match_coklu_tekil) >= 2 and any(ay for _, ay in match_coklu_tekil):
            try:
                tarih_listesi = []
                for gun, ay in match_coklu_tekil:
                    gun = int(gun)
                    ay_num = MONTHS.get(ay, today.month)
                    t = datetime(year, ay_num, gun).date()
                    if t.weekday() < 5:
                        tarih_listesi.append(t)

                valid_dates = [t for t in tarih_listesi if today <= t <= today + timedelta(days=30)]
                if not valid_dates:
                    warning = "🚫 Belirttiğiniz tarihler geçmişte veya 30 günü aşıyor."
                    print(warning)
                    return {"dates": [], "warning": warning}

                lines = [f"✅ {t.strftime('%d.%m.%Y (%A)')} → Güncellendi." for t in valid_dates]
                warning_text = "📅 Takvim işlemi tamamlandı:<br>" + "<br>".join(lines)
                print(warning_text)
                return {"dates": valid_dates, "warning": warning_text}
            except Exception as e:
                print(f"⚠️ Çoklu tekil tarih çözüm hatası: {e}")

        # 🔄 Mesaj içindeki hatalı yazılmış MONTHSı düzelt
        for k, v in AY_NORMALIZE.items():
            msg_lower = re.sub(rf"\b{k}\b", v, msg_lower)


        # 📅 Tarih aralığı tespiti (örnek: 30 ekim - 5 kasım arası)
        match_aralik = re.search(
            r"(?P<g1>\d{1,2})\s*(?P<ay1>ocak|şubat|mart|nisan|mayıs|haziran|temmuz|"
            r"ağustos|eylül|ekim|kasım|aralık)?"
            r".*?(?:-|–|ile|ve|,|'?(?:den|dan|ten|tan)|'?(?:a|e|ye|ya)|kadar|dek)\s*"
            r"(?P<g2>\d{1,2})\s*(?P<ay2>ocak|şubat|mart|nisan|mayıs|haziran|temmuz|"
            r"ağustos|eylül|ekim|kasım|aralık)?"
            r".*?(arası|arasında|kadar|dek)?",
            msg_lower
        )
        if match_aralik:
            try:
                g1 = int(match_aralik.group("g1"))
                g2 = int(match_aralik.group("g2"))
                ay1 = match_aralik.group("ay1")
                ay2 = match_aralik.group("ay2")

                # Ay bilgilerini çöz (tek ay veya iki farklı ay)
                if ay1 and ay2:
                    start_month, end_month = MONTHS[ay1], MONTHS[ay2]
                elif ay1 and not ay2:
                    start_month = end_month = MONTHS[ay1]
                elif not ay1 and ay2:
                    start_month = end_month = MONTHS[ay2]
                else:
                    start_month = end_month = today.month  # ay belirtilmemişse mevcut ay

                start_date = datetime(year, start_month, g1).date()
                end_date = datetime(year, end_month, g2).date()

                # Eğer bitiş tarihi başlangıçtan küçükse (ör. 30 kasım - 5 aralık)
                if end_date < start_date:
                    end_date = datetime(year + 1, end_month, g2).date()

                warning = None
                max_end = today + timedelta(days=30)

                #  Tarihleri oluştur (sadece hafta içi)
                tarih_listesi = []
                current = start_date
                while current <= end_date:
                    if current.weekday() < 5:
                        tarih_listesi.append(current)
                    current += timedelta(days=1)

                # Geçmiş / Gelecek / Limit Kontrolü
                # Geçmiş / Gelecek / Limit Kontrolü (iyileştirilmiş versiyon)
                valid_dates = []
                message_lines = []
                max_end = today + timedelta(days=30)

                for t in tarih_listesi:
                    if t < today:
                        message_lines.append(f"❌ {t.strftime('%d.%m.%Y (%A)')} → Geçmiş tarih, işaretlenemedi.")
                        continue
                    if t > max_end:
                        message_lines.append(f"⚠️ {t.strftime('%d.%m.%Y (%A)')} → 30 gün sınırını aşıyor, eklenmedi.")
                        continue
                    if t.weekday() >= 5:
                        message_lines.append(f"🚫 {t.strftime('%d.%m.%Y (%A)')} → Hafta sonu, eklenmedi.")
                        continue

                    valid_dates.append(t)
                    message_lines.append(f"✅ {t.strftime('%d.%m.%Y (%A)')} → Güncellendi.")

                #  Hiç geçerli tarih yoksa tamamen iptal
                if not valid_dates:
                    warning_text = "📅 Takvim işlemi tamamlanamadı:<br>" + "<br>".join(message_lines)
                    print(warning_text)
                    return {"dates": [], "warning": warning_text}

                #  Hem geçmiş hem geçerli tarih varsa (kısmi başarı)
                if len(valid_dates) < len(tarih_listesi):
                    warning_text = "📅 Takvim işlemi kısmen tamamlandı:<br>" + "<br>".join(message_lines)
                else:
                    warning_text = "📅 Takvim işlemi tamamlandı:<br>" + "<br>".join(message_lines)

                print(warning_text)
                return {"dates": valid_dates, "warning": warning_text}

            except Exception as e:
                print(f"⚠️ Aralık çözüm hatası: {e}")

        month_pattern = "|".join(MONTHS.keys())

        match_tek_tarih = re.search(
            rf"(?P<gun>\d{{1,2}})\s+(?P<ay>{month_pattern})(?:\s+(?P<yil>20\d{{2}}))?",
            msg_lower
        )

        if match_tek_tarih:
            gun = int(match_tek_tarih.group("gun"))
            ay = match_tek_tarih.group("ay")
            ay_num = MONTHS[ay]

            yil = int(match_tek_tarih.group("yil")) if match_tek_tarih.group("yil") else today.year

            tarih = datetime(yil, ay_num, gun).date()

            if tarih < today:
                return {
                    "dates": [],
                    "warning": f"❌ {tarih.strftime('%d.%m.%Y (%A)')} geçmiş tarih, işaretlenemez."
                }

            return {"dates": [tarih], "warning": None}


        # 🧩 HAFTAYA / GELECEK / ÖNÜMÜZDEKİ HAFTA DESTEK BLOĞU (BURAYA EKLENİYOR!)
        weekdays = {
            "pazartesi": 0,
            "salı": 1,
            "çarşamba": 2,
            "perşembe": 3,
            "cuma": 4,
            "cumartesi": 5,
            "pazar": 6
        }


        # 🔹 Bu haftanın ve gelecek haftanın başlangıç tarihleri
        monday = today - timedelta(days=today.weekday())
        next_monday = monday + timedelta(days=7)

        if found_days:
            tarih_listesi = []

            norm = self.normalize_calendar_text(msg_lower)


            is_next_week = any(k in norm for k in NEXT_WEEK_KEYS)
            is_this_week = "bu hafta" in norm or "bu pazartesi" in norm

            # anchor pazartesi
            if is_next_week:
                base_monday = today - timedelta(days=today.weekday()) + timedelta(days=7)
            else:
                base_monday = today - timedelta(days=today.weekday())

            # 🔹 "bu pazartesi", "bu hafta pazartesi" ifadelerinde geçmiş tarih kontrolü
            if any(
                prefix in norm and any(day in norm for day in PAZARTESI_VARIANTS)
                for prefix in BU_WEEK_DAY_PREFIXES
            ):
                tarih = base_monday
                if tarih < today:
                    return {
                        "dates": [],
                        "warning": f"❌ {tarih.strftime('%d.%m.%Y (%A)')} → Geçmiş tarih (bu pazartesi) işaretlenemedi."
                    }
                
            # 🔹 Her bir günü sırayla işle
            for g in found_days:
                idx = CANONICAL_DAY_TO_INDEX[g]


                # seçilen haftadaki gün
                tarih = base_monday + timedelta(days=idx)

                has_explicit_date = bool(re.search(r"\d", msg_lower))
                has_bu = "bu " in msg_lower
                has_gecen = "geçen" in msg_lower or "onceki" in msg_lower

                # 🔹 Eğer açık tarih veya "bu cuma" gibi net ifade varsa ASLA kaydırma
                if tarih < today:
                    if has_explicit_date or has_bu or has_gecen:
                        return {
                            "dates": [],
                            "warning": f"❌ {tarih.strftime('%d.%m.%Y (%A)')} geçmiş tarih, işaretlenemez."
                        }
                    else:
                        # sadece çıplak gün adıysa ileri kaydır
                        tarih += timedelta(days=7)

                if tarih.weekday() < 5:
                    tarih_listesi.append(tarih)

            if tarih_listesi:
                print(f"📅 Gün(ler) algılandı → {tarih_listesi}")
                return {"dates": tarih_listesi, "warning": None}


        if any(x in msg_lower for x in ["boyunca", "tüm ay", "bu ay", "gelecek ay", "önümüzdeki ay"]):
            if "gelecek" in msg_lower or "önümüzdeki" in msg_lower:
                ay = today.month + 1 if today.month < 12 else 1
                year = year if today.month < 12 else year + 1
            else:
                ay = today.month

            last_day = calendar.monthrange(year, ay)[1]
            tarih_listesi = [
                datetime(year, ay, d).date()
                for d in range(1, last_day + 1)
                if datetime(year, ay, d).weekday() < 5
            ][:30]

            return {"dates": tarih_listesi, "warning": None}

        # 🔥 AY İSMİ + BOYUNCA (ör: "aralık boyunca", "mart ayı boyunca", "temmuz komple")
        for ay_adi, ay_num in MONTHS.items():
            if f"{ay_adi} boyunca" in msg_lower or f"{ay_adi} ayı boyunca" in msg_lower or f"{ay_adi} komple" in msg_lower:
                
                last_day = calendar.monthrange(year, ay_num)[1]
                max_date = today + timedelta(days=30)

                tarih_listesi = []

                for d in range(1, last_day + 1):
                    t = datetime(year, ay_num, d).date()

                    # Geçmiş gün → at
                    if t < today:
                        continue

                    # Hafta sonu → at
                    if t.weekday() >= 5:
                        continue

                    # 30 gün sonrası → at
                    if t > max_date:
                        continue

                    tarih_listesi.append(t)

                return {"dates": tarih_listesi, "warning": None}

        if "ayın başı" in msg_lower or "ay başı" in msg_lower:
            tarih_listesi = [
                today + timedelta(days=i)
                for i in range(0, 10)
                if (today + timedelta(days=i)).weekday() < 5
            ]
            return {"dates": tarih_listesi, "warning": None}

        if "ayın ortası" in msg_lower or "ay ortası" in msg_lower:
            tarih_listesi = [
                today + timedelta(days=i)
                for i in range(10, 20)
                if (today + timedelta(days=i)).weekday() < 5
            ]
            return {"dates": tarih_listesi, "warning": None}

        if "ayın sonu" in msg_lower or "ay sonu" in msg_lower:
            tarih_listesi = [
                today + timedelta(days=i)
                for i in range(20, 31)
                if (today + timedelta(days=i)).weekday() < 5
            ]
            return {"dates": tarih_listesi, "warning": None}
        
    


        match_weeks = re.search(r"(?:(önümüzdeki|gelecek)\s*)?(\d+)\s*hafta", msg_lower)
        if match_weeks:
            try:
                week_count = int(match_weeks.group(2))
                start = next_monday if any(x in msg_lower for x in ["önümüzdeki", "gelecek"]) else monday
                end = start + timedelta(days=7 * week_count)
                max_end = today + timedelta(days=30)
                if end > max_end:
                    end = max_end
                tarih_listesi = []
                current = start
                while current < end:
                    if current.weekday() < 5:
                        tarih_listesi.append(current)
                    current += timedelta(days=1)
                return {"dates": tarih_listesi, "warning": None}
            except Exception as e:
                print(f"⚠️ 'Önümüzdeki X hafta' çözüm hatası: {e}")

        izin_durumu = any(x in msg_lower for x in ["izin", "tatil", "izinliyim", "izinli"])

        norm = self.normalize_calendar_text(msg_lower)


        is_this_week = any(k in norm for k in BU_WEEK_DAY_PREFIXES)
        is_next_week = any(k in norm for k in NEXT_WEEK_KEYS)

        if is_this_week and not is_next_week:
            monday = today - timedelta(days=today.weekday())
            week_days = [monday + timedelta(days=i) for i in range(5)]
            week_days = [d for d in week_days if d >= today]
            return {"dates": week_days, "warning": None}
        
        #(TEKİL / TOPLU AMA SADECE HAFTA SONU KELİMESİ VARSA)
        HAS_WEEKEND_KEYWORD = any(
            k in msg_lower
            for k in ["cumartesi", "pazar", "hafta sonu", "haftasonu","cmrtesi","pzr","pazr","hfta sonu","cmrt","cumartesi"]
        )

        # Daha önce hiç tarih bulunamadıysa ve hafta sonu deniyorsa
        if HAS_WEEKEND_KEYWORD:
            base_monday = (
                today + timedelta(days=(7 - today.weekday()))
                if any(k in msg_lower for k in NEXT_WEEK_KEYS)
                else today - timedelta(days=today.weekday())
            )

            weekend_dates = [
                base_monday + timedelta(days=5),  # Cumartesi
                base_monday + timedelta(days=6),  # Pazar
            ]

            return {"dates": weekend_dates, "warning": None}
        
        if (
            "tüm hafta" in msg_lower or "tum hafta" in msg_lower
            or "komple" in msg_lower
            or "full" in msg_lower
            or "haftanın tamamı" in msg_lower or "haftanin tamami" in msg_lower
            or "tamamı" in msg_lower or "tamami" in msg_lower
            or "hepsi" in msg_lower
            or "hafta içi" in msg_lower or "hafta içini" in msg_lower or "hafta ici" in msg_lower
        ):
            # Bu haftanın pazartesisi
            monday = today - timedelta(days=today.weekday())

            # Eğer bugün hafta sonu (Cumartesi–Pazar) ise → gelecek haftaya başla
            if today.weekday() >= 5:
                monday = monday + timedelta(days=7)

            # Eğer kullanıcı "haftaya" dediyse → gelecek hafta
            if any(x in msg_lower for x in ["haftaya", "gelecek", "önümüzdeki"]):
                monday = monday + timedelta(days=7)

            # Pazartesi–Cuma arasındaki günler
            week_days = [monday + timedelta(days=i) for i in range(5)]

            #  Geçmiş günleri AT
            week_days = [d for d in week_days if d >= today]

            #  Hafta sonu zaten yok (pazartesi-cuma) ama yine de filtre:
            week_days = [d for d in week_days if d.weekday() < 5]

            return {"dates": week_days, "warning": None}

    
