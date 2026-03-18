from .shared import *


class PeopleDirectoryMixin:
    def handle_company_people(self, user_message: str):
        """
        Company People Directory – FINAL & STABLE
        """
        parsed = self.fast_parse_company_people(user_message)
        parsed.setdefault("intent", "company_people")
        parsed = self.resolve_person_entity(user_message, parsed)

        if (
            parsed.get("confidence", 0) < 0.7
            and not parsed.get("persons")
        ):
            parsed = self.mini_llm_parse_company_people(user_message, parsed)

        #  TEK İSİM + persons boşsa → DB'den isimle lookup
        if not parsed.get("persons"):
            name_candidates = self.detect_person_prescan(user_message)
            if name_candidates:
                parsed["persons"] = name_candidates
                parsed["target"] = "person"

        # DB FETCH
        # --------------------------------------------------
        data = self.find_company_people_data(parsed)
        data = self.enrich_people_with_profile_links(data)

        
        #  MULTI PERSON SMART FIX
        if (
            parsed["target"] == "person"
            and len(data) > 1
            and parsed.get("confidence", 0) < 1.0   # 👈 KRİTİK
        ):

            norm_q = self.normalize_people_text(user_message)

            # ✅ Kullanıcı bilinçli çoklu kişi sormuşsa → SORMA, ANLAT
            if " ve " in norm_q or "," in norm_q or " ile " in norm_q:
                return self.compose_company_people_response(
                    question=user_message,
                    parsed=parsed,
                    data=data
                )

            # ❓ Gerçekten belirsizse (örn: "elif kim")
            names = [f"{d['name']} {d['surname']}" for d in data]


            return (
                "Birden fazla kişi buldum:\n"
                + "\n".join(f"- {n}" for n in names)
                + "\n\nHangisini demek istedin?"
            )

        # 🔥 TEK KİŞİ + ALAN YOK → OTOMATİK KİM (IDENTITY)
        if (
            parsed.get("target") == "person"
            and len(data) == 1
            and (not parsed.get("fields") or parsed.get("fields") <= {"name", "surname"})

        ):
            parsed["fields"] = {"identity"}
            return self.compose_company_people_response(
                question=user_message,
                parsed=parsed,
                data=data
            )

        # --------------------------------------------------
        # 5️⃣ DB → HİÇ KİŞİ YOK
        # --------------------------------------------------
        if not data and parsed["target"] == "person":
            fallback = parsed.copy()
            fallback["target"] = "people_list"
            if parsed.get("persons"):
                fallback["persons"] = [parsed["persons"][0].split()[0]]
            else:
                return "Kiminle ilgili bilgi istediğini tekrardan sorabilir misiniz?"

            alt_data = self.find_company_people_data(fallback)

            if alt_data:
                names = [f"{d['name']} {d['surname']}" for d in alt_data]
                return (
                    "Bu isimle birebir eşleşen bir çalışan bulamadım. "
                    "Bunlardan birini mi kastediyorsun?\n"
                    + "\n".join(f"- {n}" for n in names)
                )

            return "Bu isimle eşleşen aktif bir çalışan bulunamadı."

        # --------------------------------------------------
        # 8️⃣ FINAL RESPONSE
        # --------------------------------------------------
        return self.compose_company_people_response(
            question=user_message,
            parsed=parsed,
            data=data
        )

    #companu people kişi çözümleme için tek ve çoklu  
    def resolve_person_entity(self, text: str, parsed: dict) -> dict:
        """
        KİŞİ ADI ÇÖZÜM MERKEZİ (TEK OTORİTE)

        SIRA:
            2.1 username
            2.2 surname (tekil)
            2.3 surname + name daraltma
            2.4 name
            hiçbiri yoksa → parsed olduğu gibi devam
        """

        #  PORTAL CONTEXT GUARD — kişi çözümlemesine girme
        if parsed.get("intent") == "portal_info":
            print("🟦 [NAME-RESOLVE SKIP] portal_info intent detected")
            return parsed

        #  SESSION USER 3. TEKİL ŞAHIS FIX
        session_full = self.normalize_people_text(session.get("fullname", ""))

        if session_full and session_full in text_norm:
            # "sude'nin telefon numarası" gibi
            parsed["persons"] = [session.get("fullname")]
            parsed["target"] = "person"
            parsed["confidence"] = 1.0
            return parsed
        
        # TAM İSİM OVERRIDE (multi-person'dan ÖNCE)
        text_norm = self.normalize_people_text(text)
        MULTI_SEPARATORS = [" ve ", " ile ", ","]

        #  TAM İSİM OVERRIDE — SADECE TEK KİŞİ NİYETİNDE
        if not any(sep in text_norm for sep in MULTI_SEPARATORS):
            for p in session.get("detected_persons", []):
                p_norm = self.normalize_people_text(p)
                if p_norm in text_norm:
                    parsed["persons"] = [p]
                    parsed["target"] = "person"
                    parsed["confidence"] = 1.0

                    session.pop("pending_persons", None)
                    session.pop("pending_person_question", None)

                    print("🟢 [NAME OVERRIDE] single-person full name:", p)
                    return parsed
                
        #  SADECE BOŞLUKLA YAZILMIŞ ÇOKLU İSİM FIX
        detected = session.get("detected_persons", [])
        if detected and len(detected) > 1:
            parsed["persons"] = detected
            parsed["target"] = "person"
            parsed["confidence"] = max(parsed.get("confidence", 0), 0.9)
            return parsed
        
        original_text = text
        text_norm = self.normalize_people_text(text)

        #  MULTI PERSON FIX (ve / , ile çoklu kişi)
        if (" ve " in text_norm or "," in text_norm):
            detected = session.get("detected_persons", [])

            if detected:
                parsed["persons"] = detected
                parsed["target"] = "person"
                parsed["confidence"] = max(parsed.get("confidence", 0), 0.9)

                print("🟢 [NAME-RESOLVE] multi-person detected:", detected)
                return parsed

        print(f"[NAME-RESOLVE] input text (raw): {original_text}")
        print(f"[NAME-RESOLVE] input text (norm): {text_norm}")


        #  önce split et
        tokens = text_norm.split()

        # APOSTROPHE FIX (aksakal'ın → aksakal)
        clean_tokens = []
        for t in tokens:
            if "'" in t:
                t = t.split("'")[0]
            if "’" in t:
                t = t.split("’")[0]

            if len(t) >= 2:
                clean_tokens.append(t)

        tokens = clean_tokens
        
        # sonra suffix temizle
        def strip_tr_suffix(token: str) -> str:
            SUFFIXES = [
                "ninki",    
                "nin","nın","nun","nün",
                "in","ın","un","ün",
                "ye","ya",
                "e","a",
                "i","ı","u","ü",
                "de","da","den","dan",
                "te","ta",
                "si","sı","su","sü"
            ]

            changed = True
            while changed:
                changed = False
                for s in SUFFIXES:
                    if token.endswith(s) and len(token) > len(s) + 1:
                        token = token[:-len(s)]
                        changed = True
                        break

            return token

        NAME_IGNORE_WORDS = {
            "mail", "maili", "mailini",
            "eposta", "epostasi", "epostasini",
            "adres", "adresini",
            "ver", "verir", "verebilir",
            "kim", "nedir"
        }
        #  isim dışı kelimeleri token listesinden temizle
        tokens = [t for t in tokens if t not in NAME_IGNORE_WORDS]

        #  DB-DRIVEN FALLBACK
        try:
            conn = _mysql_conn()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    LOWER(name)     AS name,
                    LOWER(surname)  AS surname,
                    LOWER(username) AS username
                FROM users1
                WHERE is_active = 1
            """)
            users = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print("❌ DB fallback hata:", e)
            return parsed

        #  USERNAME
        for u in users:
            username_norm = self.normalize_people_text(u["username"])

            if username_norm and username_norm in tokens:

                full = f"{u['name']} {u['surname']}"
                print(f"[NAME-FALLBACK] username match → {username_norm} → {full}")

                parsed["persons"] = [full]
                parsed["target"] = "person"
                parsed["confidence"] = 1.0

                # 🔒 KESİN KİŞİ KİLİDİ (ÇOK ÖNEMLİ)
                session.pop("detected_persons", None)
                session.pop("pending_persons", None)
                session.pop("pending_person_question", None)

                return parsed
            
        #  yüce soyadı olunca çakışma engellme
        if "yuce" in tokens:
            # Yüce soyadına sahip kişilerin isimlerini çıkar
            yuce_names = {
                self.normalize_people_text(u["name"])
                for u in users
                if self.normalize_people_text(u["surname"]) == "yuce"
            }

            # tokens içinde Yüce'ye ait bir isim var mı?
            has_name_with_yuce = any(t in yuce_names for t in tokens)

            # SADECE "yüce" yazılmışsa → kişi çözümünü iptal et
            if not has_name_with_yuce:
                parsed["persons"] = []
                parsed["target"] = None
                parsed["confidence"] = 0.0

                print("🟡 [NAME-RESOLVE] 'yüce' surname-only detected → skipped")

                return parsed

        # SURNAME
        # -----------------------------
        #  NAME + SURNAME BİRLİKTE YAZILDIYSA → KESİN TEK KİŞİ
        for u in users:
            name_norm = self.normalize_people_text(u["name"])
            surname_norm = self.normalize_people_text(u["surname"])

            if name_norm in tokens and surname_norm in tokens:
                full = f"{u['name']} {u['surname']}"
                print(f"🟢 [NAME-RESOLVE] full name match → {full}")

                parsed["persons"] = [full]
                parsed["target"] = "person"
                parsed["confidence"] = 1.0

                # 🔒 BURASI ÇOK KRİTİK (KİLİT)
                session.pop("detected_persons", None)
                session.pop("pending_persons", None)
                session.pop("pending_person_question", None)

                return parsed
            
        # SURNAME (YÜCE ÖZEL KURALI İLE)
        surname_hits = []

        for u in users:
            surname_norm = self.normalize_people_text(u["surname"])

            if not surname_norm or surname_norm not in tokens:
                continue

            #  ÖZEL KURAL: SADECE "yüce" İÇİN
            if surname_norm == self.normalize_people_text("Yüce"):
                name_norm = self.normalize_people_text(u["name"])

                # tokens içinde isim YOKSA → EŞLEŞMEYİ ATLAMALIYIZ
                if name_norm not in tokens:
                    continue

            surname_hits.append(u)

        # SOYADI + İYELİK EKİ VARSA → KESİN KİŞİ
        if surname_hits:
            for u in surname_hits:
                surname_norm = self.normalize_people_text(u["surname"])

                # YÜCE özel istisna
                if surname_norm == "yuce":
                    name_norm = self.normalize_people_text(u["name"])
                    if name_norm not in tokens:
                        continue

                # ORİJİNAL METİNDE: "aksakal'ın", "aksakalın" gibi bir kullanım var mı?
                if re.search(
                    rf"\b{surname_norm}(?:\'|’)?(?:in|ın|un|ün|nin|nın|nun|nün)\b",
                    original_text.lower()
                ):
                    parsed["persons"] = [f"{u['name']} {u['surname']}"]
                    parsed["target"] = "person"
                    parsed["confidence"] = max(parsed.get("confidence", 0), 0.95)

                    print(f"🟢 [NAME-RESOLVE] possessive surname → {u['name']} {u['surname']}")
                    return parsed

        if surname_hits:
            print(f"[NAME-FALLBACK] surname hits → {[u['surname'] for u in surname_hits]}")

            if len(surname_hits) == 1:
                u = surname_hits[0]
                full = f"{u['name']} {u['surname']}"
                print(f"[NAME-FALLBACK] surname unique → {full}")

                parsed["persons"] = [full]
                parsed["target"] = "person"
                parsed["confidence"] = max(parsed.get("confidence", 0), 0.9)
                return parsed

            # SURNAME + NAME DARALTMA
            for u in surname_hits:
                name_norm = self.normalize_people_text(u["name"])

                if (
                    name_norm
                    and name_norm in tokens
                    and name_norm not in NAME_IGNORE_WORDS
                ):
                    full = f"{u['name']} {u['surname']}"
                    print(f"[NAME-FALLBACK] surname+name narrowed → {full}")

                    parsed["persons"] = [full]
                    parsed["target"] = "person"
                    parsed["confidence"] = max(parsed.get("confidence", 0), 0.9)
                    return parsed

        # NAME
        name_hits = []
        for u in users:
            name_norm = self.normalize_people_text(u["name"])

            if (
                name_norm
                and name_norm in tokens
                and name_norm not in NAME_IGNORE_WORDS
            ):
                name_hits.append(u)

        if name_hits:
            if len(name_hits) == 1:
                u = name_hits[0]
                full = f"{u['name']} {u['surname']}"
                print(f"[NAME-FALLBACK] name unique → {full}")

                parsed["persons"] = [full]
                parsed["target"] = "person"
                parsed["confidence"] = max(parsed.get("confidence", 0), 0.8)
                return parsed
            
            else:
                # çoklu isim → karar verme, prescan + DB yönetsin
                return parsed
            
        #  Prescan çoklu kişi bulduysa ve resolve karar vermediyse
        if not parsed.get("persons") and session.get("detected_persons"):
            parsed["persons"] = session["detected_persons"]
            parsed["target"] = "person"

        print("[NAME-RESOLVE] no name resolved, fallback to existing flow")
        return parsed



    def fast_parse_company_people(self, msg: str):
        """
        PROD-ready Company People parser
        - Yazım hatalarına dayanıklı
        - Çoklu alan destekli
        - PERSON vs DEPARTMENT ayrımı yapar
        """
        print("\n🧪 [PARSE INPUT]:", msg)

        text = self.normalize_people_text(msg)

        #  result HER ŞEYDEN ÖNCE
        result = {
            "intent": None,
            "target": None,
            "persons": [],
            "department": None,
            "fields": set(),
            "confidence": 0.0
        }

        # ERKEN DEPARTMAN KİLİDİ (NAME PARSE ÖNCESİ)
        dept = self.extract_department_name(msg)
        if dept and any(k in text for k in [
            "kim", "kimler",
            "calisan", "calisiyor", "calisanlar",
            "ekip", "ekibi", "ekibinde"
        ]):
            result["target"] = "department"
            result["department"] = dept
            result["fields"] = {"name", "surname"}
            result["confidence"] += 0.9
            result["intent"] = "company_people"

            print("🟢 [EARLY DEPT LOCK]:", dept)
            return result


        FIELD_KEYWORDS = {
            field: [self.normalize_people_text(k) for k in keywords]
            for field, keywords in RAW_FIELD_KEYWORDS.items()
        }
        #  FIELD TESPİTİ (ÇOKLU)
        for field, keywords in FIELD_KEYWORDS.items():
            if any(k in text for k in keywords):
                # field alias → DB column map
                key = field.lower().strip()
                db_col = FIELD_TO_COLUMN.get(key, field)
                result["fields"].add(db_col)
                result["confidence"] += 0.15


        #  DEPARTMAN LİSTE SORUSU
        if "kimler var" in text or "calisanlar" in text:
            result["target"] = "people_list"
            result["confidence"] += 0.3


        #  DEPARTMAN ADI
        if result["target"] == "department":
            dept = self.extract_department_name(msg)
            if dept:
                result["department"] = dept
                result["confidence"] += 0.2
        # DEPARTMAN + "KİM" SORGUSU
        if (
            result.get("department")
            and not result["fields"]
            and any(k in text for k in [
                    "kim", "kimler",
                    "ekip", "ekibi", "ekibinde",
                    "calisiyor", "calisiyorlar",
                    "calisan", "calisanlar",
                    "calisanlari"
                ])

        ):
            result["target"] = "department"
            result["fields"] = {"name", "surname"}
            result["confidence"] += 0.6

        #  DEFAULT FIELD SET (GENEL SORU)
        if "identity" in result["fields"]:
            result["fields"].update({
                "name", "surname", "title", "departman", "email", "TelNo"
            })

        #  DEFAULT TARGET: kişi bilgisi sorusu
        if result["target"] is None and result["fields"]:
            result["target"] = "person"
            result["confidence"] += 0.2

        # INTENT KARARI
        if result["target"] == "person":
            result["intent"] = "company_people"


        print("🧪 [PARSE FIELDS]:", result["fields"])
        print("🧪 [PARSE TARGET]:", result["target"])
        print("🧪 [PARSE PERSONS]:", result["persons"])
        print("🧪 [PARSE CONFIDENCE]:", result["confidence"])
        print("🧠 [PARSE FINAL]:", result)
        return result
 
    #LLM çağrısı yapma ama eksik tamamlancak
    def mini_llm_parse_company_people(self, user_message: str, parsed: dict):
        """
        Mini LLM fallback – HALÜSİNASYON-PROOF

        AMAÇ:
        - fast_parse yeterince emin olamadığında
        - SADECE target + fields bilgisini netleştirmek

        KURALLAR:
        - Intent DEĞİŞTİRMEZ
        - DB görmez
        - Cevap yazmaz
        - Yorum yapmaz
        - SADECE JSON döner
        """

        if parsed.get("intent") != "company_people":
            return parsed
        
        if parsed.get("fields"):
            return parsed

        prompt = f"""
      
        Sen bir AYRIŞTIRMA (decomposition) motorusun.
        Cevap yazmazsın. Tahmin yapmazsın. Yorum yapmazsın.

        Sadece aşağıdaki JSON'u döndür.
        JSON dışında hiçbir şey yazma.

        {{
        "target": "person | people_list | null",
        "persons": [],
        "department": null,
        "fields": [],
        "confidence": 0.0
        }}

        ALLOWED FIELDS:
        email, TelNo, title, departman, linkedin, dogum_gun, dogum_ay, identity

        KURALLAR:
        - İsim uydurma.
        - Sadece cümlede açık geçen isimleri al.
        - Emin değilsen boş bırak.
        - Multiple kişi olabilir.

        Kullanıcı cümlesi:
        \"\"\"{user_message}\"\"\"

        """

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.0,
                max_tokens=120
            )

            raw = resp.choices[0].message.content.strip()

            import json
            llm_data = json.loads(raw)

            if llm_data.get("persons"):
                parsed["persons"] = llm_data["persons"]

            if llm_data.get("target") in ["person", "department"]:
                parsed["target"] = llm_data["target"]

            allowed_fields = {
                "email", "TelNo", "title", "surname",
                "departman", "dogum_gun", "dogum_ay",
                "linkedin", "identity"
            }

            clean_fields = [
                f for f in llm_data.get("fields", [])
                if f in allowed_fields
            ]

            if clean_fields:
                parsed["fields"] = clean_fields
                parsed["confidence"] = max(parsed.get("confidence", 0), 0.7)

            return parsed

        except Exception as e:
            print("⚠️ mini_llm_parse_company_people hata:", e)
            return parsed

