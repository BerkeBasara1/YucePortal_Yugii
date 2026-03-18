from .shared import *


class WorkforceStatusMixin:
    def handle_workforce_status(self, user_message: str, user_info: dict):
        """
        WORKFORCE STATUS HANDLER
        - Kişi / Departman / Şirket bazlı
        - Ofis / Home / Bayi / İzin
        - Count / List / Status
        """

        print("\n🧪 [WORKFORCE] RAW INPUT:", user_message)

        msg = self.normalize_people_text(user_message)
        today = datetime.now().date()

        # TARİH ANALİZİ
        date_info = self.parse_workforce_dates(user_message)
        is_period, p_start, p_end = self.is_workforce_period_query(msg, date_info)

        if is_period:
            return self.handle_workforce_period_summary(
                user_message=user_message,
                start=p_start,
                end=p_end,
                msg_norm=msg
            )

        # MODE KULLANMIYORUZ
        start = date_info.get("start") or today
        end   = date_info.get("end") or today

        print("📅 [WORKFORCE] start:", start, "end:", end)

        # 3 AY SINIRI (mode bağımsız)
        if abs((today - start).days) > 90:
            return "En fazla 3 ay aralığında sorgulama yapabilirim."

        # ÇALIŞMA TİPİ
        work_type = self.detect_work_type(user_message)
        print("🏢 [WORKFORCE] work_type:", work_type)

        persons = self.detect_person_prescan(user_message)
        department = self.extract_department_name(user_message)

        if (
            not persons
            and self.normalize_people_text(user_info.get("fullname","").split()[0]) 
                in self.normalize_people_text(user_message).split()
        ):
            persons = [user_info.get("fullname")]

        if self.has_person_in_db(user_message) and not persons:
            return (
                "Bu isimle eşleşen birden fazla veya belirsiz çalışan buldum. "
                "Lütfen isim ve soyisimle birlikte tekrar sorabilir misin?"
            )

        if persons:
            scope = "person"
        elif department:
            scope = "department"
        else:
            scope = "company"



        print("👥 [WORKFORCE] scope:", scope)

        if scope == "person" and len(persons) > 1:
            names = ", ".join(persons)
            return (
                f"Birden fazla kişi buldum: {names}.<br>"
                "Lütfen isim ve soyisimle birlikte tekrar sorabilir misiniz?"
            )

        # SORU TİPİ
        STATUS_KEYWORDS = [
            "ne isaretlemis",
            "ne isaretledi",
            "ne yazmis",
            "ne girmis",
            "nerede",
            "nerden",
            "nereden",
            "nereden calisacak",
            "nerede olacak",
            "ofiste mi",
            "evde mi",
            "bayide mi",
            "izinli mi"          
        ]

        if any(k in msg for k in ["kim", "kimler","kim","kimler","kişiler","çalışanlar","calisanlar","çalışan"]):
            query_type = "list"
        elif any(k in msg for k in STATUS_KEYWORDS):
            query_type = "status"
        elif self.has_work_history_count_signal(msg):
            query_type = "count"
        else:
            query_type = "status"

        if persons and query_type != "list":
            query_type = "status"

        print("❓ [WORKFORCE] query_type:", query_type)

        # 🔥 SELF STATUS FIX (GENEL)
        if (
            scope == "company"
            and query_type == "status"
            and not persons
            and not department
        ):
            persons = [user_info.get("fullname")]
            scope = "person"

        # 🔥 PERSON + STATUS sorgusunda filtre uygulama
        if scope == "person" and query_type == "status":
            work_type = None

        if scope == "person" and not persons:
            return (
                "Bu isimle eşleşen bir çalışan bulamadım. "
                "İsim ve soyisimle birlikte tekrar sorabilir misin?"
            )

        conn = _mysql_conn()
        if not conn:
            return "⚠️ Şu anda çalışma bilgilerine erişemiyorum."

        cursor = conn.cursor(dictionary=True)

        base_sql = """
            FROM ofis_gunleri og
            INNER JOIN users1 u ON u.id = og.users1_id
            WHERE og.selected_date BETWEEN %s AND %s
        """
        params = [start, end]

        if work_type:
            if work_type == "Izin":
                base_sql += " AND (og.ofis_bayi IS NULL OR og.ofis_bayi = '')"
            else:
                base_sql += " AND og.ofis_bayi = %s"
                params.append(work_type)

        if scope == "person":
            name, surname = persons[0].split(" ", 1)
            base_sql += " AND LOWER(u.name) = %s AND LOWER(u.surname) = %s"
            params.extend([name.lower(), surname.lower()])

        print("DEBUG persons:", persons)
        print("DEBUG fullname:", user_info.get("fullname"))

        if scope == "department":
            base_sql += " AND u.departman = %s"
            params.append(department)

        # COUNT
        if query_type == "count":
            sql = "SELECT COUNT(*) AS cnt " + base_sql
            cursor.execute(sql, params)
            self.auto_log_sql(sql, params)
            count = cursor.fetchone()["cnt"]
            cursor.close()
            conn.close()

            label = (
                "izinli"
                if work_type == "Izin"
                else work_type.lower()
                if work_type
                else "çalışan"
            )

            day_label = self.format_workforce_day_label(start, today)

            if scope == "department":
                return (
                    f"{day_label} <b>{department}</b> departmanında <b>"
                    f"{label} olan toplam <b>{count}</b> kişi bulunuyor."
                )

            elif scope == "company":
                return (
                    f"{day_label} şirkette <b>"
                    f"{label} olan toplam <b>{count}</b> kişi bulunuyor."
                )

            else:
                return (
                    f"{day_label} {label} olan toplam <b>{count}</b> kişi bulunuyor."
                )

        # LIST
        if query_type == "list":

            is_department_only = (scope == "department")

            sql = "SELECT u.name, u.surname, u.departman " + base_sql + " ORDER BY u.departman, u.name"
            cursor.execute(sql, params)
            self.auto_log_sql(sql, params)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if not rows:
                return "Bu kriterlere uygun çalışan bulunamadı."

            grouped = {}

            if is_department_only:
                grouped[department] = [
                    f"{r['name']} {r['surname']}" for r in rows
                ]
            else:
                for r in rows:
                    dept = (r["departman"] or "Departman belirtilmemiş").strip()
                    grouped.setdefault(dept, []).append(f"{r['name']} {r['surname']}")

            lines = []

            for dept, people in grouped.items():
                people_str = ", ".join(people)
                lines.append(f"<b>{dept}</b> ({len(people)}): {people_str}")

            day_label = self.format_workforce_day_label(start, today)

            if work_type == "Home":
                emoji = "🏠"
                label = "evden çalışanlar"
            elif work_type == "Bayi":
                emoji = "🚗"
                label = "sahada olanlar"
            elif work_type == "Izin":
                emoji = "🌴"
                label = "izinli olanlar"
            elif work_type == "Ofis":
                emoji = "🏢"
                label = "ofiste olanlar"
            else:
                emoji = "👥"
                label = "çalışanlar"

            if scope == "department":
                title = f"{emoji} {day_label} {department} – {label}"
            else:
                title = f"{emoji} {day_label} {label}"

            return "<br>".join([title, ""] + lines)

        # STATUS (tek kişi)
        sql = "SELECT og.ofis_bayi " + base_sql + " LIMIT 1"
        cursor.execute(sql, params)
        self.auto_log_sql(sql, params)
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        person_name = persons[0] if persons else "Kişi"
        day_label = self.format_workforce_day_label(start, today)

        if not row:
            return f"{person_name} için {day_label} herhangi bir çalışma durumu işaretlenmemiş."

        wt = self.normalize_db_work_type(row["ofis_bayi"])

        is_explicit_izin_mark = any(k in msg for k in [
            "izin isaretle","izinliydi","izinli","izin yapmış","izinlimiydi","izinmi almış",
            "izin almış","izinlimiydi","izinmi aldı","izin işaretlemiş",
            "izin işaretle", "izinli işaretleyenle","izin yazanlar",
            "izin giren","izin girenler","izin almis"
        ])

        if wt == "Izin":
            if is_explicit_izin_mark:
                wt_text = "izin işaretlemiş olarak gözükmekte."
            else:
                wt_text = "izinli"
        elif wt == "Ofis":
            wt_text = "ofisten çalışıyor olarak gözükmekte."
        elif wt == "Home":
            wt_text = "evden çalışıyor olarak gözükmekte."
        elif wt == "Bayi":
            wt_text = "bayide çalışıyor olarak gözükmekte."
        else:
            wt_text = "çalışma tipi tanımsız olarak gözükmekte."

        return f"{person_name}, {day_label} {wt_text}."

    def is_simple_smalltalk(self, message: str) -> bool:
        if not message:
            return False

        msg = self.normalize_people_text(message)

        SMALLTALK_KEYS = [
            "merhaba", "selam", "slm", "hello", "hi",
            "naber", "nbr", "nasilsin", "nasılsın",
            "iyi misin", "ne haber",
            "tesekkur", "teşekkür", "sagol", "sağol"
        ]
        return any(k in msg for k in SMALLTALK_KEYS)

    def is_password_guide_question(self, msg: str) -> bool:
        text = self.normalize_people_text(msg)

        PASSWORD_GUIDE_KEYWORDS = [
            "nasil",
            "nasıl",
            "degistir",
            "değiştir",
            "guncelle",
            "güncelle",
            "sifremi degistir",
            "sifremi değistir",
            "sifre nasil",
            "sifre degistirme",
            "reset",
            "yenile"
        ]

        PASSWORD_CONTEXT = [
            "sifre","sifrem","pc sifrem","pc sifremi","bilgisayar sifremi","pc sfre","pc sifresi",
            "sifrem",
            "sifremi",
            "password",
            "pc sifre",
            "pc sifrem",
            "bilgisayar sifre",
            "bilgisayar sifrem"
        ]
        return (
            any(k in text for k in PASSWORD_GUIDE_KEYWORDS)
            and any(p in text for p in PASSWORD_CONTEXT)
        )


