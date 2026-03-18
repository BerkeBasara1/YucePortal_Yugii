from .shared import *


class LanguageHistoryMixin:
    def naturalize_text(self, base_message: str, category: str) -> str:
        """
        Sabit backend mesajlarını daha doğal, çeşitli ve insan gibi hale getirir.
        AI küçük bir ek cümle/ek ifade üretir.
        """
        try:
            prompt = f"""
            Aşağıdaki mesaj {category} kategorisinde bir sistem yanıtıdır.
            Görevin:
            - Anlamı BOZMAMAK.
            - Backend tarafından üretilen mesajı asla değiştirme.
            - Sadece sonuna 1 kısa doğal, samimi, profesyonel cümle ekle.
            - Emoji çok abartma (maks 1 kullan).
            - Cümle Türkçe olmalı.

            Mesaj:
            "{base_message}"

            Sadece geliştirilmiş nihai metni döndür.
            """
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role":"system", "content":prompt}],
                max_tokens=50,
                temperature=0.6
            )
            return resp.choices[0].message.content.strip()
        except:
            return base_message

    def naturalize_intro(self, category: str) -> str:
        """
        Yugii'nin çeşitli modüllerde kullanıcıya verdiği
        kısa, samimi, profesyonel ve işlem belirtmeyen intro cümlesi.
        """
        try:
            prompt = f"""
            Sen Yüce Auto'nun dijital asistanı Yugii'sin.
            Kullanıcıya işlemden ÖNCE gösterilecek çok kısa bir karşılama cümlesi üret.

            Kurallar:
            - En fazla 1 cümle.
            - İşlem belirtme: "kontrol ediyorum", "bakıyorum", "sorguluyorum", "inceleyim", "hallediyorum" gibi fiilleri ASLA kullanma.
            - Cümle sadece karşılayıcı ve olumlu olsun.
            - Profesyonel + samimi bir ton.
            - Emoji 0 veya 1 tane olabilir.
            - Her üretimde farklı ve çeşitli olsun.
            - Asistanın işlevini açıklama, sadece sıcak bir karşılayış olsun.

            Kategori: {category}

            Örnek doğru format kısa cümleler:
            - “Tabii ki 😊”
            - “Elbette, memnuniyetle.”
            - “Buradayım, yardımcı olmaya hazırım 🌿”
            - “Tamamdır 🙂”
            - “Memnuniyetle 💚”

            Sadece cümleyi döndür.
            """

            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=25,
                temperature=0.8
            )
            return resp.choices[0].message.content.strip()

        except:
            return "Tabii ki 😊"
    
    #yemek menüsü cevapları başına doğan cümle ekleme
    def naturalize_food_intro(self):
        try:
            prompt = """
            Yemek menüsü isteği için kullanıcıya gösterilecek
            çok kısa bir karşılama cümlesi üret.

            Kurallar:
            - İşlem belirtme YOK (bakıyorum, kontrol ediyorum vs. yasak).
            - En fazla 1 cümle.
            - 0–1 emoji kullanılabilir.
            - Samimi + profesyonel ton.
            - Her seferinde çeşitli olsun.

            Örnekler:
            - "Elbette 😊"
            - "Seve seve 🌿"
            - "Memnuniyetle 💚"
            - "Tabii ki 😊"
            """
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=20,
                temperature=0.9
            )
            return resp.choices[0].message.content.strip()
        except:
            return "Elbette 😊"

    #Yemek menüsü mesajının SONUNA doğal bir kapanış cümlesi eklemek
    def naturalize_food_outro(self):
        try:
            prompt = """
            Yemek menüsü mesajının sonuna eklenecek,
            kısa, samimi ve yemek temasına uygun bir kapanış cümlesi üret.

            Kurallar:
            - Tek cümle.
            - 0–1 emoji.
            - Afiyet temalı olabilir ama aşırı değil.

            Örnek:
            - "Afiyetle keyifli bir gün dilerim 😊"
            - "Şimdiden afiyet olsun 🌿"
            - "Umarım bugün menü tam damak tadına göredir 💚"
            """
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=20,
                temperature=0.8
            )
            return resp.choices[0].message.content.strip()
        except:
            return "Afiyet olsun 😊"
     
    # çalışma şekli belirleme haftalık takvim
    def _norm(self, s: str) -> str:
        return (
            s.lower()
            .replace("ı", "i")
            .replace("ş", "s")
            .replace("ğ", "g")
            .replace("ü", "u")
            .replace("ö", "o")
            .replace("ç", "c")
        )

    def _strip_tr_suffixes(self, text: str) -> str:
        """
        Türkçe fiil ve isim çekim eklerini kaba şekilde temizler.
        Amaç: geldiğim → geldim → gel
        """
        SUFFIXES = [
            "digim", "tigim",
            "dim", "tim", "dum", "tum",
            "mis", "mus", "mıs", "müş",
            "yor", "iyor",
            "deki", "daki", "teki", "taki",
            "ken", "iken",
            "im", "um", "üm",
            "mi", "mı", "mu", "mü",
        ]

        for suf in SUFFIXES:
            text = re.sub(rf"\b(\w+){suf}\b", r"\1", text)

        return text
    
    def _detect_by_root(self, text: str):

        if not any(x in text for x in ["calis", "ofis", "home", "izin", "bayi"]):
            return None
        
        ROOT_PATTERNS = [
            ("Izin",  [r"\b(izin|tatil|rapor|off)\w*"]),
            ("Home",  [r"\b(ev|home|uzaktan|remote)\w*"]),
            ("Ofis",  [r"\b(ofis|şirket|sirket)\w*"]),
            ("Bayi",  [r"\b(bayi|müşteri|musteri|saha|ziyaret)\w*"]),
        ]

        for work_type, patterns in ROOT_PATTERNS:
            for p in patterns:
                if re.search(p, text, re.IGNORECASE):
                    return work_type

        return None
       
    def detect_work_type(self, msg: str):
            """
            Kullanıcının yazdığı cümleden çalışma tipini tespit eder.
            Ultra dayanıklı, Türkçe karakter uyumlu, tüm varyasyonları kapsar.
            """

            if not msg:
                return None

            # METNİ HAZIRLA (ZORUNLU NORMALIZE)
            text = self._norm(msg)
            text = self._strip_tr_suffixes(text)
            text = re.sub(r"\s+", " ", text).strip()

            ignore_words = {"komple", "boyunca", "tamami", "tamamı","full","tamammına","tamamı","kmple"}
            tokens = text.split()
            tokens = [t for t in tokens if t not in ignore_words]
            text = " ".join(tokens)

            # ⭐ 1) ROOT + REGEX (ANA YOL)
            root_type = self._detect_by_root(text)
            if root_type:
                return root_type
            
            # 2) TÜM ANAhtar kelime listeleri

            # departman / şirket bağlamında work_type çıkmasın

            if any(k in msg for k in ["departman", "departmanlar","şirketteki departmanlar","ofisteki departmanlar","ofiste olan departmanlar"]):
                return None
            izin_words = [
                "izin", "izinli", "izinliyim", "izne", "izindeyim", "izinde",
                "tatil", "tatilde", "tatile", "yıllık izin", "yillik izin",
                "off", "offday", "off-day", "off day", "off gün", "offgun",
                "izinliydim", "izindeydim", "izindeyken", "izin yaptım",
                "izindeyim", "izindeydim","izin almısım","izinlydım","izin isaretlemisim"
            ]

            home_words = [
                # temel
                "home", "homeoffice", "home office",
                "ev", "evde", "evden",
                "evdi", "evdeydi", "evdiydi", "evdeydim", "evdiler", "evdeydiler",
                # çalışma fiilleri
                "evden calis", "evden çalış",
                "evde calis", "evde çalış",

                # uzaktan
                "uzaktan", "remote", "remotely", "wfh",

                # konuşma dili
                "evden baglan", "evden bağlan",
                "evden calisiyorum", "evden çalışıyorum",

                # yazım hataları
                "evdn", "hom"
            ]

            ofis_words = [
                # =====================
                # TEMEL OFİS
                "ofis", "ofiste", "ofise", "ofisten",
                "ofisde", "ofisden",

                # =====================
                # ŞİRKET (ANA)
                # =====================
                "şirket", "şirkete", "şirkette", "şirketten",
                "sirket", "sirkete", "sirkette", "sirketten",

                # =====================
                # İŞ YERİ / BİNA
                # =====================
                "iş yeri", "isyeri", "işyerinde",
                "iş yerinde", "iş yerinden",
                "is yeri", "is yerinde", "is yerinden",
                "merkez", "bina",

                # =====================
                # KONUŞMA DİLİ
                # =====================
                "ofise gel", "ofise geliyorum",
                "ofise geleceğim", "ofise gelecegim",
                "şirkete gel", "şirkete geliyorum",
                "şirkete geleceğim", "şirkete gelecegim","ise gel", "ise geldim", "ise geliyorum",
                "ise git", "ise gittim", "ise gidiyorum",
                "ise var", "ise vardim", "ise vardım",

                # =====================
                # YAYGIN YAZIM HATALARI
                # =====================
                "şirktette", "sirkette","şirketten","şirketde","şirktte","sirketden","şrktten"
            ]

            bayi_words = [
                "bayi", "bayide", "bayiye","bayii",
                "müşteri", "musteri", "ziyaret", "ziyarete", "ziyarette",
                "sahada", "saha", "aktif satış", "sales visit"
            ]


            # -----------------------------
            # 3) DİREKT KELİME İÇERİSİNDE ARA
            # -----------------------------
            for w in izin_words:
                if w in text:
                    return "Izin"

            for w in home_words:
                if w in text:
                    return "Home"

            for w in ofis_words:
                if w in text:
                    return "Ofis"

            for w in bayi_words:
                if w in text:
                    return "Bayi"

            # -----------------------------
            # 4) TOKENS & FUZZY MATCH (%80 üzeri)
            # -----------------------------

            tokens = text.split()

            def fuzzy_match(token, keywords):
                for w in keywords:
                    ratio = difflib.SequenceMatcher(None, token, w).ratio()
                    if ratio >= 0.80:   # güçlü eşleşme
                        return True
                return False

            for t in tokens:
                if fuzzy_match(t, izin_words):
                    return "Izin"
                if fuzzy_match(t, home_words):
                    return "Home"
                if fuzzy_match(t, ofis_words):
                    return "Ofis"
                if fuzzy_match(t, bayi_words):
                    return "Bayi"

            # -----------------------------
            # 5) SEMANTIC HINTS
            # -----------------------------
            if any(h in text for h in ["çalışmıyorum","çalışmadım","rahatsız", "hasta", "yokum", "istirahat","izinli","izin"]):
                return "Izin"

            if re.search(r"\bev(de|den)?\b", text):
                return "Home"

            if any(h in text for h in ["geliyorum", "geleceğim", "ofiste olacağım","geliyor","gelicek","gelecek","gelecek ofise",
            "ofise geliyor", "ofise gelicek","ofise gelecek"
            ]):
                return "Ofis"

            if any(h in text for h in ["bayi", "sahada", "ziyaret","bayide"]):
                return "Bayi"

            # -----------------------------
            # 6) BULUNAMADI
            # -----------------------------
            return None
    
    #Cümleyi “çalışma tipi”ne göre parçalara ayırır
    def extract_worktype_segments(self, text: str):
        """
        Metni work-type bazlı parçalara ayırır.
        Work type TESPİT ETMEZ, detect_work_type kullanır.
        """

        if not text:
            return []

        # normalize + suffix kırma (AYNI AKIŞ)
        t = self._norm(text)
        t = self._strip_tr_suffixes(t)

        tokens = t.split()

        segments = []
        current_tokens = []
        current_type = None

        for i, tok in enumerate(tokens):

            # 🔑 2 kelimelik pencere
            window2 = " ".join(tokens[i:i+2])

            # 🔑 BU HAFTA anchor
            if any(k in window2 for k in BU_WEEK_DAY_PREFIXES):
                current_tokens.append("bu hafta")
                continue

            # 🔑 HAFTAYA / GELECEK HAFTA / ÖNÜMÜZDEKİ HAFTA
            if any(k in window2 for k in NEXT_WEEK_KEYS):
                current_tokens.append("haftaya")
                continue

            # 🔥 VE bağlacı özel kontrolü
            if tok == "ve":
                next_window = " ".join(tokens[i+1:i+3])
                next_type = self.detect_work_type(next_window)

                if next_type and current_tokens and current_type:
                    segments.append({
                        "text": " ".join(current_tokens),
                        "type": current_type
                    })
                    current_tokens = []
                    current_type = None
                continue

            # 🔍 çalışma tipi algılama
            window3 = " ".join(tokens[max(0, i-2):i+1])
            wt = self.detect_work_type(window3)

            if wt:
                if current_tokens and current_type:
                    segments.append({
                        "text": " ".join(current_tokens),
                        "type": current_type
                    })
                    current_tokens = []
                current_type = wt
            else:
                current_tokens.append(tok)

        # son segment
        if current_tokens and current_type:
            segments.append({
                "text": " ".join(current_tokens),
                "type": current_type
            })

        return segments
    
    def is_plate_add_question(self, msg: str) -> bool:
        text = self.normalize_people_text(msg)

        PLATE_KEYWORDS = [
            "plaka ekle",
            "arac plakasi ekle",
            "araç plakası ekle",
            "plaka nasil eklenir",
            "plaka nasil girilir",
            "plakam yok",
            "plaka guncelle",
            "plaka degistir",
            "arac plakasi",
        ]

        return any(k in text for k in PLATE_KEYWORDS)
  
 

    #control_work_history tarih belirleme
    def extract_history_dates(self, message: str):
        """
        Gelişmiş tarih algılama motoru (Geçmiş + Bugün + Gelecek).
        Amaç:
        - Kullanıcının yazdığı doğal cümleden NET bir tarih aralığı çıkarmak.
        - Hem geçmiş hem gelecek ifadelerini anlamak.
        - Limitler:
                Geçmiş: max 365 gün
                Gelecek: max 30 gün
        RETURN:
            { start: date, end: date, mode: "past|future|mixed", source: "gpt|rule" }
        """

        import json
        import regex as re
        import calendar
        from dateutil.relativedelta import relativedelta


        today = datetime.now().date()
        msg = message.lower().strip()

        msg = self.normalize_month_with_suffixes(msg)

        # === AY HARİTASI (TEK KAYNAK) ===
        month_map = {
            "ocak":1, "şubat":2, "mart":3, "nisan":4, "mayıs":5, "haziran":6,
            "temmuz":7, "ağustos":8, "eylül":9, "ekim":10, "kasım":11, "aralık":12
        }

        # TÜM YIL / YIL BOYUNCA
        if any(k in msg for k in ["tum yil", "tüm yil", "yil boyunca", "butun yil"]):
            return {
                "start": date(today.year, 1, 1),
                "end": date(today.year, 12, 31),
                "mode": "mixed",
                "source": "rule"
            }

        # BU YIL
        if "bu yil" in msg or "bu yıl" in msg:
            return {
                "start": date(today.year, 1, 1),
                "end": today,
                "mode": "past",
                "source": "rule"
            }

        # BU AY
        if "bu ay" in msg:
            start = date(today.year, today.month, 1)
            end = today
            return {
                "start": start,
                "end": end,
                "mode": "past",
                "source": "rule"
            }
        # SON X AY (son 3 ay, son 6 ay)
        m = re.search(r"son\s+(\d+)\s+ay", msg)
        if m:
            months = int(m.group(1))
            end = today
            start = today - relativedelta(months=months)
            return {
                "start": start,
                "end": end,
                "mode": "past",
                "source": "rule"
            }
        # ============================================================
        # 🔥 ÇOKLU AY ALGILAMA (ocak ve şubat / kasım, aralık)
        # ============================================================
        found_months = [
            (name, num)
            for name, num in month_map.items()
            if name in msg
        ]

        if len(found_months) >= 2:
            months = [m[1] for m in found_months]
            min_month = min(months)
            max_month = max(months)

            # yıl hesabı (aralık → ocak gibi durumlar)
            start_year = today.year
            end_year = today.year

            if max_month < min_month:
                # yıl geçişi var (aralık-ocak)
                start_year = today.year - 1
                end_year = today.year

            start = datetime(start_year, min_month, 1).date()
            end = datetime(
                end_year,
                max_month,
                calendar.monthrange(end_year, max_month)[1]
            ).date()

            return {
                "start": start,
                "end": end,
                "mode": "future" if start > today else "past" if end < today else "mixed",
                "source": "rule"
            }


        # === YIL HESAPLAMA YARDIMCI FONKSİYONU ===
        def resolve_year_for_month(month_num, today):
            # Eğer ay bugünün ayından büyükse → geçen yıl
            if month_num > today.month:
                return today.year - 1
            # Aksi halde → bu yıl
            return today.year
        
        for name, num in month_map.items():
            if name in msg:
                year = resolve_year_for_month(num, today)
                start = datetime(year, num, 1).date()
                end = datetime(year, num, calendar.monthrange(year, num)[1]).date()
                mode = "future" if start > today else "past"
                return {
                    "start": start,
                    "end": end,
                    "mode": mode,
                    "source": "rule"
                }
        # RULE FALLBACK — Her ihtimale karşı
        for key, triggers in RELATIVE_DAY_TRIGGERS.items():
            if any(t in msg for t in triggers):

                if key == "today":
                    return {
                        "start": today,
                        "end": today,
                        "mode": "past",
                        "source": "rule"
                    }

                if key == "tomorrow":
                    d = today + timedelta(days=1)
                    return {
                        "start": d,
                        "end": d,
                        "mode": "future",
                        "source": "rule"
                    }

                if key == "yesterday":
                    d = today - timedelta(days=1)
                    return {
                        "start": d,
                        "end": d,
                        "mode": "past",
                        "source": "rule"
                    }

        # === BU HAFTA ===
        if any(k in msg for k in THIS_WEEK_KEYS):
            monday = today - timedelta(days=today.weekday())
            friday = monday + timedelta(days=4)
            return {"start": monday,"end": friday,"mode": "mixed","source": "rule" }

        # === GEÇEN HAFTA ===
        if any(k in msg for k in PAST_WEEK_KEYS):
            monday = today - timedelta(days=today.weekday() + 7)
            return {"start": monday, "end": monday + timedelta(days=4), "mode": "past", "source": "rule"}

        # === HAFTAYA ===
        norm = self.normalize_calendar_text(msg)
        if any(k in norm for k in NEXT_WEEK_KEYS):
            monday = today + timedelta(days=(7 - today.weekday()))
            return {"start": monday, "end": monday + timedelta(days=4), "mode": "future", "source": "rule"}

        # === GEÇEN AY ===
        if "geçen ay" in msg or "gecen ay" in msg:
            last_month = today.month - 1 if today.month > 1 else 12
            year = today.year if today.month > 1 else today.year - 1
            last_day = calendar.monthrange(year, last_month)[1]
            return {
                "start": datetime(year, last_month, 1).date(),
                "end": datetime(year, last_month, last_day).date(),
                "mode": "past",
                "source": "rule"
            }
        # === SAYI + AY (tek gün) ===
        match = re.search(r"(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)", msg)
        if match:
            day = int(match.group(1))
            ay_map = {
                "ocak": 1, "şubat":2, "mart":3,"nisan":4,"mayıs":5,"haziran":6,
                "temmuz":7,"ağustos":8,"eylül":9,"ekim":10,"kasım":11,"aralık":12
            }
            month = ay_map[match.group(2)]
            year = resolve_year_for_month(month, today)
            d = datetime(year, month, day).date()
            return {
                "start": d,
                "end": d,
                "mode": "future" if d > today else "past",
                "source": "rule"
            }
    
        # === AY + SAYI (TERS SIRA) → ocak 15 ===
        reverse_match = re.search(
            r"\b(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\s+(\d{1,2})\b",
            msg
        )
        if reverse_match:
            ay = reverse_match.group(1)
            gun = int(reverse_match.group(2))

            ay_num = month_map[ay]
            year = resolve_year_for_month(ay_num, today)

            d = date(year, ay_num, gun)
            return {
                "start": d,
                "end": d,
                "mode": "future" if d > today else "past",
                "source": "rule"
            }
        # === SAYI SAYI SAYI + AY (ör: 11 12 13 kasım) ===
        multi = re.findall(r"(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+(kasım|ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|aralık)", msg)
        if multi:
            g1,g2,g3,ay = multi[0]
            numbers = sorted([int(g1),int(g2),int(g3)])
            ay_map = {
                "ocak":1,"şubat":2,"mart":3,"nisan":4,"mayıs":5,"haziran":6,
                "temmuz":7,"ağustos":8,"eylül":9,"ekim":10,"kasım":11,"aralık":12
            }
            m = ay_map[ay]

            year = resolve_year_for_month(m, today)
            d1 = datetime(year, m, numbers[0]).date()
            d2 = datetime(year, m, numbers[2]).date()
            return {
                "start": d1,
                "end": d2,
                "mode": "future" if d1 > today else "past",
                "source": "rule"
            }

        #  GPT  cümle oluşturma — Hem geçmiş hem gelecek için
        gpt_prompt = f"""
        Kullanıcı çalışma günlerini incelemek istiyor.
        Mesajdan NET bir tarih aralığı çıkarmalısın.

        Sadece ŞU JSON formatında cevap ver:

        {{
            "start": "YYYY-MM-DD",
            "end":   "YYYY-MM-DD"
        }}

        Kurallar:
        - Eğer kullanıcı tek gün soruyorsa start=end yap.
        - Aşağıdaki ifadeleri anlamalısın:
            * bu ay, geçen ay, gelecek ay
            * bu hafta, geçen hafta, haftaya, önümüzdeki hafta
            * 3 gün sonra, 5 gün önce, dün, yarın, bugün
            * 11 kasım, 11-15 kasım, 11 12 13 kasım
            * ayın başı, ayın ortası, ayın sonu
            * geçen sene kasım değil → sadece son 12 ay
        - Eğer tarih çıkaramazsan:
            {{"start": null, "end": null}}
        """
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": gpt_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=120,
            )

            raw = resp.choices[0].message.content.strip()
            gpt_json = json.loads(raw)

            if gpt_json.get("start") and gpt_json.get("end"):
                start = datetime.fromisoformat(gpt_json["start"]).date()
                end = datetime.fromisoformat(gpt_json["end"]).date()

                # GPT üretti ama start>end olabilir → düzelt
                if start > end:
                    start, end = end, start

                # === GPT TARİH YIL AUTO-DÜZELTME ===
                def fix_year_auto(d):
                    # Eğer ay bugünden büyükse → geçen yıl
                    if d.month > today.month:
                        return d.replace(year=today.year - 1)
                    # Aksi halde → bu yıl
                    return d.replace(year=today.year)

                start = fix_year_auto(start)
                end = fix_year_auto(end)

                return {
                    "start": start,
                    "end": end,
                    "mode": "future" if start > today else "past" if end < today else "mixed",
                    "source": "gpt"
                }


        except Exception as e:
            print("GPT tarih hatası:", e)
        #  HIÇBIR ŞEY ÇÖZÜLEMEZSE
        return {"start": None, "end": None, "mode": "unknown", "source": "none"}

    
