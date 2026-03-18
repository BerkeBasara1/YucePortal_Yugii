from .shared import *


class BrainBaseMixin:
    _INSTANCE = None

    #ilk çağtıda class yarat, diğer çağrılarda aynı nesneyi döndür
    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        # Yeni OpenAI client (v1.x uyumlu))
        self.client = _build_openai_client()

        # Prompt'ı yükle
        self.base_prompt = self._load_prompt()
        
        self.cities = cities 
        self.general_assistant = GeneralAssistant()
        self.people_field_roots = self._build_people_field_roots()
        self._dealer_cache = None
        self._dealer_cache_time = None

    def _oracle_conn(self):
        try:
            username = "USR_YUCE_PWR"
            password = "vJ9Q3BpH01"
            host = "10.113.197.4"
            port = 1521
            service_name = "DOTODWHDBP1"

            dsn = f"{host}:{port}/{service_name}"

            conn = oracledb.connect(
                user=username,
                password=password,
                dsn=dsn
            )

            return conn

        except Exception as e:
            print(f"❌ Oracle bağlantı hatası: {e}")
            return None
        
    def _load_prompt(self):
        """Asistanın kişiliğini içeren dosyayı okur."""
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print("Prompt dosyası okunamadı:", e)
            return "Sen bir şirkete ait chatbot'sun."
        
    # NORMALIZE PROXY METHODS- normalize.py den çağırmak için
    def normalize_people_text(self, text: str) -> str:
        return nrm.normalize_people_text(text)

    def normalize_calendar_text(self, text: str) -> str:
        return nrm.normalize_calendar_text(text)

    def normalize_intent_text(self, text: str) -> str:
        return nrm.normalize_intent_text(text)

    def normalize_field_name(self, field: str) -> str:
        return nrm.normalize_field_name(field)

    def normalize_people_name_token(self, token: str) -> str:
        return nrm.normalize_people_name_token(token)

    def normalize_department_suffixes(self, text: str) -> str:
        return nrm.normalize_department_suffixes(text)
    
    def normalize_month_with_suffixes(self, text: str) -> str:
        return nrm.normalize_month_with_suffixes(text)

    def format_date_with_day(self, date_obj):
        return nrm.format_date_with_day(date_obj)
    
    def fuzzy_match(self, word, options, threshold=0.75):
        return nrm.fuzzy_match(word, options, threshold)

    def fuzzy_match_in_text(self, msg: str, keywords: list, threshold=0.75) -> bool:
        return nrm.fuzzy_match_in_text(msg, keywords, threshold)

    def auto_log_sql(self, sql: str, params=None):
        
        logger = YugiiLogger.get_instance()

        # buffer varsa oraya ekle
        if hasattr(self, "_db_query_buffer"):
            self._db_query_buffer.append({
                "sql": sql,
                "params": params
            })

        logger.log_db_query(sql, params)


    def ask_gpt(self, user_message: str) -> str:
        """
        SADECE smalltalk ve yönlendirme için kullanılır.
        İşlem yapmaz, uydurmaz, yönlendirme yapmaz.
        """
        if self.client is None:
            return "Biraz daha detay verirsen daha net yardımcı olabilirim."

        SMALLTALK_GUARD_PROMPT = """
            ROLE:
            You are Yüce Auto’s corporate digital assistant.
            This call is ONLY for light conversation and soft responses.
            
            OUTPUT LANGUAGE:
            - ALL user-facing responses MUST be in Turkish.
            
            STRICT RULES (VERY IMPORTANT):
            - NEVER perform any action.
            - NEVER imply that an action was or will be performed.
            - NEVER describe any process or ongoing work.
            - NEVER use technical terms (backend, system, portal, database, API, vb.).
            - NEVER say “I don’t understand” or similar phrases.
            - NEVER invent, assume, or infer information.
            - NEVER use future tense or imply future actions.
            - Responses must be 1–2 short sentences only.

            IDENTITY / CAPABILITY RULE (MANDATORY):

            If the user asks about:
            - what you do
            - your purpose
            - your role
            - what you are
            - your capabilities
            - your mission

            You MUST respond ONLY with this exact sentence in Turkish:

            "Ben Yüce Auto’nun kurumsal dijital asistanı Yugii’yim. Otopark rezervasyonu, haftalık takvim, çalışan bilgileri ve portal işlemlerinde yardımcı olurum."

            - Do NOT add anything.
            - Do NOT rephrase.
            - Do NOT extend.
            - Do NOT invent features.

            GREETING-ONLY CASE (CRITICAL):
            - If the user message contains ONLY a greeting
            (e.g. “selam”, “merhaba”, “naber”, “nasılsın”):
                → Respond with a short greeting only.
                → NEVER ask follow-up questions.
                → NEVER say phrases like
                “detay verir misin” or
                “nasıl yardımcı olabilirim”.
            
            - If a greeting is combined WITH a request
            (e.g. “merhaba yarın park ayır”):
                → Ignore the greeting.
                → Handle the request normally.
            
            VAGUE OR GENERAL REQUESTS:
            - Respond politely and conversationally.
            - You MAY ask for clarification ONLY if the user actually made a request.
            - In that case, you MAY say:
            “Biraz daha detay verirsen daha net yardımcı olabilirim.”
            
            UNSUPPORTED REQUESTS:
            - Politely set a boundary.
            - Say:
            “Bu konuda şu an yardımcı olamıyorum ama başka bir şey sorabilirsin.”
            
            CASUAL CONVERSATION:
            - Keep responses natural, short, and corporate.
            - Light humor is allowed.
            - NEVER invent information.
            
            IMPORTANT – STRICT BEHAVIOR RULE (MANDATORY):
            - Asla aksiyon veya süreç anlatma.
            - “kontrol ediyorum”, “bakıyorum”, “inceleyip döneceğim”, “bekle” gibi ifadeler KULLANMA.
            - Yapılan veya yapılacak bir eylemi ima etme.
            - İç işleyiş, bekleme, kontrol, işlem ifadeleri kullanma.
            - Yalnızca:
            • NET bir SONUÇ cümlesi
            • veya NET bir AÇIKLAMA / EKSİK BİLGİ sorusu üret.
            
            EXAMPLE TONES (REFERENCE ONLY):
            - “Güzel bir soru 😊 Biraz daha açarsan daha net yardımcı olabilirim.”
            - “Bu konuda şu an yardımcı olamıyorum ama başka bir şey sorabilirsin.”
            - “Rica ederim 😊 Yardımcı olabildiysem ne mutlu.”
            """


        try:
            system_prompt = (
                self.base_prompt.strip()
                + "\n\n"
                + SMALLTALK_GUARD_PROMPT.strip()
            )

            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.4,   
                max_tokens=120
            )

            reply = response.choices[0].message.content.strip()
            reply_lower = reply.lower()

            FORBIDDEN = [
                "yapılacak", "yapılacaktır",
                "iletilecek", "iletildi",
                "backend", "sistem", "portal",
                "ilgili birim", "yönlendiriyorum",
                "işlem yapılacak", "işleme alınacak"
            ]

            if any(x in reply_lower for x in FORBIDDEN):
                return "Ne yapmak istediğini tam anlayamadım. Biraz daha detay yazar mısın?"

            return reply

        except Exception as e:
            print("GPT hata:", e)
            return (
                "Şu anda bu isteğe yanıt veremiyorum. "
                "Biraz daha net ifade edebilir misin?"
            )
        
    #REPUTATION HELPERS
    def fuzzy_contains(self, text, phrase, threshold=80):
        return fuzz.partial_ratio(text, phrase) >= threshold

    def root_match(self, text, root):
        if self.fuzzy_contains(text, root):
            return True
        if self.fuzzy_contains(text.replace(" ", ""), root.replace(" ", "")):
            return True
        return False
    
    #kur bilgisi
    def get_currency_rates(self):
        import requests
        import xml.etree.ElementTree as ET

        url = "https://www.tcmb.gov.tr/kurlar/today.xml"
        r = requests.get(url, timeout=5)
        r.raise_for_status()

        root = ET.fromstring(r.content)
        tarih = root.attrib.get("Tarih", "")

        rates = {}
        for currency in root.findall("Currency"):
            code = currency.get("CurrencyCode")
            if code in ["USD", "EUR"]:
                value = currency.find("ForexSelling").text.replace(",", ".")
                rates[code] = float(value)

        return rates, tarih
    
    def _format_currency_result(self, amount, from_unit, total, to_unit, rate_used, tarih):
        return (
            "💱 Döviz Dönüşümü<br>"
            f"{amount:,.2f} {from_unit} karşılığı "
            f"<b>{total:,.2f} {to_unit}</b><br>"
            f"<small>(1 {from_unit} = {rate_used:,.2f} TL)</small><br>"
            f"<small>{tarih} tarihli TCMB satış kuru baz alınmıştır.</small>"
        )

    def handle_currency_calculation(self, user_message: str):

        msg = self.normalize_people_text(user_message)

        # --- Tutar ---
        match = re.search(r"\d+[.,]?\d*", msg)
        if not match:
            return "Hesaplama için tutar belirtmelisin."

        amount = float(match.group().replace(",", "."))

        # --- Para Birimleri ---
        found_units = re.findall(r"(dolar|usd|euro|eur|tl|try)", msg)

        if len(found_units) < 2:
            return "Dönüştürmek istediğin iki para birimini belirtmelisin."

        unit_map = {
            "dolar": "USD",
            "usd": "USD",
            "euro": "EUR",
            "eur": "EUR",
            "tl": "TL",
            "try": "TL"
        }

        source = unit_map.get(found_units[0])
        target = unit_map.get(found_units[1])

        if source == target:
            return "Aynı para birimi arasında dönüşüm yapılamaz."

        try:
            rates, tarih = self.get_currency_rates()

            usd = rates.get("USD")
            eur = rates.get("EUR")

            if not usd or not eur:
                return "Kur bilgisi alınamadı."

            # --- TL bazına çevir ---
            if source == "USD":
                tl_amount = amount * usd
                rate_used = usd
            elif source == "EUR":
                tl_amount = amount * eur
                rate_used = eur
            elif source == "TL":
                tl_amount = amount
                rate_used = 1
            else:
                return "Desteklenmeyen para birimi."

            # --- TL'den hedefe ---
            if target == "USD":
                total = tl_amount / usd
            elif target == "EUR":
                total = tl_amount / eur
            elif target == "TL":
                total = tl_amount
            else:
                return "Desteklenmeyen para birimi."

            return self._format_currency_result(
                amount, source, total, target, rate_used, tarih
            )

        except Exception as e:
            print("❌ Döviz hesaplama hata:", e)
            return "⚠️ Hesaplama şu an yapılamıyor."
    
    #kur modülü
    def handle_currency_rate(self):
        try:
            rates, tarih = self.get_currency_rates()

            dolar = rates.get("USD")
            euro = rates.get("EUR")

            if not dolar or not euro:
                return "⚠️ Döviz kuru bilgisi alınamıyor."

            return (
                "💱 Güncel Döviz Kurları<br>"
                f"💵 1 USD = <b>{dolar:,.2f} TL</b><br>"
                f"💶 1 EUR = <b>{euro:,.2f} TL</b><br>"
                f"<small>TCMB tarafından yayımlanan son geçerli kur "
                f"({tarih}) baz alınmıştır.</small>"
            )

        except Exception as e:
            print("❌ Döviz API hata:", e)
            return "⚠️ Döviz kuru bilgisi geçici olarak alınamıyor."
    
