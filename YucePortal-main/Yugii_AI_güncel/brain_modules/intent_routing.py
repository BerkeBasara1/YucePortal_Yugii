from .shared import *


class IntentRoutingMixin:
    def detect_main_intent(self, user_message: str, signals: dict) -> str:

        print("\n🧪 [TEST] detect_main_intent INPUT:", user_message)

        msg = self.normalize_people_text(user_message)
        print("INTENT TEST MSG:", msg)

        #sinyal tanımlama
        has_date = signals.get("has_date")


        
        COMPANY_TERMS = [
            "yuce auto","yuce oto","skoda","sirket","firma","marka","yuceauto","skoda yüce auto","yüce auto","şirketimiz","şirketttimiz","yuce autonun","yuce autodaki","yuce auto'daki",
        ]

        is_company_question = any(t in msg for t in COMPANY_TERMS)

        has_person = bool(
            not is_company_question   #  KRİTİK
            and (
                session.get("detected_persons")
                or self.has_person_in_db(user_message)
            )
        )
        msg_norm = self.normalize_people_text(user_message)

        if (
            any(k in msg_norm for k in KIM_YAPTI_SORUSU)
            and not any(x in msg_norm for x in [   "komik", "saka", "espri", "eglendir", "guldur", "moral"
            ])
        ):
            return "Beni Yüce Auto’nun IT ekibinden Sude Bayhan geliştirdi 🙂"

        CAPABILITY_PATTERNS = [
            r"\bne\s+is\s+yap",
            r"\bne\s+yap",
            r"\bneler\s+yap",
            r"\bne\s+ise\s+yar",
            r"\bamac",
            r"\bgorev",
            r"\byetenek",
            r"\bkabiliyet",
            r"\bmisyon",
            r"\brol",
            r"\bne\s+icin\s+var",
            r"\bneden\s+burda",
            r"\bneden\s+buradasin",
            r"\bsen\s+nesin",
            r"\bsenin\s+is",
            r"\bbu\s+sistem\s+ne\s+yap",
        ]

        if any(re.search(p, msg) for p in CAPABILITY_PATTERNS):
            return "assistant_capabilities"

        # --- ROOT FALLBACK (yazım hatalı yakalama) ---
        tokens = msg.split()

        if any(t.startswith(("amac", "gorev", "yetenek", "kabiliyet")) for t in tokens):
            return "assistant_capabilities"

        if (
            "ne" in tokens and
            (
                any(t.startswith("yap") for t in tokens) or
                "ise" in tokens and any(t.startswith("yar") for t in tokens)
            )
        ):
            return "assistant_capabilities"

        if (
            "bu ve gecen ay analiz raporu hazirla" in msg_norm
        ):
            return "monthly_trend_analysis"

        for k in FUN_REQUEST_KEYWORDS:
            score = fuzz.partial_ratio(msg, k)
            if score >= 90:
                print(f"🧠 [INTENT]: fun_request (fuzzy={score})")
                return "fun_request"
            

        # BUGÜN / GÜN SORGUSU (SADECE NET KALIPLAR)
        for k in TODAY_DAY_KEYS:
            if k in msg:
                print("🧠 [INTENT]: today_day")
                return "today_day"

        #  YÜCE AUTO – REPUTATION (HELP’TEN önce)
        if (
            not any(h in msg for h in EXPORT_HINTS)
            and not self.contains_department_word(msg)
            and not self.detect_work_type(user_message)   
            and not self.has_work_history_count_signal(msg)  
            and any(self.root_match(msg, root) for root in YUCE_AUTO_REPUTATION_ROOTS)
            and any(self.fuzzy_contains(msg, q) for q in YUCE_AUTO_REPUTATION_QUESTIONS)
        ):
            return "yuce_auto_reputation"
        
        #  PORTAL LINK INTENT (SADECE NET SAYFA / LİNK İSTEĞİ)
        if (
            any(h in msg for h in PORTAL_LINK_STRONG_HINTS)
            and (
                any(v in msg for v in PORTAL_LINK_VERBS)
                or "link" in msg
                or "sayfa" in msg
            )
            #  BİLGİ SORULARINI ELEYELİM
            and not any(k in msg for k in [
                "kaç", "kac", "sayısı", "sayisi","departmnlar",
                "nelerdir", "neler", "çeşitleri",
                "departman", "departmanlar"
            ])
        ):
            return "portal_link"
        

        
        #şarj rezervasyon için
        norm = self.normalize_people_text(user_message)

        if (
            self.fuzzy_match_in_text(norm, CHARGE_ROOTS, 0.75)
            and self.fuzzy_match_in_text(norm, CHARGE_ACTIONS, 0.75)
        ):
            return "charge_reservation"
        
        #  CURRENCY CALCULATION (currency_rate'ten önce!)
        if self.detect_currency_calculation(user_message):
            print("🧠 [INTENT]: currency_calculation")
            return "currency_calculation"
        
        
        #  DÖVİZ KURU INTENT (HELP'ten sonra olmalı)
        if any(k in msg for k in CURRENCY_KEYWORDS):
            print("🧠 [INTENT]: currency_rate")
            return "currency_rate"

        #  GENEL SOHBET / MUHABBET (PERSON OLMASIN)
        GENERAL_CHAT_KEYS = [
            "onerin var mi",
            "oneri var mi",
            "tavsiyen var mi",
            "bir fikrin var mi",
            "ne dersin",
            "sence",
            "ne dusunuyorsun"
        ]

        if (
            any(k in msg for k in GENERAL_CHAT_KEYS)
            and not any(c in msg for c in YUCE_AUTO_REPUTATION_ROOTS)
        ):
            print("🧠 [INTENT]: smalltalk (general)")
            return None
        
        #  YÜCE PORTAL BİLGİ INTENT

        PORTAL_KEYWORDS = [
            "yuceportal", "yüceportal",
            "yuce portal", "yüce portal",
            "portal"
        ]

        PORTAL_INFO_TRIGGERS = [
            "nedir","ne","nedır","ne için var"
            "ne ise yarar","nedir","ne","nedır","ne için var",
            "ne ise yarar","ne","ndr",
            "ne işe yarar",
            "neler yapilir",
            "neler yapılir",
            "neler yapilir",
            "ne yapilir",
            "ne yapilir",
            "ne var",
            "bilgi"
        ]
        if (
            not self.contains_department_word(msg)   #
            and any(p in msg for p in PORTAL_KEYWORDS)
            and any(t in msg for t in PORTAL_INFO_TRIGGERS)
        ):
            return "portal_info"

        #  OTOPARK CONTEXT FLAG  
        has_park = any(k in msg for k in OTOPARK_KEY)
        has_availability = any(k in msg for k in PARK_AVAILABILITY_KEYWORDS)
        has_user_status = any(k in msg for k in USER_PARK_STATUS_KEYS)


        if has_availability and has_date and not has_park:
            print("🧠 [INTENT]: otopark_status (implicit)")
            return "otopark_status"
        
        if (
            has_park
            and has_availability
            and not has_user_status
        ):
            print("🧠 [INTENT]: otopark_status (availability)")
            return "otopark_status"
        
        #  OTOPARK INTENT (TEK VE NET BLOK)
        if has_park and any(k in msg for k in CANCEL_KEYS):
            print("🧠 [INTENT]: otopark_cancel")
            return "otopark_cancel"
        
        if (
            has_park
            and any(k in msg for k in USER_PARK_STATUS_KEYS)
            and not any(k in msg for k in PARK_CREATE_ACTION_VERBS)
        ):
            print("🧠 [INTENT]: otopark_status_user")
            return "otopark_status_user"

        
        #  CREATE otopark
        if (
            has_park
            and any(k in msg for k in PARK_CREATE_ACTION_VERBS)
            and not any(k in msg for k in USER_PARK_STATUS_KEYS)
        ):
            print("🧠 [INTENT]: otopark_create")
            return "otopark_create"

        #  WEATHER INTENT 
        if (
            (
                any(k in msg for k in WEATHER_KEYWORDS)
                or self.fuzzy_match_in_text(msg, WEATHER_KEYWORDS, 0.80)
            )
            and not any(k in msg for k in OTOPARK_KEY)
            and not self.detect_work_type(user_message)
        ):
            print("🧠 [INTENT]: weather")
            return "weather"
        
        HELP_KEYS_NORM = [self.normalize_people_text(h) for h in HELP_ACTION_KEYS]

        has_help_keyword = any(h in msg for h in HELP_KEYS_NORM)

        has_module_signal = any([
            any(k in msg for k in OTOPARK_KEY),
            "takvim" in msg,
            self.detect_work_type(user_message),
            self.extract_department_name(user_message),
            self.has_people_field_request(user_message),
        ])

        if has_help_keyword and has_module_signal:
            return "help"
        
        has_department = self.extract_department_name(user_message) is not None

        def _has_cancel_intent_local(msg: str) -> bool:
            msg = self.normalize_people_text(msg)
            for w in CANCEL_KEYS:
                # 🔒 SADECE TAM KELİME
                if re.search(rf"\b{re.escape(w)}\b", msg):
                    return True
            return False
        
        has_cancel =_has_cancel_intent_local(msg)

        has_any_context = any(k in msg for k in (
            OTOPARK_KEY
            + ["takvim", "haftalik", "haftalık"]
        ))

        if has_department :
            has_cancel = False

        if has_cancel and not has_any_context and not has_date:
            print("🧠 [INTENT]: cancel_without_context")
            return "cancel_without_context"
        
        # FALLBACK: OTOPARK GPT (SADECE HİÇBİR RULE TUTMADIYSA)

        if any(p in msg for p in ["park", "otopark", "rezervasyon","park yeri","prk","otoprk","rez","rezervsyn","yer ayır"]):
            print("🟡 [INTENT]: fallback → GPT otopark intent")

            if self.client is None:
                if any(k in msg for k in CANCEL_KEYS):
                    return "otopark_cancel"
                if any(k in msg for k in USER_PARK_STATUS_KEYS):
                    return "otopark_status_user"
                if any(k in msg for k in PARK_AVAILABILITY_KEYWORDS):
                    return "otopark_status"
                return "otopark_create"

            prompt = f"""
            Aşağıdaki kullanıcı mesajından otopark niyetini tespit et.

            Kurallar:
            - Kullanıcı KENDİ rezervasyonunu soruyorsa → otopark_status_user
            - Genel müsaitlik soruyorsa → otopark_status
            - Ayırma / rezerve → otopark_create
            - İptal → otopark_cancel
            - Emin değilsen → none

            Kullanıcı mesajı:
            "{user_message}"

            Sadece şu seçeneklerden biriyle cevap ver:
            - otopark_create
            - otopark_cancel
            - otopark_status
            - otopark_status_user
            - none
            """

            try:
                resp = self.client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "system", "content": prompt}],
                    max_tokens=5,
                    temperature=0
                )
                intent = resp.choices[0].message.content.strip().lower()
                print("🧠 [GPT FALLBACK INTENT]:", intent)
                return intent
            except Exception as e:
                print("❌ GPT fallback hata:", e)

    def is_company_only(self, text: str) -> bool:
        text = self.normalize_people_text(text)
        COMPANY_ROOTS = [
            "yuce auto",
            "yuce oto",
            "skoda",
            "škoda"
        ]
        if any(k in text for k in COMPANY_ROOTS) and not any(p in text for p in PERSONEL_KEY):
            return True

        return False

    def route_company_reputation(self, text: str):
        text_norm = self.normalize_people_text(text)

        # YÜCE AUTO
        if any(k in text_norm for k in [
            "yuce auto","yuce oto","yuce"
        ]):
            return self.handle_yuce_auto_reputation()

        # SKODA
        if any(k in text_norm for k in [
            "skoda","škoda"
        ]):
            return self.handle_skoda_reputation()

        return None
    def has_person_in_db(self, text: str) -> bool:
        text_norm = self.normalize_people_text(text)
        BLOCKED_SURNAME_ONLY = {"yuce"}
        if (
            any(t in text_norm for t in YUCE_AUTO_REPUTATION_ROOTS)
            and any(q in text_norm for q in YUCE_AUTO_REPUTATION_QUESTIONS)
        ):
            return False
        
        tokens = text_norm.split()

        conn = _mysql_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT LOWER(name) AS name, LOWER(surname) AS surname
            FROM users1
            WHERE is_active = 1
        """)
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        # 1️⃣ AD + SOYAD (en net durum)
        for u in users:
            full = f"{u['name']} {u['surname']}"
            if full in text_norm:
                return True

        #  TEK İSİM (DB’de GERÇEKTEN unique mi?)
        name_hits = [u for u in users if u["name"] in tokens]

        if len(name_hits) == 1:
            return True          

        if len(name_hits) > 1:
            return False         

        # 3 TEK SOYİSİM (DB’de GERÇEKTEN unique mi?)
        surname_hits = [u for u in users if u["surname"] in tokens]

        if any(s in BLOCKED_SURNAME_ONLY for s in tokens):
            return False

        if len(surname_hits) == 1:
            return True

        if len(surname_hits) > 1:
            return False

        return False

    def looks_like_company_people(self, msg: str) -> bool:

        if not msg:
            return False
        
        
        text = self.normalize_people_text(msg)
        
        #  asistan / smalltalk (hard stop)
        if text in {
            "naber", "naberr", "naberrr",
            "selam", "selamlar",
            "merhaba", "mrb", "slm", "hey", "hi", "hello",
            "nasilsin", "nasılsın", "nasil", "nası",
            "iyi misin", "ne haber", "ne var ne yok",
            "napıyorsun", "napiyorsun", "ne yapıyorsun",
             "nbr"
        }:
            return False

        #diğer modüller (hard stop)
        blacklist = [
            "otopark", "park", "rezervasyon", "takvim", "yemek", "menu",
            "onerin", "oneri", "tavsiye", "fikrin","hakkında"
        ]        
        if any(b in text for b in blacklist):
            return False

        #  DB'DEN İSİM BULUNUYORSA → DİREKT GİR
        try:
            persons = self.has_person_in_db(msg)
            if persons:
                return True
        except Exception:
            pass

        # Alan kelimeleri (RAW_FIELD_KEYWORDS'tan)
        field_keywords = []
        for kws in RAW_FIELD_KEYWORDS.values():
            field_keywords.extend(kws)

        field_keywords = [self.normalize_people_text(k) for k in field_keywords]
        has_field = any(k in text for k in field_keywords)

        # Kişi niyeti (çok sınırlı, kontrollü)
        person_intent_keywords = [
            "kim", "kimin", "çalışan", "personel", "kişi","kişiler","çalışanlar","kimler","kişi", "kişiler","çalışan",   
            "ekip", "ekibi"
        ]
        has_person_intent = any(p in text for p in person_intent_keywords)

        if has_field and has_person_intent:
            return True

        #  HİÇBİRİ YOKSA → GİRME

        return False


    #akıcı şekilde akıllı gözükmesi için başına ve sonuna metin ekleme
