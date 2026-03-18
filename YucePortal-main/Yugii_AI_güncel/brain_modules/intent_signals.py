from .shared import *


class IntentSignalsMixin:
    def detect_bulk_people_context(self, msg: str) -> bool:
        msg = self.normalize_people_text(msg)

        if any(k in msg for k in ALL_PEOPLE_KEYWORDS):
            return True

        has_scope = any(w in msg for w in SCOPE_WORDS)
        has_people = any(w in msg for w in PEOPLE_WORDS)

        return has_scope and has_people
    
    #toplu company ile ilgili intent yönlendirme fonk
    def detect_business_intent(self, user_message: str, signals: dict) -> str | None:
        """
        İş domain karar motoru (DETAYLI vce GÜVENLİ)

        """

        # SIGNALS (TEK KAYNAK)
        has_date = signals["has_date"]
        has_question = signals["has_question"]
        has_work_type = signals["has_work_type"]
        has_person = signals["has_person"]
        has_department = signals["has_department"]
        has_export = signals["has_export"]
        has_history = signals["has_history"]
        has_people_field = signals["has_people_field"]
        has_bulk_people = signals.get("has_bulk_people_context")

        msg = self.normalize_people_text(user_message)

        
        # OTOPARK VARSA ASLA WORKFORCE'A GİRME
        if any(k in self.normalize_people_text(user_message) for k in OTOPARK_KEY):
            return None
        #  PORTAL LINK INTENT (SADECE NET NAVİGASYON / SAYFA İSTEĞİ)
        is_link_action = (
            any(v in msg for v in PORTAL_LINK_VERBS)
            or "link" in msg
            or "sayfa" in msg
            or "sayfası" in msg
            or "sayfasını" in msg
            or "syfa" in msg
        )

        is_information_query = any(k in msg for k in [
            "kaç", "kac", "sayısı", "sayisi",
            "nelerdir", "neler", "çeşitleri",
            "departman", "departmanlar", "departmanı",
            "departmanındaki", "departmanındakiler",
            "departmanındakilerin",
            "kim", "kimler", 
        ])

        if (
            any(h in msg for h in PORTAL_LINK_STRONG_HINTS)
            and is_link_action
            and not is_information_query
        ):
            return "portal_link"
        has_calendar_action = any(f in msg for f in self.TAKVİM_KEYS)

        LOCATION_QUESTION_WORDS = [
            "nerede", "nerde","ofiste","şirkette","evde","dışardan",
            "nereden", "nerden",
            "nereye","ofiste","ofis", "şirkette","şirket", "uzaktan","home", "bayide","bayi",
            "nerelerde", "nerdeler",
            "nerdeydi", "nerdeymis", "nerdeymiş","kimler var","kmler var"
        ]

        has_location_context = any(k in msg for k in LOCATION_QUESTION_WORDS)
        WEATHER_KEYWORDS = [
            "hava", "hava durumu", "sicaklik",
            "yagmur", "kar", "ruzgar",
            "gunesli", "bulutlu", "soguk", "sicak","otopark"
        ]

        if any(k in msg for k in WEATHER_KEYWORDS):
            return None
        
        has_month_word = any(
            re.search(rf"\b{m}\b", msg)
            for m in AY_NORMALIZE.values()
        )
        
        has_export = (
            any(k in msg for k in EXPORT_HINTS)
            and any(k in msg for k in ["excel", "exel"])
        )
        has_count = any(k in msg for k in PEOPLE_COUNT_KEYS)
        has_people_word = any(
            f" {k} " in f" {msg} "
            for k in PERSONEL_KEY
        )
        
        ALL_RELATIVE_DAYS = (
            RELATIVE_DAY_TRIGGERS["today"]
            + RELATIVE_DAY_TRIGGERS["tomorrow"]
            + RELATIVE_DAY_TRIGGERS["yesterday"]
        )

        has_numeric_date2 = bool(
            re.search(r"\b\d{1,2}\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\b", msg)
        )

        has_real_day = (
            any(re.search(rf"\b{d}\b", msg) for d in ALL_WEEKDAY_VARIANTS)
            or any(re.search(rf"\b{r}\b", msg) for r in ALL_RELATIVE_DAYS)
            or has_numeric_date2
            or has_month_word
        )

        has_department_context = any(
            re.search(rf"\b{root}(ler|lar)?\b", msg)
            for root in DEPARTMENT_WORD_VARIANTS
        )
        BAYI_ROOTS = [
            "bayiler",
            "servis", "servisler", "servisleri",
            "satış servisi", "satis servisi",
        ]

        COUNT_HINTS = [
            "kaç", "kac",
            "adet", "adeti",
            "sayısı", "sayisi",
            "rakam", "liste", "listesi",
            "goster", "göster",
            "var"
        ]

        if (
            (
                "bayi" in msg
                and any(h in msg for h in COUNT_HINTS)
            )
            or any(root in msg for root in BAYI_ROOTS)
        ):
            return "bayi_about"
                
        if (
            any(k in msg for k in ["kaç", "kac", "sayısı", "sayisi"])
            and any(p in msg for p in ["çalışan", "calisan", "personel", "kisi", "kişi"])
            and not has_export
            and not has_real_day
            and not has_department
        ):
            return "people_count_only"
        
        SATIS_ROOTS = [
            "satış",
            "satis","satısı yapılan araba sayısı","araba sayısı"
            "satilan","arac satıldı","satıldı",
            "satılan","satıs oldu","satıs yapıldı",
        ]

        COUNT_ROOTS = [
            "kaç",
            "kac",
            "adet","ne kadar",
            "adedi","adeti","rakamı","rakam",
            "sayısı",
            "sayisi",
            "miktar","toplam satış",
            "toplam",
            "tüm","toplam kaç adet"
        ]
        # SATIŞ INTENT (daha akıllı)
        if (
            any(s in msg for s in SATIS_ROOTS)
            and any(c in msg for c in COUNT_ROOTS)
        ):
            return "satis_sayisi"
        
        print("DEBUG has_count:", has_count)
        print("DEBUG has_people_word:", has_people_word)
        print("DEBUG has_export:", has_export)
        print("DEBUG has_bulk_people:", has_bulk_people)

        #  WORK HISTORY (BEN)
        if (
            signals.get("has_work_history_intent")
            and signals.get("has_history_date")   #  AY / YIL / ARALIK
            and not signals.get("has_person")
            and not signals.get("has_department")
        ):
            return "work_history"

        #  HAFTALIK TAKVİM (EMİR) – PEOPLE FIELD DEĞİLSE
        if (
            self.detect_haftalik_takvim_intent(user_message)
            and not signals.get("has_people_field")
            and not signals.get("has_export")
        ):
            return "haftalik_takvim"
        
        has_department_word = any(k in msg for k in DEPARTMENT_WORD_VARIANTS)
        has_department_count = any(k in msg for k in DEPARTMENT_COUNT_HINTS)
        has_department_list = any(k in msg for k in DEPARTMENT_LIST_HINTS)

        # DEPARTMAN – COUNT vs LIST NET AYRIMI
        has_strict_department_count = (
            has_department_word
            and any(k in msg for k in DEPARTMENT_COUNT_HINTS)
            and not any(k in msg for k in DEPARTMENT_LIST_HINTS)
        )

        has_strict_department_list = (
            has_department_word
            and (
                any(k in msg for k in DEPARTMENT_LIST_HINTS)
                or "departmanlar" in msg
                or "isimleri" in msg
                or "çeşitleri" in msg
            )
        )
        #  WORKFORCE STATUS (KİM / NEREDE / KAÇ)
        if (
            has_date
            and signals.get("date_info")
            and signals["date_info"].get("start")
            and signals["date_info"]["start"].year > datetime.now().year + 1
            and any(k in msg for k in [
                "nasil olacak",
                "ne olacak",
                "modeli",
                "gelecekte",
                "ileride","ileride"
            ])
        ):
            return None
        if any(k in msg for k in PARK_AVAILABILITY_KEYWORDS):
            return None
        

        
        # FORCE WORKFORCE (GEÇMİŞ / BUGÜN / GELECEK)
        if (
            signals.get("has_department")
            and signals.get("has_date")
            and signals.get("has_work_type")
            and not has_calendar_action
            and not any(k in msg for k in EXPORT_HINTS)
        ):
            return "workforce_status"
        if (
            has_department
            and any(k in msg for k in PERSONEL_KEY)
            and not has_export
            and not has_people_field
            and not has_strict_department_list
            and not has_strict_department_count
            and not any(k in msg for k in EXPORT_HINTS)
        ):
            return "workforce_status"
        if (
            has_department
            and has_date
            and has_question
            and not has_export
            and not has_people_field
            and not has_strict_department_list
            and not has_strict_department_count
            and not any(k in msg for k in EXPORT_HINTS)
        ):
            return "workforce_status"
        
        # WORKFORCE STATUS
        if (
            (has_date or has_location_context)
            and (
                has_person
                or has_department
                or has_location_context
                
            )
            and (
                has_work_type
                or has_location_context
                or has_question
                or has_count
            )
            and not has_strict_department_list
            and not has_strict_department_count
            and not has_export
            and not has_calendar_action
            and not any(k in msg for k in EXPORT_HINTS)
        ):
            return "workforce_status"
        
        if (
            any(k in msg for k in EXPORT_HINTS)
            and not self.has_corporate_context(msg, has_bulk_people)
        ):
            return None   
        
        has_export_language = (
            any(e in msg for e in EXPORT_HINTS)
            or has_people_field   # mail / telefon / title
        )
        has_list_language = (
            any(p in msg for p in PERSONEL_KEY)
            or any(w in msg for w in WORKFORCE_LIST_KEYS)
        )
        #  PERSON / LIST → DIRECT EXPORT (SINGLE SOURCE OF TRUTH)
        if (
            # Kapsam: departman veya şirket geneli
            (
                has_department
                or has_bulk_people
                or signals.get("has_bulk_people_context")
                or signals.get("has_bulk_list_request")
            )

            # Liste / export dili
            and (
                has_list_language
                or has_export_language
            )

            and not any(k in msg for k in OTOPARK_KEY)
            and not has_strict_department_count
            and not has_real_day
        ):
            return "people_export"

        print("INTENT TEST MSG:", msg)


        #  COMPANY PEOPLE (KİŞİ / DEPARTMAN / ŞİRKET)
        has_people_intent = (
            has_person
            or (
                has_department
                and not signals.get("has_bulk_people_context")
            )
        )
        # TEK KİŞİ BİLGİSİ
        if (
            has_people_intent
            and not has_date
            and not has_work_type
            and not any(p in msg for p in PERSONEL_KEY)
        ):
            return "company_people"

        #  SADECE SAYI SORUSU
        if (
            has_strict_department_count
            and self.contains_department_word(user_message)
            and not has_date
            and not has_people_intent
        ):
            return "department_count"

        #  SADECE LİSTE / ÇEŞİT SORUSU
        if (
            has_strict_department_list
            and self.contains_department_word(user_message)
            and not has_date
            and not has_work_type
            and not has_people_intent
        ):
            return "department_list"
        
        return None
    
    def handle_people_count_only(self):
        conn = _mysql_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM users1
            WHERE is_active = 1
        """)
        self.auto_log_sql("""
            SELECT COUNT(*)
            FROM users1
            WHERE is_active = 1
        """, None)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return f"Şirkette toplam mevcut <b>{count}</b> aktif çalışan bulunuyor."

    #yeni ek detect main intetn fonksiyonu
    def extract_message_signals(self, user_message: str) -> dict:
        """
        Kullanıcı mesajından SADECE sinyal çıkarır.
        Intent, handler veya return kararı VERMEZ.
        """

        msg = self.normalize_people_text(user_message)
        msg_stripped = self._strip_tr_suffixes(msg)

        QUESTION_KEYWORDS = [
            "kim", "kimler","hangi kişiler","kç adt","sayısı","sayı ver","sayı",
            "kaç", "kac","kaç kişi","kaç tane","kaç adet","kaç olucak","kaç kişi",
            "var","nerede","nerde","nasıl","nasil",          
            "çalışıyor", "calisiyor","çalışıcak","nerde çalışıyor",
            "çalışıcak", "calisacak",
             "nasıl", "nasil","hangi", "hangileri", "nelerdir", "neler","kimler var"
        ]

        # TEMEL SİNYALLER
        has_calendar_action = any(f in msg for f in self.TAKVİM_KEYS)
        
        MONTH_KEYS = list(AY_NORMALIZE.values())
        
        has_numeric_date = bool(
            re.search(r"\b\d{1,2}\b", msg) and any(m in msg for m in MONTH_KEYS)
        ) or bool(
            re.search(r"\b20\d{2}\b", msg)   # yıl (2024, 2025…)
        )

        # Tarih sinyali (tek otorite)
        
        has_date = (
            any(
                re.search(rf"\b{re.escape(k)}\b", msg)
                for k in (
                    RELATIVE_DAY_TRIGGERS["today"]
                    + RELATIVE_DAY_TRIGGERS["tomorrow"]
                    + ALL_WEEKDAY_VARIANTS
                    + THIS_WEEK_KEYS
                    + NEXT_WEEK_KEYS
                    + THIS_MONTH_KEYS
                )
            )
            or any(re.search(rf"\b{re.escape(m)}\b", msg) for m in MONTH_KEYS)
            or has_numeric_date
        )

        has_explicit_date = (
            (
                any(
                    re.search(rf"\b{re.escape(k)}\b", msg)
                    for k in (
                        RELATIVE_DAY_TRIGGERS["today"]
                        + RELATIVE_DAY_TRIGGERS["tomorrow"]
                        + ALL_WEEKDAY_VARIANTS
                        + THIS_WEEK_KEYS
                        + NEXT_WEEK_KEYS
                        + THIS_MONTH_KEYS
                    )
                )
                or any(re.search(rf"\b{re.escape(m)}\b", msg) for m in MONTH_KEYS)
                or has_numeric_date
            )
            and not any(
                re.search(rf"\b{re.escape(m)}\b", msg)
                for m in WORKFORCE_COUNT_KEYS
            )
        )

        # Çalışma tipi (ofis / home / bayi / izin)
        work_type = self.detect_work_type(user_message)
        has_work_type = work_type is not None

        # Kişi (isim / soyisim)
        has_person = bool(
            self.detect_person_prescan(user_message)
            or self.has_person_in_db(user_message)
        )

        is_portal_link_candidate = (
            any(h in msg for h in PORTAL_LINK_STRONG_HINTS)
            and any(v in msg for v in PORTAL_LINK_VERBS)
        )

        # Departman
        department = self.extract_department_name(user_message)
        has_department = department is not None

        #  PORTAL LINK BAĞLAMI VARSA → DEPARTMAN SUSTURULUR
        if is_portal_link_candidate:
            has_department = False
            department = None

        # FIX: workforce bağlamında "bayi" work_type iken departman sayılmasın
        if work_type == "Bayi":
            has_department = False
            department = None

        has_question = (
            self.has_work_history_count_signal(msg)
            or any(k in msg for k in QUESTION_KEYWORDS)
            or bool(re.search(r"(mi|mı|mu|mü)\b", msg))
            or bool(re.search(r"(mi|mı|mu|mü)\b", msg_stripped))  # şirkettemi, uzaktanmı
        )
        
        has_bulk_list_request = (
            self.detect_bulk_people_context(msg)
            and not has_person          # kişi adı yok
            and not has_question        # soru değil
            and not any(k in msg for k in [
                "departman", "departmanlar", "departmanı",
                "birim", "birimler",
                "organizasyon"
            ])
        )

        #  EXPORT SİNYALİ
        EXPORT_KEYWORDS = [
            "excel", "exel",
            "liste", "listesi",
            "döküman", "dokuman",
            "indir", "çıkar",
            "export","döküman"
        ]
        has_export = (
            any(k in msg for k in EXPORT_HINTS)
            and any(k in msg for k in ["excel", "exel"])
        )

        #  WORK HISTORY SİNYALİ (BEN)
        HISTORY_KEYWORDS = [
            "geldim", "çalıştım", "calistim",
            "ofisteydim", "şirketteydim",
            "evdeydim", "izin aldım",
            "uzaktan çalıştım"
        ]
        has_history = any(k in msg for k in HISTORY_KEYWORDS)

        LOCATION_KEYWORDS = [
            
            "nerede","nerdede","nerde","neredeler","nerdeler"
        ]
        has_location_context = any(k in msg_stripped for k in LOCATION_KEYWORDS)

        #  ALAN (email, tel vs.)
        raw_has_people_field = (
            self.has_people_field_request(user_message)
            and not any(k in msg for k in [
                "kim", "kimler",
                "kac", "kaç", "kaç kişi", "kaç tane"
            ])
        )
        #  people_field SADECE GERÇEK KİŞİSEL ALANLAR İÇİN TRUE
        raw_has_people_field = self.has_people_field_request(user_message)

        #mail telefon gibi 
        has_people_field = (
            raw_has_people_field
            and not has_date
            and not has_work_type
        )

        #  EXPORT / PEOPLE FIELD VARSA → work_type İPTAL
        if has_export or has_people_field:
            has_work_type = False
            work_type = None

        #  TOPLU KİŞİ BAĞLAMI (şirket / departman / herkes) tek kişi değil
        has_bulk_people_context = (
            self.detect_bulk_people_context(msg)
            and not any(k in msg for k in [
                "departman", "departmanlar",
                "sayisi", "sayısı",
                "nelerdir", "neler"
            ])
        )

        DEPARTMENT_LIST_QUESTION_HINTS = [
            "hangi", "hangileri", "nelerdir", "neler",
            "liste", "listesi",
            "var", "mevcut",
            "şirketteki", "sirketteki"
        ]

        has_department_list_question = (
            any(k in msg for k in DEPARTMENT_WORD_VARIANTS)
            and (
                any(k in msg for k in ["hangi", "hangileri", "nelerdir", "neler","çeşitleri"])
                or "departmanlar" in msg
            )
            and not has_people_field   #  mail/tel varsa KAPAT
            and not has_export 
        )

        # ---- WORK HISTORY INTENT (FINAL) -----
        history_date_info = self.extract_history_dates(user_message)
        has_history_date = bool(history_date_info and history_date_info.get("start"))
        
        has_work_history_intent = (
            any(k in msg for k in [
                "kaç gün",
                "kac gun","kç gün",
                "ne kadar gün",
                "kç gün",
                "gün sayısı",
                "gun sayisi"
            ])
            and has_history_date
            and not any(k in msg for k in [
                "bugün", "yarın", "yarin",
                "şu an", "simdi"
            ])
        )

        has_work_history_count = has_work_history_intent

        #  TOPLU SONUÇ

        return {
            # temel
            "has_location_context": has_location_context,
            "has_date": has_date, 
            "has_work_type": has_work_type,
            "work_type": work_type,

            "has_person": has_person,
            "has_department": has_department,
            "department": department,

            # niyet
            "has_question": has_question,
            "has_calendar_action": has_calendar_action,
            "has_history": has_history,

            # export / directory
            "has_export": has_export,
            "has_people_field": has_people_field,
            "has_bulk_people_context": has_bulk_people_context,

            "has_department_list_question": has_department_list_question,
            "has_bulk_list_request": has_bulk_list_request,
            "has_work_history_count": has_work_history_count,
            "has_history_date": has_history_date,
            "has_work_history_intent": has_work_history_intent,

        }


