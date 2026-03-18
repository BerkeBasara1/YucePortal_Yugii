from .shared import *


class ParkingCreateMixin:
    def otopark_parse_tarih(self, user_message: str):

        today = datetime.now().date()
        text = user_message.lower().replace("'", "").replace("’", "").strip()

        def strip_weekday_suffixes(text: str) -> str:
            suffixes = ["ye","ya","de","da","den","dan","te","ta","nde","nda","inde","ında","ine","ına"]
            for day in ["pazartesi","salı","çarşamba","perşembe","cuma","cumartesi","pazar"]:
                for suf in suffixes:
                    text = re.sub(rf"\b{day}{suf}\b", day, text)
            return text

        def normalize_weekdays_fuzzy(text: str) -> str:
            weekdays = ["pazartesi","salı","çarşamba","perşembe","cuma","cumartesi","pazar"]
            words = text.split()
            for i, w in enumerate(words):
                match = difflib.get_close_matches(w, weekdays, n=1, cutoff=0.75)
                if match:
                    words[i] = match[0]
            return " ".join(words)

        #aylarda yazım yanlışını doğruya çevirmek için
        def normalize_months_fuzzy(text: str) -> str:
            months = [
                "ocak","şubat","mart","nisan","mayıs",
                "haziran","temmuz","ağustos",
                "eylül","ekim","kasım","aralık"
            ]
            words = text.split()
            for i, w in enumerate(words):
                match = difflib.get_close_matches(w, months, n=1, cutoff=0.75)
                if match:
                    words[i] = match[0]
            return " ".join(words)
        
        #ay eklerini temizlemek için
        def strip_month_suffixes(text: str) -> str:
            suffixes = [
                "da","de","ta","te",
                "dan","den","tan","ten",
                "a","e","ya","ye",
                "nda","nde","ında","inde",
                "nın","nin"
            ]
            months = [
                "ocak","şubat","mart","nisan","mayıs",
                "haziran","temmuz","ağustos",
                "eylül","ekim","kasım","aralık"
            ]
            for m in months:
                for suf in suffixes:
                    text = re.sub(rf"\b{m}{suf}\b", m, text)
            return text

        # --- normalize ---
        NORMALIZE_GROUPS = {
            "pazartesi": [
                "pzrtsi","pazrtesi","pazartes","pazartesii","pazartesı",
                "pazartesine","pazartesinde","pazartesinden","pazartesiye",
                "pazartesiyi","paazartesi","pazartesi̇","pzt","pzrtsı"
            ],

            "salı": [
                "sali","salıi","salıı","saliya","saliye","salida",
                "salıda","salidan","salıdan","saali","salii","slı",
            ],

            "çarşamba": [
                "carsamba","çarsamba","çarsmaba","çarşmaba","çarşambaı",
                "carsambaa","carsambada","carsambaya","çarsambaa","carsmba"
            ],

            "perşembe": [
                "persembe","perşmbe","perşm","prsmb","ersembe",
                "perşembeı","perşembede","perşembeye","perşembeden","perşembeee","perş","pers","persenbe","persnbe"
            ],

            "cuma": [
                "cumaa","cumaı","cumaya","cumada","cumadan",
                "cumaaa","cuuma","cumaı","cumeya","cumae"
            ],

            "cumartesi": [
                "cumrtesi","cumartes","cumartesii","cumartesiye","cumartesinde",
                "cumartesinden","cumaratesi","cumartesı","cumartesii","cumartes"
            ],

            "pazar": [
                "pazarr","pazara","pazarda","pazardan","pazarı",
                "pazarr","pazzar","paazar","pazarrr","pazarrda"
            ],
            "haftaya": [
                "hafataya", "haftay", "haftayaa", "haftyaa",
                "haftayaa", "haftayaaa", "haftayae","haftya","hftaya","aftaya","hftaya"
            ],

            # --- GÜNSEL İFADELER ---
            "bugün": [
                "bugun","bugünu","bugüne","bugunu","bugünde",
                "bugunden","bu gun","bugünn","bugünı","bugunn"
            ],

            "yarın": [
                "yarin","yarına","yarını","yarinda","yarından",
                "yarinn","yarınn","yarn","yaarın","yarınnn"
            ],

            "öbür gün": [
                "obur gun","oburgun","öbürgun","obur gunn","öbür günn",
                "obur gunu","obur gune","öbür gune","obur gunden","öbürgün"
            ],

            "ertesi gün": [
                "ertesi gun","ertesigun","ertesi gunn","ertesii gun",
                "ertesi gune","ertesi gunden","ertesigunu","ertesi güni","ertsi gun"
            ],
    
            "ocak": ["ocak"],
            "şubat": ["subat","şubatta","subatta","subata"],
            "mart": ["mart","martta","marta"],
            "nisan": ["nisan","nisanda","nisana"],
            "mayıs": ["mayis","mayista","mayisa"],
            "haziran": ["haziran","haziranda","hazirana"],
            "temmuz": ["temmuz","temmuzda","temmuza"],
            "ağustos": ["agustos","agust","agu","agustosta","agustosa"],
            "eylül": ["eylul","eylule","eylulde"],
            "ekim": ["ekim","ekimde","ekime"],
            "kasım": ["kasim","kasm","kasımda","kasima"],
            "aralık": ["aralik","aralikta","araliga"]
        }

        for correct, variants in NORMALIZE_GROUPS.items():
            for v in variants:
                text = text.replace(v, correct)


        #  GÜN NORMALIZATION (TEK YER)
        text = strip_weekday_suffixes(text)
        text = normalize_weekdays_fuzzy(text)

        #  AY NORMALIZATION (TEK YER)
        text = strip_month_suffixes(text)
        text = normalize_months_fuzzy(text)

        TEMPORAL_ANCHORS = {
            "next_week": [
                "haftaya",
                "gelecek hafta",
                "önümüzdeki hafta",
                "bir sonraki hafta",
                "diger hafta"
            ],
            "this_week": [
                "bu hafta"
            ]
        }
        tokens = text.split()

        # 🔒 GLOBAL ANCHOR (yazım hatasında anchor düşmesin diye)
        detected_global_anchor = None
        for anchor, variants in TEMPORAL_ANCHORS.items():
            for v in variants:
                if v in text:
                    detected_global_anchor = anchor
                    break
        MONTHS = {
            "ocak":1,"şubat":2,"mart":3,"nisan":4,"mayıs":5,
            "haziran":6,"temmuz":7,"ağustos":8,
            "eylül":9,"ekim":10,"kasım":11,"aralık":12
        }
        dates = []
        # BUGÜN / YARIN / ÖBÜR GÜN
        text = text.lower()
        text = re.sub(r"\s+", " ", text)

        # BUGÜN / YARIN / DÜN
        if any(t in text for t in RELATIVE_DAY_TRIGGERS["today"]):
            dates.append(today)

        if any(t in text for t in RELATIVE_DAY_TRIGGERS["tomorrow"]):
            dates.append(today + timedelta(days=1))

        if "öbür gün" in text or "ertesi gün" in text:
            dates.append(today + timedelta(days=2))

        #  HAFTAYA + BUGÜN (SADECE YAN YANA)
        if contains_next_week_relative(text, "today", max_gap=1):
            return {"dates": [today + timedelta(days=7)]}

        #  HAFTAYA + YARIN (SADECE YAN YANA)
        if contains_next_week_relative(text, "tomorrow", max_gap=1):
            return {"dates": [today + timedelta(days=8)]}
        
        #  HAFTAYA ama GÜN YOKSA → Pazartesi–Cuma
        if any(k in text for k in NEXT_WEEK_KEYS) and not any(
            g in text for g in ALL_WEEKDAY_VARIANTS
        ):
            monday = today + timedelta(days=(7 - today.weekday()))
            dates = [monday + timedelta(days=i) for i in range(5)]
            return {"dates": dates}

        # GÜN KAPSAMI (HANGİ GÜNLER?)
        DAY_SCOPES = {
            "all_days": [
                "tum gunler", "tüm günler","hafta boyu her gün ","hafta boynca","tüm hfta",
                "tum hafta", "tüm hafta","tüm hafta içi","hafta içi hergün",
                "hafta boyunca",
                "komple",
                "tamami", "tamamı"
            ],
            "weekdays": [
                "hafta ici", "hafta içi",
                "is gunleri", "iş günleri"
            ],
            "weekend": [
                "hafta sonu","hfta sonu",
                "weekend"
            ]
        }

        #  HER GÜN / HER GÜNE ALGILAMA
        has_every_day = any(k in text for k in EVERY_DAY_KEYS)

        if has_every_day:
            #  Haftaya her gün
            if detected_global_anchor == "next_week":
                base_monday = today + timedelta(days=(7 - today.weekday()))
                dates = [
                    base_monday + timedelta(days=i)
                    for i in range(5)   # hafta içi
                ]
                return {"dates": dates}

            #  Bu hafta her gün
            if detected_global_anchor == "this_week":
                base_monday = today - timedelta(days=today.weekday())
                dates = [
                    base_monday + timedelta(days=i)
                    for i in range(5)
                    if base_monday + timedelta(days=i) >= today
                ]
                return {"dates": dates}

            #  Bu ay her gün
            if any(k in text for k in THIS_MONTH_KEYS):
                start = today
                end = datetime(
                    today.year,
                    today.month,
                    calendar.monthrange(today.year, today.month)[1]
                ).date()

                dates = []
                cur = start
                while cur <= end:
                    if cur.weekday() < 5:   # hafta içi
                        dates.append(cur)
                    cur += timedelta(days=1)

                return {"dates": dates}

            #Sadece "her gün" (anchor yoksa → bugünden itibaren 5 iş günü)
            dates = []
            cur = today
            while len(dates) < 5:
                if cur.weekday() < 5:
                    dates.append(cur)
                cur += timedelta(days=1)

            return {"dates": dates}

        # SCOPE + ANCHOR (tüm hafta / hafta içi / hafta sonu)
        detected_scope = None
        for scope, variants in DAY_SCOPES.items():
            for v in variants:
                if v in text:
                    detected_scope = scope
                    break

        # Anchor zaten normalize sonrası global tespit edildi
        if detected_scope and detected_global_anchor:

            if detected_global_anchor == "next_week":
                base_monday = today + timedelta(days=(7 - today.weekday()))
            else:
                base_monday = today - timedelta(days=today.weekday())

            if detected_scope == "all_days":
                for i in range(7):
                    dates.append(base_monday + timedelta(days=i))

            elif detected_scope == "weekdays":
                for i in range(5):
                    dates.append(base_monday + timedelta(days=i))

            elif detected_scope == "weekend":
                dates.append(base_monday + timedelta(days=5))
                dates.append(base_monday + timedelta(days=6))

        # WEEKDAY ÇÖZÜMÜ (scope YOKSA)
        if not detected_scope:

            WEEKMAP = {
                "pazartesi":0,"salı":1,"çarşamba":2,
                "perşembe":3,"cuma":4,"cumartesi":5,"pazar":6
            }

            def resolve_weekday_with_anchor(gun, anchor):
                idx = WEEKMAP[gun]

                if anchor == "next_week":
                    base = today + timedelta(days=(7 - today.weekday()))
                    return base + timedelta(days=idx)

                if anchor == "this_week":
                    base = today - timedelta(days=today.weekday())
                    return base + timedelta(days=idx)

                diff = idx - today.weekday()
                if diff <= 0:
                    diff += 7
                return today + timedelta(days=diff)

            for token in tokens:
                if token in WEEKMAP:
                    dates.append(
                        resolve_weekday_with_anchor(
                            token,
                            detected_global_anchor
                        )
                    )

        # TÜM AY / TÜM AY BOYUNCA
        if "tüm ay" in text and ("komple" in text or "boyunca" in text or "tamamı" in text):
            start = today
            end = datetime(today.year, today.month,
                        calendar.monthrange(today.year, today.month)[1]).date()
            cur = start
            while cur <= end:
                dates.append(cur)
                cur += timedelta(days=1)

        # BU AY KOMPLE / BU AY BOYUNCA        
        if "bu ay" in text and ("komple" in text or "boyunca" in text or "tamamı" in text):
            start = today
            end = datetime(today.year, today.month,
                        calendar.monthrange(today.year, today.month)[1]).date()
            cur = start
            while cur <= end:
                dates.append(cur)
                cur += timedelta(days=1)

        for ay, ay_num in MONTHS.items():
            if f"{ay} boyunca" in text or f"{ay} komple" in text or f"{ay} tamamı" in text:
                start = datetime(today.year, ay_num, 1).date()
                end = datetime(today.year, ay_num, calendar.monthrange(today.year, ay_num)[1]).date()
                cur = start
                while cur <= end:
                    dates.append(cur)
                    cur += timedelta(days=1)

        # AY + GÜN (15 kasım)
        for gun, ay in re.findall(
            r"(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)",
            text
        ):
            try:
                dates.append(datetime(today.year, MONTHS[ay], int(gun)).date())
            except:
                pass

        # TARİH ARALIĞI (15 kasım - 20 kasım)
        m = re.search(
            r"(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)"
            r".*?(?:-|–|ile|den|dan).*?"
            r"(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)",
            text
        )
        if m:
            g1, a1, g2, a2 = m.groups()
            try:
                d1 = datetime(today.year, MONTHS[a1], int(g1)).date()
                d2 = datetime(today.year, MONTHS[a2], int(g2)).date()
                if d1 > d2:
                    d1, d2 = d2, d1
                cur = d1
                while cur <= d2:
                    dates.append(cur)
                    cur += timedelta(days=1)
            except:
                pass

        # ------------------------------------------------
        # FORMATLI TARİHLER (15.11 / 15-11 / 15/11)
        # ------------------------------------------------
        for s in re.findall(r"\d{1,2}[./-]\d{1,2}(?:[./-]\d{2,4})?", text):
            try:
                dates.append(dateutil.parser.parse(s, dayfirst=True).date())
            except:
                pass

        return {
            "dates": sorted(set(dates))
        }

    def gpt_fix_calendar_text(self, text: str) -> str:
        """
        "Metindeki yazım hatalarını düzelt. "
        "ANLAMI ASLA değiştirme. "
        "⚠️ GÜN VE TARİH ifadelerine asla dokunma. "
        "Perşembe → cuma gibi düzeltmeler YASAK. "
        "Sadece yazım hatalarını düzelt. "
        "Ör: 'perişme' → 'perşembe', 'hafaya' → 'haftaya'. "
        "Ancak anlamı değiştirecek tahminler yapma."

        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Metindeki sadece yazım hatalarını düzelt. "
                            "ANLAMI ASLA değiştirme. "
                            "⚠️ GÜN isimlerini ASLA değiştirme: pazartesi, salı, çarşamba, perşembe, cuma, cumartesi, pazar—"
                            "bu isimlerde düzeltme YAPABİLİRSİN ama BAŞKA bir güne çeviremezsin. "
                            "Örnek: 'perşenbe' → 'perşembe' olur, ama 'perşembe' → 'cuma' OLMAZ. "
                            "Tarihsel veya mantıksal tahmin yapma. "
                            "Kullanıcı ne yazdıysa O kalsın."
                        )
                    },

                    {"role": "user", "content": text}
                ],
                max_tokens=80,
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except:
            return text
        
    def gpt_extract_dates(self, text: str):
        """
        Karmaşık doğal dil tarih ifadelerini anlamak için GPT'yi kullanır.
        Örneğin: 'yarından 3 gün sonra', 'önümüzdeki ay ortası'.
        Çıktı ISO formatlı tarih listesi olur: ['2024-11-15', '2024-11-18'].
        """
        today = datetime.now().date()

        prompt = f"""
        Bugünün tarihi: {today}

        Kullanıcı mesajındaki karmaşık tarih ifadelerini analiz et.
        - 'yarından sonra 3 gün'
        - 'gelecek ayın ortası'
        - 'haftaya salıdan iki gün sonra'
        - '3 gün sonra'
        gibi ifadeleri kesin tarihlere çevir.

        Sadece ISO formatlı Python listesi döndür:
        Örnek: ["2024-11-15", "2024-11-18"]

        Eğer hesaplanacak tarih yoksa: []
        """

        try:
            result = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=120,
                temperature=0
            )
            raw = result.choices[0].message.content.strip()

            if raw.startswith("[") and raw.endswith("]"):
                return eval(raw)
            return []
        except:
            return []

    def resolve_calendar_dates(self, raw_message: str):
        """
        GPT düzeltme (YOL 1) + GPT tarih çıkarımı (YOL 2) +
        klasik tarih parser (parse_takvim_tarih_araligi)
        → En doğru tarih listesi.
        """

        cleaned = raw_message
        work_types_in_text = set()
        tokens = cleaned.split()

        for i in range(len(tokens)):
            wt1 = self.detect_work_type(tokens[i])
            if wt1:
                work_types_in_text.add(wt1)

            if i + 1 < len(tokens):
                wt2 = self.detect_work_type(tokens[i] + " " + tokens[i+1])
                if wt2:
                    work_types_in_text.add(wt2)

        # 🔎 GÖRELİ GÜN VAR MI?
        norm_cleaned = self.normalize_calendar_text(cleaned)

        HAS_RELATIVE_DAY = any(
            k in norm_cleaned for k in ["bugun", "yarin", "obur gun", "ertesi gun"]
        )
        # 🚫 GPT’nin gün isimlerini yanlış düzeltmesini engelle
        gunler = ["pazartesi","salı","sali","çarşamba","carsamba",
                  "perşembe","cuma","cumartesi","pazar"]

        for g in gunler:
            if g in raw_message.lower() and g not in cleaned.lower().replace("ı", "i").replace("İ", "i"):
                print("⚠️ GPT gün ismini yanlış değiştirdi → orijinale dönüldü:", g)
                cleaned = raw_message  # GPT düzeltmesini iptal et
                break


        # 2) GPT tarih çıkarımı dene
        gpt_dates = self.gpt_extract_dates(cleaned)

        norm = self.normalize_calendar_text(cleaned)
        if any(k in norm for k in NEXT_WEEK_KEYS):
            print("❗ [DEBUG] NEXT_WEEK_KEYS tespit edildi → GPT tarihleri yok sayıldı:", gpt_dates)
            gpt_dates = []

        # Eğer GPT bir tarih listesi döndürdüyse → hemen kullan
        if gpt_dates:
            parsed_dates = []
            for iso in gpt_dates:
                try:
                    dt = datetime.fromisoformat(iso).date()
                    parsed_dates.append(dt)
                except:
                    pass

            if parsed_dates:
                # Bu tarihleri klasik parser olmadan direkt döndür
                return {"dates": parsed_dates, "warning": None}

        # 🔥 ÇOKLU AY FULL (ocak ve şubat full / boyunca / komple)
        MONTHS = {
            "ocak":1,"subat":2,"şubat":2,"mart":3,"nisan":4,
            "mayis":5,"mayıs":5,"haziran":6,"temmuz":7,
            "agustos":8,"ağustos":8,"eylul":9,"eylül":9,
            "ekim":10,"kasim":11,"kasım":11,"aralik":12,"aralık":12
        }

        text = self.normalize_calendar_text(cleaned)

        multi_months = re.findall(
            r"\b(ocak|subat|şubat|mart|nisan|mayis|mayıs|haziran|temmuz|agustos|ağustos|eylul|eylül|ekim|kasim|kasım|aralik|aralık)\b",
            text
        )

        if len(multi_months) >= 2 and any(k in text for k in ["full", "komple", "tamami", "boyunca"]):
            dates = []
            today = datetime.now().date()

            for ay in dict.fromkeys(multi_months):  # tekrarları sil
                ay_num = MONTHS.get(ay)
                if not ay_num:
                    continue

                start = datetime(today.year, ay_num, 1).date()
                end = datetime(today.year, ay_num, calendar.monthrange(today.year, ay_num)[1]).date()

                cur = start
                while cur <= end:
                    if cur.weekday() < 5:
                        dates.append(cur)
                    cur += timedelta(days=1)

            return {"dates": sorted(set(dates)), "warning": None}

        # 3) GPT işini yapamadıysa → klasik parser’ı çalıştır
        return self.parse_takvim_tarih_araligi(cleaned)


    def _detect_weekday_count_scope(self, text: str):
        """
        'haftaya 5 gün', 'ilk 3 gün', 'haftanın ilk 2 günü'
        return: int | None
        """
        patterns = [
            r"(haftaya|gelecek hafta|onumuzdeki hafta).*(\d)\s*gun",
            r"haftanin\s*ilk\s*(\d)\s*gun",
            r"ilk\s*(\d)\s*gun"
        ]

        for p in patterns:
            m = re.search(p, text)
            if m:
                return int(m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1))

        return None
    

    def handle_otopark_create(self, user_message: str, user_info: dict):
        print("🅿️ CREATE modülü çalışıyor...")

        if any(k in user_message.lower() for k in [
            "boş", "dolu", "müsait", "müsaitlik",
            "yer var", "yer varmı", "yer var mı",
            "boşluk", "uygun","boş yer varmı","musaitmi","doluluk nedir","dolumu","dolu mu"
        ]):
            print(" CREATE engellendi → STATUS'a yönlendirildi")

            return self.handle_otopark_status(user_message, user_info)
        
        username = user_info.get("fullname")
        plaka = user_info.get("plaka")
        plaka2 = user_info.get("plaka2") or user_info.get("arac_plaka2")

        is_company_car = bool(plaka2)

        msg_norm = self.normalize_people_text(user_message)

        # 0) Kullanıcının aracı var mı?
        if not plaka and not plaka2:
            return "🚫 Otopark rezervasyonu yapabilmek için sistemde kayıtlı bir aracınız bulunmamaktadır."

        # 1) Kullanıcının tarih talebini çöz
        parsed = self.otopark_parse_tarih(user_message)
        print("📅 Tarih Parse:", parsed)

        #Saat 8 kuralı 
        today = get_effective_today()

        #Son 3 iş günü kuralı  
        #Hafta sonu sayılmıyor, Geriye doğru 3 iş günü bulunuyor
        three_days_ago = today - timedelta(days=3)

        try:
            conn_check = pyodbc.connect(YA_2El_AracSatis)
            cur_check = conn_check.cursor()

            #Gelinmeyen rezervasyon son 3 İŞ GÜNÜ içindeyse yeni rezervasyona izin vermiyor.
            cur_check.execute("""
                SELECT COUNT(*)
                FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                WHERE username = ?
                AND is_active = 1
                AND Geldi = 0
                AND canceled_at IS NULL
                AND rezerv_tarih >= ?
            """, (username, three_days_ago))

            no_show_count = cur_check.fetchone()[0]
            conn_check.close()

        except Exception as e:
            print("❌ No-show kontrol hatası:", e)
            no_show_count = 0  # fail-open (engelleme yapma)

        if no_show_count > 0:
            return (
                "🚫 Son 3 gün içinde oluşturduğunuz bir otopark rezervasyonunda "
                "şirkete giriş yapılmadığı tespit edildi.<br>"
                "Otopark kullanım verimliliğini artırmak adına, "
                "<b>3 gün sonra</b> tekrar rezervasyon oluşturabilirsiniz."
            )

        # === TARİH FİLTRELEME (TEK DOĞRU YER) ===
        dates = parsed.get("dates", [])

        #otopark create rezervasyon oluşturma
        today = get_effective_today()
        limit = today + timedelta(days=7)

        success_rows = []  
        info_rows = []      
        error_rows = []    
        
        valid_dates = []
        past_dates = []
        too_far_dates = []
        weekend_dates = []
        created_any = False


        for d in dates:
            if d.weekday() >= 5:   # 5=Cumartesi, 6=Pazar
                weekend_dates.append(d)
                continue
            if d < today:
                past_dates.append(d)
            elif d > limit:
                too_far_dates.append(d)
            else:
                valid_dates.append(d)

        for d in weekend_dates:
            error_rows.append((
                d,
                f"🚫 {self.format_date_with_day(d)} → Hafta sonu olduğu için işlenmedi."
            ))

        if not dates:
            return (
                "🅿️ Otopark rezervasyonu oluşturabilmem için bir gün belirtmen gerekiyor 😊<br><br>"
                "Örnekler:<br>"
                "• <b>Yarın için park yeri ayır</b><br>"
                "• <b>Pazartesi ve salı ofise geleceğim, otoparkta park 15 rezerve et</b><br>"
                "• <b>17 kasım için otopark ayır</b>"
            )
        
        # 3) Yetki alanı belirle
        if is_company_car:
            allowed_range = list(range(10, 44))
            priority_range = list(range(36, 44))  # 🔥 öncelikli havuz
        else:
            allowed_range = list(range(10, 36))
            priority_range = []

        print("🔐 Yetkili park aralığı:", allowed_range)
        
        if not valid_dates:
            if past_dates and not too_far_dates:
                return "❌ Girdiğiniz tüm tarihler geçmiş olduğu için işlem yapılamadı."
            if too_far_dates and not past_dates:
                return "⏳ Girdiğiniz tarihler 7 gün sınırını aştığı için işlem yapılamadı."
            if past_dates and too_far_dates:
                return "❌ Geçmiş ve 7 günü aşan tarihler olduğu için işlem yapılamadı."

        try:
            conn = pyodbc.connect(YA_2El_AracSatis)
            cur = conn.cursor()
        except Exception as e:
            print("❌ DB hata:", e)
            return "⚠️ Sistem geçici olarak kullanılamıyor."

        requested_park = None

        # Kullanıcı park numarası yazdıysa yakala
        park_no_match = re.search(
            r"\bpark\s*(?:no\s*)?(\d{1,2})\b",
            user_message.lower()
        )
        if park_no_match:
            requested_park = int(park_no_match.group(1))

        # === ANA DÖNGÜ ===
        for t in valid_dates:
            gun_str = self.format_date_with_day(t)

            # 1) Kullanıcının o gün zaten rezervasyonu var mı?
            cur.execute("""
                SELECT COUNT(*)
                FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                WHERE username=? AND rezerv_tarih=? AND is_active=1
            """, (username, t))
            already = cur.fetchone()[0]

            if already > 0:
                info_rows.append((
                    t,
                    f"♻️ {gun_str} → Aktif rezervasyonunuz var."
                ))
                continue

            if requested_park:

                # Yetkisi var mı?
                if requested_park not in allowed_range:
                    error_rows.append((
                        t,
                        f"🚫 {gun_str} → {requested_park} numaralı park için yetkiniz yok."
                    ))
                    continue
                if requested_park < 10:
                    error_rows.append((
                        t,
                        f"🚫 {gun_str} → 1–9 arası parklar rezerve edilemez."
                    ))
                    continue

                # Park dolu mu?
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                    WHERE rezerv_tarih=? AND rezerv_park_no=? AND is_active=1
                """, (t, requested_park))
                dolu = cur.fetchone()[0]

                if dolu > 0:
                    # 🔥 O günün boş parklarını bul
                    cur.execute("""
                        SELECT rezerv_park_no
                        FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                        WHERE rezerv_tarih=? AND is_active=1
                    """, (t,))
                    dolu_liste = {int(r[0]) for r in cur.fetchall()}
                    bos_liste = [p for p in allowed_range if p not in dolu_liste]

                    bos_str = ", ".join(map(str, bos_liste[:12]))

                    error_rows.append((
                        t,
                        f"🚫 {gun_str} → {requested_park} numaralı park dolu. "
                        f"Uygun park sayısı: {len(bos_liste)}"
                    ))
                    continue


                # Park boş → oluştur
                cur.execute("""
                    INSERT INTO [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                        (username, plaka, rezerv_tarih, rezerv_park_no, created_at, is_active, aciklama, Geldi, guvenlik_aciklama)
                    VALUES (?, ?, ?, ?, GETDATE(), 1, '', 1, '')
                """, (username, plaka or plaka2, t, requested_park))
                
                conn.commit()

                created_any = True

                success_rows.append((
                    t,
                    f"🅿️ {gun_str} → {requested_park} numaralı park rezerve edildi."
                ))
                continue

            # === Kullanıcı park numarası belirtmediyse → RANDOM PARK AYIR ===
            
            # O günün dolu parklarını al
            cur.execute("""
                SELECT rezerv_park_no
                FROM [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                WHERE rezerv_tarih=? AND is_active=1
            """, (t,))
            dolu_olanlar = {int(r[0]) for r in cur.fetchall()}

            # Boş parkları belirle
            bos_olanlar = [p for p in allowed_range if p not in dolu_olanlar]

            if not bos_olanlar:
                error_rows.append((
                    t,
                    f"🚫 {gun_str} → Uygun park bulunamadı."
                ))
                continue

            # 🚗 ŞİRKET ARACI ÖNCELİĞİ (36–43)
            if priority_range:
                priority_boslar = [p for p in priority_range if p in bos_olanlar]

                if priority_boslar:
                    secilen = random.choice(priority_boslar)  # önce 36–43
                else:
                    secilen = random.choice(bos_olanlar)      # fallback
            else:
                secilen = random.choice(bos_olanlar)

            # RANDOM → INSERT
            cur.execute("""
                INSERT INTO [Yuce_PortalTest].[dbo].[YA_otopark_TEST]
                    (username, plaka, rezerv_tarih, rezerv_park_no, created_at, is_active, aciklama, Geldi, guvenlik_aciklama)
                VALUES (?, ?, ?, ?, GETDATE(), 1, '', 1, '')
            """, (username, plaka or plaka2, t, secilen))
            conn.commit()

            created_any = True

            success_rows.append((
                t,
                f"🅿️ {gun_str} → {secilen} numaralı park rezerve edildi."
            ))

        for d in past_dates:
            error_rows.append((
                d,
                f"❌ {self.format_date_with_day(d)} → Geçmiş tarih."
            ))


        for d in too_far_dates:
            error_rows.append((
                d,
                f"⏳ {self.format_date_with_day(d)} → 7 gün kuralı nedeniyle oluşturulmadı."
            ))

        conn.close()

        def _sort(rows):
            return [text for _, text in sorted(rows, key=lambda x: x[0])]

        success_rows = _sort(success_rows)
        info_rows = _sort(info_rows)
        error_rows = _sort(error_rows)
    
        #mesaj son 
        intro = self.naturalize_intro("otopark_create")
        
        sections = []

        if success_rows:
            sections.append(
                "🅿️ <b>Otopark Rezervasyonu</b><br>" +
                "<br>".join(success_rows)
            )

        if info_rows:
            sections.append(
                "ℹ️ <b>Bilgilendirme</b><br>" +
                "<br>".join(info_rows)
            )

        if error_rows:
            sections.append(
                "⚠️ <b>İşlem Yapılamayan Günler</b><br>" +
                "<br>".join(error_rows)
            )

        body = "<br><br>".join(sections)

        has_calendar_action = any(f in msg_norm for f in self.TAKVİM_KEYS)
        has_work_type = bool(self.detect_work_type(msg_norm))

        has_calendar_intent = has_calendar_action and has_work_type


        if created_any:
            outro_base = "Uygun günler için otopark rezervasyonu oluşturuldu."
        else:
            outro_base = "Otopark rezervasyonu oluşturulamadı."

        # Haftalık takvim niyeti varsa → LLM outro YOK
        if has_calendar_intent:
            outro = outro_base          
        else:
            outro = self.naturalize_text(outro_base, "otopark_create")


        final = ""
        if intro:
            final += intro + "<br>"

        final += body

        if outro:
            final += "<br>" + outro


        if has_calendar_intent:
            final += (
                "<br><br>🗓️ Ayrıca haftalık takvimle ilgili de bir işlem yapmak istediğini fark ettim.<br>"
                "Bu işlem için ayrıca yardımcı olabilirim tekarar söylemen yeterli."
            )
        return final


