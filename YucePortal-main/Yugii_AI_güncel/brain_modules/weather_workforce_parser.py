from .shared import *


class WeatherWorkforceParserMixin:
    def handle_portal_info(self):

        RESPONSES = [
            (
                "YücePortal, Yüce Auto çalışanlarının şirket içi işleyişini kolaylaştırmak için "
                "geliştirilmiş kapsamlı bir dijital platformdur. Otopark rezervasyonu, haftalık "
                "çalışma takvimi işaretleme, raporlar ve  araç bildirimleri gibi birçok "
                "şirket içi modül bu portal üzerinden yönetilir."
            ),
            (
                "YücePortal; otopark rezervasyonu, haftalık takvim, raporlama ve araç bildirimleri "
                "gibi pek çok şirket içi sürecin tek bir çatı altında toplandığı Yüce Auto’ya "
                "özel bir iç portaldır. Amaç, günlük iş akışını sadeleştirmektir."
            ),
            (
                "YücePortal, çalışanların otopark rezervasyonu yapabildiği, haftalık çalışma "
                "takvimini işaretleyebildiği ve raporlara erişebildiği; bunun gibi birçok "
                "kurumsal modülü barındıran merkezi bir platformdur."
            ),
            (
                "YücePortal sayesinde çalışanlar; otopark, haftalık takvim, raporlar ve benzeri "
                "birçok şirket içi modülü tek bir ekran üzerinden hızlı ve pratik şekilde "
                "kullanabilir."
            ),
        ]

        return random.choice(RESPONSES)
    
    def handle_yuce_auto_reputation(self):
        responses = [
            (
                "Yüce Auto, uzun yıllardır otomotiv sektöründe faaliyet gösteren ve "
                "Škoda’nın Türkiye distribütörlüğünü yürüten köklü ve güvenilir bir firmadır."
            ),
            (
                "Yüce Auto; müşteri deneyimi, satış ve satış sonrası hizmetler alanlarında "
                "elde ettiği uluslararası başarılarla sektörde güçlü bir konuma sahiptir."
            ),
            (
                "1989’dan bu yana Škoda markasını Türkiye’de temsil eden Yüce Auto, "
                "istikrarlı büyümesi ve yaygın bayi ağıyla öne çıkan bir şirkettir."
            ),
            (
                "Yüce Auto, hem operasyonel gücü hem de müşteri memnuniyetine verdiği önemle "
                "otomotiv sektöründe saygın bir yere sahiptir."
            ),
            (
                "Yüce Auto; köklü geçmişi, güçlü organizasyonu ve uluslararası ödülleriyle "
                "güven veren bir şirkettir."
            )
        ]

        return random.choice(responses)
    
    def handle_skoda_reputation(self):
        responses = [
            (
                "Škoda hakkında kısaca bilgi vereyim: Václav Laurin ve Václav Klement "
                "1895 yılında Mladá Boleslav’da kendi işlerini kurdu. "
                "Bugün Škoda, dünyanın en köklü otomotiv markalarından biri olarak faaliyet göstermektedir."
            ),
            (
                "Škoda hakkında genel bir bilgi paylaşmak gerekirse, markanın kökeni "
                "1895 yılına dayanır ve uzun yıllara yayılan üretim tecrübesiyle "
                "otomotiv sektöründe güçlü bir konuma sahiptir."
            ),
            (
                "Škoda hakkında kısaca bilgi vereyim: 1895 yılında kurulan marka, "
                "mühendislik mirası ve köklü geçmişiyle otomotiv dünyasında "
                "önemli bir yere sahiptir."
            )
        ]

        return random.choice(responses)


    def get_department_list(self):
        conn = _mysql_conn()
        if conn is None:
            return []

        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT TRIM(departman)
            FROM users1
            WHERE 
                is_active = 1
                AND departman IS NOT NULL
                AND TRIM(departman) <> ''
            ORDER BY departman
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [r[0] for r in rows] 
    def handle_department_list(self):
        departments = self.get_department_list()

        if not departments:
            return "Şu anda departman bilgilerine ulaşılamıyor."

        if len(departments) == 1:
            return f"Şirkette yalnızca <b>{departments[0]}</b> departmanı bulunuyor."

        # düzgün Türkçe liste
        if len(departments) == 2:
            dept_text = " ve ".join(departments)
        else:
            dept_text = ", ".join(departments[:-1]) + " ve " + departments[-1]

        return (
            f"Şirkette toplam <b>{len(departments)}</b> departman bulunuyor:<br>"
            f"{dept_text}."
        )
    
    def handle_charge_reservation_redirect(self):
        return (
            "🔌 Şu an için şarj rezervasyonu konusunda yardımcı olamıyorum.<br><br>"
            "Bu özellik ilerleyen dönemlerde geliştirilecektir.<br><br>"
            "Şimdilik Yüce Portal’daki "
            "<b><a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve'>"
            "şarj rezervasyonu sayfası</a></b> 🔗"
        )

    def detect_weather_day(self, msg: str) -> str:
        msg = self.normalize_people_text(msg)

        if any(w in msg for w in ALL_WEEKDAY_VARIANTS):
            return "weekday_unsupported"

        if "yarin" in msg or "yarinki" in msg:
            return "tomorrow"

        if "bugun" in msg:
            return "today"

        return "today"  # default
    
    def detect_weather_question_type(self, msg: str) -> str:
        msg = self.normalize_people_text(msg)

        if any(k in msg for k in ["kac derece", "kaç derece", "derece"]):
            return "temperature"

        if any(k in msg for k in ["soguk mu", "soğuk mu", "sicak mi", "sıcak mı","yağmurlumu","güneşlimi","soğukmu","sıcakmı"]):
            return "comfort"

        return "general"   # hava nasıl
    
    @staticmethod
    def weather_advice_tag(weathercode: int, temp: float) -> str:
        # 🔥 SICAKLIK BANTLARI (ÖNCELİKLİ)
        if temp < 0:
            return "freezing"
        if 0 <= temp < 10:
            return "very_cold"
        if 10 <= temp <= 25:
            # Ilıman ama yağmur/fırtına varsa onu öne al
            if weathercode in [61, 63, 80]:
                return "rain"
            if weathercode in [95, 99]:
                return "storm"
            return "mild"
        if temp > 25:
            return "hot"

        return "neutral"
    
    def handle_weather_redirect(self, user_message: str):
        try:
            msg_norm = self.normalize_people_text(user_message)

            city_key = None
            for c in self.cities.keys():
                if c in msg_norm:
                    city_key = c
                    break

            if not city_key:
                city_key = "istanbul"

            lat, lon = self.cities[city_key]

            day = self.detect_weather_day(user_message)
            if day == "weekday_unsupported":
                return (
                    "📅 Belirttiğin gün için hava durumu bilgisini şu an gösteremiyorum.<br><br>"
                    "Şimdilik sadece <b>bugün</b> ve <b>yarın</b> için hava durumunu paylaşabiliyorum."
                )

            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}&current_weather=true"
            )

            data = requests.get(url, timeout=5).json()
            weather = data.get("current_weather")

            if not weather:
                return "🌦️ Hava durumu bilgisi şu anda alınamıyor."

            temp = weather["temperature"]
            code = weather["weathercode"]

            desc_map = {
                0: "☀️ Açık",
                1: "🌤 Az bulutlu",
                2: "⛅ Parçalı bulutlu",
                3: "☁️ Bulutlu",
                45: "🌫 Sisli",
                48: "🌫 Sisli",
                51: "🌦 Hafif yağmurlu",
                61: "🌧 Yağmurlu",
                63: "🌧️ Kuvvetli yağmur",
                80: "🌧 Sağanak",
                95: "⛈ Gök gürültülü",
                99: "⛈ Fırtınalı"
            }
            desc = desc_map.get(code, "🌦 Belirsiz hava durumu")

            tag = self.weather_advice_tag(code, temp)
            question_type = self.detect_weather_question_type(user_message)

            return self.llm_weather_sentence(
                user_message=user_message,
                city=city_key.title(),
                temp=round(temp, 1),
                desc=desc,
                advice_tag=tag,
                question_type=question_type
            )

        except Exception as e:
            print("❌ Weather hata:", e)
            return (
                "🌦️ Hava durumu bilgisine şu anda ulaşılamıyor.<br>"
                "İnternet bağlantısı veya servis geçici olarak yanıt vermiyor olabilir."
            )
        
    def llm_weather_sentence(
        self,
        user_message: str,
        city: str,
        temp: float,
        desc: str,
        advice_tag: str,
        question_type: str
    ) -> str:
        """
        Gerçek hava durumu verilerinden,
        kontrollü ve halüsinasyonsuz tek cümle üretir.
        """
        print("🧠 LLM WEATHER ÇALIŞTI:", question_type, advice_tag)

        prompt = f"""
    Aşağıda GERÇEK hava durumu verileri ve
    sistem tarafından belirlenmiş bir öneri etiketi vardır.

    KURALLAR (ÇOK ÖNEMLİ):
    - SADECE verilen verileri kullan.
    - Yeni bilgi ekleme.
    - Tahmin yapma.
    - Gelecek zaman kullanma.
    - Tek cümle yaz.
    - Emoji en fazla 3 tane.
    - Öneri SADECE advice_tag'e göre yapılır.
    - advice_tag = neutral ise öneri ekleyebilirsin.
    - temperature soru tipinde emoji KULLANABİLİRSİN ama öneri  kısaca yapabilirsin genel.

    SORU TİPİ KURALLARI:
    - temperature → dereceyi vurgula
    - comfort → soğuk/sıcak yorumunu yap
    - general → genel hava durumunu anlat

    Advice tag kuralları:
    - freezing  → dondurucu soğuk vurgusu (buzlanma)
    - very_cold → çok soğuk, kalın giyin
    - mild      → ılıman, rahat hava
    - hot       → sıcak, hafif giyin / su için
    - rain      → şemsiye öner
    - storm     → dikkatli olun uyarısı
    - neutral   → genel, kısa yorum

    VERİLER:
    - Şehir: {city}
    - Sıcaklık: {temp}°C
    - Durum: {desc}
    - Advice tag: {advice_tag}
    - Soru tipi: {question_type}

    Kullanıcı mesajı:
    "{user_message}"
    """

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.4,
                max_tokens=60
            )
            return resp.choices[0].message.content.strip()

        except Exception as e:
            print("❌ LLM weather hata:", e)
            return f"{city} için hava durumu {desc}, {temp:.1f}°C."
        

    
    def handle_today_question(self, msg_norm: str) -> str:
        gunler = ["pazartesi","salı","çarşamba","perşembe","cuma","cumartesi","pazar"]

        # 🔑 bugün mü yarın mı?
        is_tomorrow = "yarin" in msg_norm
        offset = 1 if is_tomorrow else 0

        target_date = datetime.now() + timedelta(days=offset)
        day_name = gunler[target_date.weekday()]

        for canonical, variants in {
            "pazartesi": PAZARTESI_VARIANTS,
            "salı": SALI_VARIANTS,
            "çarşamba": CARSAMBA_VARIANTS,
            "perşembe": PERSEMBE_VARIANTS,
            "cuma": CUMA_VARIANTS,
            "cumartesi": CUMARTESI_VARIANTS,
            "pazar": PAZAR_VARIANTS,
        }.items():
            if any(v in msg_norm for v in variants):
                if canonical == day_name:
                    return f"📅 Evet, {'yarın' if is_tomorrow else 'bugün'} {day_name.title()} 😊"
                else:
                    return f"📅 Hayır, {'yarın' if is_tomorrow else 'bugün'} {day_name.title()} 😊"

        responses_today = [
            f"Bugün {day_name.title()}, güzel bir gün — çalışmaya devam edelim 😊",
            f"{day_name.title()}, ne güzel bir gün değil mi, tempoyu bozmayalım.",
            f"Bugün {day_name.title()}, gün güzel görünüyor, keyifle devam edelim.",
            f"{day_name.title()}, hafta akıyor; istersen hava durumuna da bakabilirim 🌦️",
            f"Bugün {day_name.title()}, enerjimiz yerindeyse devam edelim 💪",
            f"{day_name.title()}, günün havasını merak edersen sorman yeterli 😊",
        ]

        responses_tomorrow = [
            f"Yarın {day_name.title()}, şimdiden plan yapmak iyi fikir 🙂",
            f"Yarın {day_name.title()} görünüyor, hazırlıklı olabilirsin.",
            f"Yarın {day_name.title()}, güzel bir gün olacak gibi; istersen hava durumuna da bakabilirim 🌦️",
            f"Yarın {day_name.title()}, tempoya hazır olalım 💪",
        ]

        return "📅 " + random.choice(
            responses_tomorrow if is_tomorrow else responses_today
        )
    
    
    #handle_workforce_status tarih tespiti
    def parse_workforce_dates(self, message: str):
        """
        Workforce için TEK GÜN tarih parser.
        Öncelik sırası:
        1) bugün / yarın / öbür gün
        2) bu + gün / bu hafta + gün
        3) haftaya + gün
        4) sadece gün (en yakın ileri)
        5) net tarih (16 ocak / 16.01 / 16.01.2026)
        6) extract_history_dates fallback
        """
        print("\n🧪 [DATE PARSER] INPUT:", message)

        msg = self.normalize_people_text(message)
        msg = self.normalize_month_with_suffixes(msg)


        # ŞU AN = BUGÜN
        msg = re.sub(
        r"(ofis(?:ten|den|te|de)?)(mi|mı|mu|mü)\b",
        r"\1 \2",
        msg
        )
        msg = re.sub(r"(mi|mı|mu|mü)\b", r" \1", msg)

        #zaman referansı
        today = datetime.now().date()
        current_year = today.year

        #suffix strip (SORU TESPİTİ İÇİN)
        msg_stripped = self._strip_tr_suffixes(msg)

        has_question_particle = (
            bool(re.search(r"(mi|mı|mu|mü)\b", msg))
            or bool(re.search(r"(mi|mı|mu|mü)\b", msg_stripped))
        )
        #  ŞU AN = BUGÜN (SADECE SORU VARSA)
        if has_question_particle and any(k in msg for k in ["suan", "su an"]):
            return {
                "start": today,
                "end": today,
                "mode": "today"
            }
        
        #  BUGÜN / YARIN / ÖBÜR GÜN
        if "bugun" in msg:
            return {"start": today, "end": today, "mode": "today"}
        
        if "yarin" in msg:
            d = today + timedelta(days=1)
            return {"start": d, "end": d, "mode": "future"}

        if "obur gun" in msg or "öbür gun" in msg:
            d = today + timedelta(days=2)
            return {"start": d, "end": d, "mode": "future"}
        
        #  GÜN HARİTASI (VARIANT → WEEKDAY INDEX)
        DAY_VARIANT_MAP = {}

        for v in PAZARTESI_VARIANTS:
            DAY_VARIANT_MAP[v] = 0
        for v in SALI_VARIANTS:
            DAY_VARIANT_MAP[v] = 1
        for v in CARSAMBA_VARIANTS:
            DAY_VARIANT_MAP[v] = 2
        for v in PERSEMBE_VARIANTS:
            DAY_VARIANT_MAP[v] = 3
        for v in CUMA_VARIANTS:
            DAY_VARIANT_MAP[v] = 4
        for v in CUMARTESI_VARIANTS:
            DAY_VARIANT_MAP[v] = 5
        for v in PAZAR_VARIANTS:
            DAY_VARIANT_MAP[v] = 6

        has_day_name = any(v in msg for v in DAY_VARIANT_MAP)
        has_month_name = (
            any(k in msg for k in AY_NORMALIZE.keys())
            or any(m in msg for m in AY_NORMALIZE.values())
        )
        has_day_number = bool(re.search(r"\b\d{1,2}\b", msg))

        #PERIOD ANCHOR VAR + GÜN YOK → TEK GÜN PARSER DEVRE DIŞI
        has_period_anchor = any(k in msg for k in (
            THIS_WEEK_KEYS + PAST_WEEK_KEYS + THIS_MONTH_KEYS
        ))

        has_explicit_day = (
            any(v in msg for v in DAY_VARIANT_MAP)      
            or bool(re.search(r"\b\d{1,2}\b", msg))     
        )

        if has_period_anchor and not has_explicit_day:
            return {"start": None, "end": None, "mode": None}


        for variant, weekday_idx in DAY_VARIANT_MAP.items():
            if variant in msg:

                base_monday = today - timedelta(days=today.weekday())

                # ⏪ GEÇEN HAFTA
                if any(k in msg for k in PAST_WEEK_KEYS):
                    base_monday -= timedelta(days=7)

                # ⏩ HAFTAYA / GELECEK HAFTA
                elif any(k in msg for k in NEXT_WEEK_KEYS):
                    base_monday += timedelta(days=7)

                # 🟡 AKSİ HALDE → bu hafta
                target = base_monday + timedelta(days=weekday_idx)

                return {
                    "start": target,
                    "end": target,
                    "mode": "past" if target < today else "future" if target > today else "today"
                }


        #  NET TARİH — NUMERİK (16.01 / 16.01.2026)
        match_numeric = re.search(r"\b(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?\b", msg)
        if match_numeric:
            day = int(match_numeric.group(1))
            month = int(match_numeric.group(2))
            year = int(match_numeric.group(3)) if match_numeric.group(3) else current_year
            try:
                d = date(year, month, day)
                if d < today:
                    mode = "past"
                elif d > today:
                    mode = "future"
                else:
                    mode = "today"
                return {"start": d, "end": d, "mode": mode}
            except ValueError:
                pass
        #  NET TARİH — AY YAZILI (16 ocak)
        for raw, normalized in AY_NORMALIZE.items():
            msg = re.sub(rf"\b{raw}\b", normalized, msg)

        match_textual = re.search(
            r"\b(\d{1,2})\s+"
            r"(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)"
            r"(?:\s+(\d{4}))?\b",
            msg
        )

        if match_textual:
            day = int(match_textual.group(1))
            month_name = match_textual.group(2)
            year = int(match_textual.group(3)) if match_textual.group(3) else current_year

            MONTH_NUM = {
                "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
                "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8,
                "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12
            }

            try:
                d = date(year, MONTH_NUM[month_name], day)
                if d < today:
                    mode = "past"
                elif d > today:
                    mode = "future"
                else:
                    mode = "today"
                return {"start": d, "end": d, "mode": mode}
            except ValueError:
                pass

        #  AY + GÜN (TERS SIRA) — ocak 15 / ocakta 15
        reverse_match = re.search(
            r"\b(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\s+(\d{1,2})\b",
            msg
        )
        if reverse_match:
            month_name = reverse_match.group(1)
            day = int(reverse_match.group(2))

            MONTH_NUM = {
                "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
                "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8,
                "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12
            }

            try:
                d = date(current_year, MONTH_NUM[month_name], day)
                if d < today:
                    mode = "past"
                elif d > today:
                    mode = "future"
                else:
                    mode = "today"
                return {"start": d, "end": d, "mode": mode}
            except ValueError:
                pass
        
        # 2️⃣ BU / BU HAFTA + GÜN
        is_this_week = any(p in msg for p in BU_WEEK_DAY_PREFIXES)

        for variant, weekday_idx in DAY_VARIANT_MAP.items():
            if variant in msg and is_this_week:
                base_monday = today - timedelta(days=today.weekday())
                target = base_monday + timedelta(days=weekday_idx)

                # bu hafta denmiş ama gün geçmişse → GEÇMİŞ
                mode = (
                    "today" if target == today
                    else "future" if target > today
                    else "past"
                )

                return {"start": target, "end": target, "mode": mode}
        
        is_past_query = any(k in msg for k in [
            "calisti", "calismis", "ofisteydi", "geldi", "oldu", "yapildi","evdeydi","uzaktan çalıştı","remote","calıstı"
        ])

        is_future_query = any(k in msg for k in [
            "calisacak", "gelecek", "olacak", "olucak",
            "bulunacak", "bulunucak", "gelicek", "çalisacak","isaretlemis"
        ])

        is_present_query = any(k in msg for k in [
            "calisiyor", "çalışıyor",
            "nerede", "nerden","nerde","nrde","isaretlemis"
        ])
        has_person = bool(
            self.detect_person_prescan(message)
            or self.has_person_in_db(message)
        )
        if (
            has_person 
            and (is_present_query or has_question_particle)
            and not is_past_query
            and not is_future_query
            and not has_day_name
            and not has_month_name
            and not has_day_number
        ):
            return {
                "start": today,
                "end": today,
                "mode": "today"
            }

        # HAFTAYA + GÜN
        if "haftaya" in msg or "gelecek hafta" in msg:
            for variant, weekday_idx in DAY_VARIANT_MAP.items():
                if variant in msg:
                    base_monday = today - timedelta(days=today.weekday())
                    target = base_monday + timedelta(days=7 + weekday_idx)

                    #  güvenlik: 14 günden ileri gitmesin
                    if (target - today).days > 14:
                        target = base_monday + timedelta(days=7)

                    return {"start": target, "end": target, "mode": "future"}

        
        print("🧪 [DATE PARSER] NO MATCH → None")


        return {"start": None, "end": None, "mode": None}

    def format_workforce_day_label(self, target_date: date, today: date):
        days = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]
        day_name = days[target_date.weekday()]

        if target_date == today:
            prefix = "Bugün"
        elif target_date == today + timedelta(days=1):
            prefix = "Yarın"
        else:
            prefix = day_name

        return f"{prefix} ({target_date.strftime('%d.%m.%Y')} {day_name})"

    def is_workforce_period_query(self, msg_norm: str, date_info: dict):
        """
        Workforce için PERIOD sorgusu mu?
        Eğer PERIOD ise → (True, start, end)
        Değilse        → (False, None, None)
        """
        today = date.today()
        #  GÜN VARSA → ASLA PERIOD DEĞİL
        if any(d in msg_norm for d in ALL_WEEKDAY_VARIANTS):
            return False, None, None

        if re.search(r"\b\d{1,2}\b", msg_norm):  # 6, 7, 15 ocak
            return False, None, None
        
        #  BU HAFTA
        if any(k in msg_norm for k in THIS_WEEK_KEYS):
            monday = today - timedelta(days=today.weekday())
            friday = monday + timedelta(days=4)
            return True, monday, friday

        # GEÇEN HAFTA
        if any(k in msg_norm for k in PAST_WEEK_KEYS):
            last_monday = today - timedelta(days=today.weekday() + 7)
            return True, last_monday, last_monday + timedelta(days=4)

        #  BU AY
        if any(k in msg_norm for k in THIS_MONTH_KEYS):
            start = today.replace(day=1)
            end_day = calendar.monthrange(today.year, today.month)[1]
            return True, start, today.replace(day=end_day)

        #  GEÇEN AY
        if any(k in msg_norm for k in PAST_MONTH_KEYS):
            first_this_month = today.replace(day=1)
            last_month_end = first_this_month - timedelta(days=1)
            start = last_month_end.replace(day=1)
            return True, start, last_month_end

        #  AY ADI (ocak, şubat, …) – GÜN YOKSA
        for raw, normalized in AY_NORMALIZE.items():
            if raw in msg_norm or normalized in msg_norm:
                month_map = {
                    "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
                    "mayıs": 5, "haziran": 6, "temmuz": 7,
                    "ağustos": 8, "eylül": 9, "ekim": 10,
                    "kasım": 11, "aralık": 12
                }
                m = month_map.get(normalized)
                if m:
                    start = date(today.year, m, 1)
                    end = date(today.year, m, calendar.monthrange(today.year, m)[1])
                    return True, start, end

        #  PERIOD DEĞİL none dönmeli
        return False, None, None

    def handle_workforce_period_summary(self, user_message, start, end, msg_norm):

        if not start or not end:
            return "Bu tarih aralığını net anlayamadım."

        period_label = f"{start.strftime('%d.%m.%Y')} – {end.strftime('%d.%m.%Y')}"

        work_type = self.detect_work_type(user_message)
        # KULLANICIYA GÖSTERİLECEK LABEL
        if work_type == "Ofis":
            label = "ofiste"
        elif work_type == "Home":
            label = "evden"
        elif work_type == "Bayi":
            label = "sahada"
        elif work_type == "Izin":
            label = "izinli"
        else:
            label = "şirkette"   

        conn = _mysql_conn()
        cursor = conn.cursor()

        if work_type is None:
            #  Kullanıcı çalışma tipi söylememiş → TÜM KAYITLAR
            cursor.execute("""
                SELECT COUNT(DISTINCT users1_id)
                FROM ofis_gunleri
                WHERE selected_date BETWEEN %s AND %s
            """, (start, end))

        elif work_type == "Izin":
            cursor.execute("""
                SELECT COUNT(DISTINCT users1_id)
                FROM ofis_gunleri
                WHERE selected_date BETWEEN %s AND %s
                AND (ofis_bayi IS NULL OR ofis_bayi = '')
            """, (start, end))

        else:
            #  Ofis / Home / Bayi
            cursor.execute("""
                SELECT COUNT(DISTINCT users1_id)
                FROM ofis_gunleri
                WHERE selected_date BETWEEN %s AND %s
                AND ofis_bayi = %s
            """, (start, end, work_type))

        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

    
        return (
            f"📅 <b>{period_label}</b> aralığında {label} olan çalışanlar "
            f"günlere göre değişiklik gösteriyor.<br>"
            f"<b>Özet:</b><br>"
            f"• Bu dönemde toplam <b>{count}</b> farklı çalışan en az bir gün {label} bulunmuş.<br>"
            f"<br>"
            f"📆 Gün bazında görmek ister misin?<br>"
            f"Örnekler:<br>"
            f"• “ocak ayı pazartesi kimler ofiste”<br>"
            f"• “cuma kimler ofiste”"
        )


    #şirkete bugün kaç kişi gelicek yada isim bugün ofistemi olucak?
