from .shared import *


class PeopleContextMixin:
    def _build_people_field_roots(self):
        roots = set()

        for keywords in RAW_FIELD_KEYWORDS.values():
            for k in keywords:
                k_norm = self.normalize_people_text(k)
                if " " not in k_norm and len(k_norm) >= 3:   
                    roots.add(k_norm)

        return roots
    
    def has_first_person_possessive(self, text: str) -> bool:
        text = self.normalize_people_text(text)

        # 🔒 SADECE GERÇEK 1. TEKİL ŞAHIS
        FIRST_PERSON_KEYS = {
            "benim",
            "bana",
            "bende",
            "benden",
            "bizim",
            "bizi"
        }

        return any(k in text for k in FIRST_PERSON_KEYS)

    def detect_person_prescan(self, text: str) -> list:
        """
        INTENT ÖNCESİ PERSON TESPİTİ
        - users1 tablosuna bakar
        - normalize + suffix strip kullanır
        - SADECE tespit eder (karar vermez)
        - return: ["isimsoyisim]veya []
        """

        text_norm = self.normalize_people_text(text)
        tokens = text_norm.split() 

        CORPORATE_GUARD_BASE = [
            "yuce portal","yuceportal","yuce auto","şirketimiz",
            "yuce oto","yuceauto","yuce firma","sirketimiz","firma","marka","kurum","skoda","skodanın","skoda'da","skoda'nın"
        ]

        CORPORATE_GUARD_INFO = [
            "nedir",
            "bilgi",
            "hakkinda","nasıl bir yer","nasıl bir şirket",
            "ne ise yarar","ne is yapar","hakkinda", "anlat","bilgi","fikrin","fikirilerin","neler düşünüyorsun","düşüncelerin",
        ]

        if (
            any(b in text_norm for b in CORPORATE_GUARD_BASE)
            and any(i in text_norm for i in CORPORATE_GUARD_INFO)
        ):
            return []
        
        # SESSION USER NAME OVERRIDE (ADIYLA SORARSA)
        session_name = f"{session.get('name','')} {session.get('surname','')}".strip()
        session_first = self.normalize_people_text(session.get("name",""))

        if (
            session_first
            and session_first in text_norm.split()
            and not self.has_people_field_request(text_norm)
        ):
            return [session_name]

        #  BEN / 1. TEKİL ŞAHIS → SESSION USER
        if "benim" in text_norm:
            session_name = f"{session.get('name','')} {session.get('surname','')}".strip()
            if session_name:
                return [session_name]

        # ---- Türkçe ek temizleme ----
        def strip_tr_suffix(token: str) -> str:
            SUFFIXES = ["ninki","nin","nın","nun","nün","in","ın","un","ün",
                        "ye","ya","de","da","den","dan","te","ta","si","sı","su","sü"]
            changed = True
            while changed:
                changed = False
                for s in SUFFIXES:
                    if token.endswith(s) and len(token) > len(s) + 1:
                        token = token[:-len(s)]
                        changed = True
                        break
            return token

        tokens = text_norm.split()
        tokens = [strip_tr_suffix(t) for t in tokens]

        IGNORE = {
            "mail","maili","eposta","adres",
            "telefon","numara",
            "kim","nedir","ver"
        }

        tokens = [
            t for t in tokens
            if t not in IGNORE
            and t.isalpha()
            and len(t) >= 3
        ]

        # ---- DB'den kişi isimlerini al ----
        try:
            conn = _mysql_conn()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT name, surname
                FROM users1
                WHERE is_active = 1
            """)
            users = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception:
            return []

        found = []
        match_type = "NONE"

        for u in users:
            name_norm = self.normalize_people_text(u["name"])
            surname_norm = self.normalize_people_text(u["surname"])

            # 1) isim + soyisim
            if name_norm in tokens and surname_norm in tokens:
                result = [f"{u['name']} {u['surname']}"]
                match_type = "FULL_NAME"

                return result
            
            # 2) sadece soyisim
            if surname_norm in tokens and match_type == "NONE":
                match_type = "SURNAME"
                found.append(f"{u['name']} {u['surname']}")
                continue

            # 3) sadece isim
            if name_norm in tokens and match_type == "NONE":
                match_type = "NAME"
                found.append(f"{u['name']} {u['surname']}")

        try:
            session_name = f"{session.get('name','')} {session.get('surname','')}".strip()
            if session_name:
                session_name_norm = self.normalize_people_text(session.get("name",""))
                if session_name_norm in tokens and session_name not in found:
                    found.insert(0, session_name)
        except Exception:
            pass
        final_found = list(dict.fromkeys(found))

        return final_found
    
    def has_corporate_context(self, msg: str, has_bulk_people: bool) -> bool:
        msg = self.normalize_people_text(msg)

        return any([
            bool(has_bulk_people),
            any(k in msg for k in ALL_PEOPLE_KEYWORDS),
            any(k in msg for k in DEPARTMENT_WORD_VARIANTS),
            self.has_people_field_request(msg),          # mail, tel, title
            bool(self.detect_person_prescan(msg)),       # kişi adı
            self.extract_department_name(msg) is not None,  # departman
        ])
    
    def has_people_field_request(self, msg: str) -> bool:
        text = self.normalize_people_text(msg)

        for keywords in RAW_FIELD_KEYWORDS.values():
            for k in keywords:
                if self.normalize_people_text(k) in text:
                    return True
            for root in self.people_field_roots:
                if root in text:
                    return True
        return False
    
    def has_all_people_reference(self, msg: str) -> bool:
        text = self.normalize_people_text(msg)

        STRONG_PEOPLE_ROOTS = [
            "calisan",
            "personel",
            "kisi",
            "ekip",
            "herkes"
        ]
        CONTEXTUAL_ROOTS = [
            "ofis",
            "sirket",
            "isyeri",
            "tum",
            "tamami",
            "hepsi"
        ]

        #  Güçlü kök varsa direkt true
        if any(r in text for r in STRONG_PEOPLE_ROOTS):
            return True

        #  Bağlamsal kök + people kökü birlikteyse true
        if any(r in text for r in CONTEXTUAL_ROOTS) and any(
            p in text for p in STRONG_PEOPLE_ROOTS
        ):
            return True

        return False
    
    SENSITIVE_PASSWORD_KEYWORDS = [
        # Türkçe
        "sifre", "şifre",
        "kullanici sifresi", "kullanıcı şifresi",
        "pc sifresi", "pc şifresi",
        "bilgisayar sifresi", "bilgisayar şifresi",
        "portal sifresi", "portal şifresi",
        "giris sifresi", "giriş şifresi","pc şifre","pc pasword"

        # İngilizce
        "password",
        "pass",
        "login password",
        "pc password",
        "user password",
        "account password",

        # Karışık
        "mail sifresi",
        "email sifresi",
        "outlook sifresi",
        "office sifresi"
        ]
    

    def has_password_request(self, msg: str) -> bool:
        PASSWORD_GUIDE_KEYWORDS = [
        "nasil",
        "nasıl",
        "degistir",
        "değiştir",
        "guncelle",
        "güncelle",
        "sifremi degistir",
        "sifremi değiştir",
        "sifre degistirme",
        "sifre degistirilir",
        "sifre nasil",
        "password change",
        "reset",
        "yenile"
    ]
        text = self.normalize_people_text(msg)

        # 🔓 Eğer kullanıcı "nasıl / değiştir / reset" diyorsa → ŞİFRE TALEBİ DEĞİL
        if any(k in text for k in PASSWORD_GUIDE_KEYWORDS):
            return False

        # 🔒 Aksi halde → gerçek şifre talebi mi?
        return any(k in text for k in self.SENSITIVE_PASSWORD_KEYWORDS)
    
    def handle_password_guide(self):
        return (
            "🔐 Bilgisayar şifreni değiştirmek için iki yol bulunuyor:<br><br>"
            "• IT ekibiyle iletişime geçerek destek isteyebilirsin.<br>"
            "• Bilgisayarında <b>Ctrl + Alt + Delete</b> tuşlarına basarak "
            "“Parola Değiştir” seçeneğini kullanabilirsin.<br><br>"
            "Her iki yöntem de güvenli ve yaygın olarak kullanılıyor."
        )
    
    def handle_cancel_without_context(self) -> str:
        return (
            "Ne için iptal işlemi yapmak istersin? 🤔<br>"
            "İptal etmek istediğin işlemi biraz daha net yazar mısın?<br>"
            "Örnek olarak:<br>"
            "• “Yarınki veya aktif tüm <b>otopark</b> rezervasyonumu iptal et”<br>"
        )
    def get_department_count(self):
        """
        ofis_gunleri tablosuna göre
        GERÇEKTE kullanılan departman sayısını döndürür
        """
        conn = _mysql_conn()
        if conn is None:
            return None

        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT TRIM(LOWER(Department)))
            FROM ofis_gunleri
            WHERE Department IS NOT NULL
            AND TRIM(Department) <> ''
        """)

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count
    
    def contains_department_word(self, msg: str) -> bool:
        text = self.normalize_people_text(msg)

        for root in DEPARTMENT_WORD_VARIANTS:
            # departman, departmanlar, departmanlarda, departmanların...
            if re.search(rf"\b{root}(ler|lar|in|ın|un|ün|de|da|den|dan)?\b", text):
                return True

        return False
    
    def has_work_history_count_signal(self, msg: str) -> bool:
        """
        Yazım hatalarına dayanıklı 'kaç / ne kadar' tespiti
        """

        msg_norm = self.normalize_people_text(msg)

        for key in WORK_HISTORY_COUNT_KEYS:
            key_norm = self.normalize_people_text(key)

            # birebir
            if key_norm in msg_norm:
                return True

            # fuzzy (özellikle bozuk yazım)
            if fuzz.partial_ratio(msg_norm, key_norm) >= 85:
                return True

        return False
    
    def detect_currency_calculation(self, msg: str) -> bool:

        # sayı var mı
        has_number = bool(re.search(r"\d+[.,]?\d*", msg))

        # para birimi (kök bazlı, ekli halleri yakalar)
        has_currency = bool(re.search(
            r"\b(dolar|usd|euro|eur|tl|try|lira)\b|\$|€",
            msg
        ))

        # dönüşüm / hesap kelimeleri
        has_calc_word = bool(re.search(
            r"\b(kac|eder|ne kadar|cevir|donustur|hesapla|karsiligi)\b",
            msg
        ))

        # direkt pattern: "100 dolar tl"
        has_direct_pair = bool(re.search(
            r"\d+[.,]?\d*\s+(dolar|usd|euro|eur|tl|try)",
            msg
        ))

        return has_number and has_currency and (has_calc_word or has_direct_pair)

    def normalize_people_name_token(self, token: str) -> str:
        token = token.lower()

        SUFFIXES = [
            "ninki","ndaki","daki",
            "nin","nın","nun","nün",
            "dan","den","tan","ten",
            "yla","yle",
            "yi","yı","yu","yü",
            "in","ın","un","ün",
            "ya","ye"
        ]

        for s in SUFFIXES:
            if token.endswith(s) and len(token) > len(s) + 1:
                return token[:-len(s)]

        return token
    
    TAKVİM_KEYS = [
        "isaretle","ekle","ayarla","planla","yap","gir","yaz","tikla","yap","yp","ekle","isaretlesene",
        "belirle","kayit et","kaydet","isaretle","girermisin","isaretlermisin","calisicam","calisicam",
        "calisacagim","calisacagim","komple","calisacagim","calisacagim",
        "calisacam","calisacam","olacagim","olucam","olacagim",
        "gelecegim","gelicem","clisicam","olacagim","gelecegim","gelicem",
        "isaretle","isaretle","ekle","kaydet","planla","ayarla","olacagim","olucam","calisacagim","calisacagim","caliscam",
        "calisicam","calisicam","gelicem","gelecegim","gelcem","glcm","isarle","işaretle","ısretle","isaretle"
    ]

    def detect_haftalik_takvim_intent(self, user_message: str) -> bool:
        """
        Haftalık takvim EMİR tespiti.
        Bu fonksiyon eski detect_main_intent içindeki
        haftalık takvim mantığının AYNI HALİDİR.
        """

        msg = self.normalize_people_text(user_message)
        has_calendar_action = any(f in msg for f in self.TAKVİM_KEYS)

        # 🚫 LİSTE / EXPORT VARSA ASLA TAKVİM OLMASIN
        if any(k in msg for k in ["liste", "listesi", "export", "excel", "ver","listele"]):
            return False
        
        #  FIX: Başka bir kişi soruluyorsa BU BİR EMİR DEĞİLDİR
        if self.detect_person_prescan(user_message):
            return False
        
        #  OTOPARK kelimesi VARSA → HAFTALIK TAKVİM HİÇ ÇALIŞMAZ
        has_park = any(k in msg for k in OTOPARK_KEY)
        if has_park:
            print("⛔ [BLOCK]: Otopark intent varken haftalık takvim atlandı")


        calisma_tipleri = ["ofis","home","izin","bayi"]

        gun_kelimeleri = [
            "pazartesi","salı","sali","çarşamba","perşembe","cuma","cumartesi","pazar",
            "bugün","bugun","yarın","yarin",
            "haftaya", "gelecek hafta", "önümüzdeki hafta",
            "birdahaki hafta", "next week"
        ]

        tarih_kelimeleri = [
            "ocak","şubat","mart","nisan","mayıs","haziran","temmuz","ağustos",
            "eylül","ekim","kasım","aralık"
        ]

        work_type = self.detect_work_type(user_message)
        msg_has_tip = work_type is not None

        msg_has_gun  = any(g in msg for g in gun_kelimeleri)
        msg_has_date = any(t in msg for t in tarih_kelimeleri)
        is_question = bool(re.search(r"\b(mi|mı|mu|mü)\b", msg))
        has_count_q = any(k in msg for k in ["kaç", "kac", "kim", "kimler", "ne zaman", "hangi"])

        # ⭐ 1) TARİH + ÇALIŞMA TİPİ
        if (
            not has_park
            and msg_has_tip
            and (msg_has_gun or msg_has_date)
            and has_calendar_action              
            and not is_question
            and not has_count_q
        ):
            return True

        # ⭐ 2) ÇALIŞMA TİPİ + EMİR
        if (
            not has_park
            and msg_has_tip
            and has_calendar_action
            and not is_question
            and not has_count_q
        ):
            print("🧠 [INTENT]: haftalik_takvim (çalışma tipi + emir)")
            return True

        # ⭐ 3) GÜN + EMİR
        if (
            not has_park
            and msg_has_gun
            and has_calendar_action
            and not is_question
            and not has_count_q
        ):
            print("🧠 [INTENT]: haftalik_takvim (gün + emir)")
            return True

        # ⭐ 4) SADECE EMİR + ZAMAN
        if (
            not has_park
            and has_calendar_action
            and (msg_has_gun or msg_has_date)
            and not is_question
            and not has_count_q
        ):
            print("🧠 [INTENT]: haftalik_takvim (fiil + zaman)")
            return True

        return False

