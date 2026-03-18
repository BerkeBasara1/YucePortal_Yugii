from .shared import *


class WorkHistoryMixin:
    def normalize_db_work_type(self, value):
        """
        DB canonicalizasyonu:
        - NULL           → Izin
        - "" / "izin"    → Izin
        - Ofis(*)        → Ofis
        - Home(*)        → Home
        - Bayi(*)        → Bayi
        - Bilinmeyen     → None (bilinçli)
        """

        # İZİN = NULL
        if value is None:
            return "Izin"

        v = str(value).strip().lower()
        v = v.replace("ı", "i").replace("İ", "i").replace("i̇", "i")

        # İZİN (string olarak gelmişse)
        if v in {"", "izin"}:
            return "Izin"

        # OFİS
        if v.startswith("ofis"):
            return "Ofis"

        # HOME
        if v.startswith("home") or v in {"ev", "evde", "remote", "homeoffice"}:
            return "Home"

        # BAYİ
        if v.startswith("bayi") or v in {"saha", "ziyaret", "musteri"}:
            return "Bayi"

        # ❗ Bilinmeyen → tespit edilmedi
        return None
    
    def parse_work_history_summary(self, message: str, start, end, work_type, query_type):
        """
        Kullanıcının isteğinden NET bir özet çıkarır (LLM yok).
        """
        # Çalışma tipi etiketi
        wt_label = (
            "izin"
            if work_type == "Izin"
            else work_type.lower()
            if work_type
            else "tüm çalışma türleri"
        )

        # Zaman etiketi
        date_label = f"{start.strftime('%d.%m.%Y')} – {end.strftime('%d.%m.%Y')}"

        return {
            "date_label": date_label,
            "work_type_label": wt_label,
            "query_type": query_type
        } 
    
    def llm_format_work_history_count(self, summary, count: int): 
        prompt = f"""
            Kısa ve net bir Türkçe cümle yaz.
            Sayım DEĞİŞMEZ, sadece anlatım yap.

            Kurallar:
            - Tek cümle.
            - Gelecek zaman yok.
            - Emoji yok.
            - Resmi ve net ton.

            Bilgiler:
            - Tarih: {summary['date_label']}
            - Tür: {summary['work_type_label']}
            - Gün sayısı: {count}

            Sadece cümleyi yaz.
            """
        return self.ask_gpt(prompt)

    def control_work_history(self, message: str, user_info: dict):
        """
        Kullanıcının geçmiş / gelecek çalışma ve izin günlerini analiz eder.

        KURALLAR:
        - İzin = ofis_bayi IS NULL
        - Hafta sonu ASLA dahil edilmez
        - Gelecek max 30 gün
        - Geçmiş max 365 gün
        - COUNT / LIST merkezi keyword listesiyle belirlenir
        """

        user_id = user_info.get("id")
        if not user_id:
            return "🚫 Kullanıcı bilgisi bulunamadı."

        today = datetime.now().date()
        msg = message.lower()

        # ======================================================
        # 1️⃣ TARİH ARALIĞI
        # ======================================================
        tarih_info = self.extract_history_dates(message)
        start = tarih_info.get("start")
        end = tarih_info.get("end")

        if not start or not end:
            return (
                "📅 İnceleyebilmem için bir tarih aralığı belirtmelisin.<br>"
                "Örnekler:<br>"
                "• “Bu ay kaç gün ofise geldim”<br>"
                "• “Geçen hafta izinlerim”<br>"
                "• “11–15 kasım home çalıştığım günler”"
            )

        # ======================================================
        # 2️⃣ RANGE TİPİ & LİMİTLER
        # ======================================================
        is_past = end < today
        is_future = start > today
        is_mixed = start <= today <= end

        if is_future and (end - today).days > 30:
            return (
                "🚫 Geleceğe yönelik en fazla <b>30 gün</b> için sorgulama yapabilirim."
            )

        if is_past and (today - start).days > 365:
            return (
                "🚫 <b>1 yıldan</b> daha eski çalışma kayıtlarına erişemiyorum."
            )

        # ======================================================
        # 3️⃣ SORGU TÜRÜ (COUNT / LIST)
        # ======================================================
        WORK_HISTORY_LIST_KEYS = [
            "neler",
            "hangileri",
            "hangi gunler","hngi gunler","hngi gnler",
            "hangi gunlerde",
            "hangi tarihler",
            "listele",
            "goster",
            "nelerdir"
        ]
        msg_norm = self.normalize_people_text(message)

        if any(k in msg_norm for k in WORK_HISTORY_LIST_KEYS):
            query_type = "list"
        elif any(k in msg_norm for k in WORK_HISTORY_COUNT_KEYS):
            query_type = "count"
        else:
            query_type = "list"   # default

        # ======================================================
        # 4️⃣ ÇALIŞMA TİPİ (Ofis / Home / Bayi / Izin / None)
        # ======================================================
        work_type = self.detect_work_type(message)
        # None → tüm tipler

        # ======================================================
        # 5️⃣ SQL (HAFTA SONU HARİÇ!)
        # ======================================================
        conn = _mysql_conn()
        if conn is None:
            return "⚠️ Çalışma geçmişine erişilemiyor."

        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT selected_date, ofis_bayi
            FROM ofis_gunleri
            WHERE users1_id = %s
            AND selected_date BETWEEN %s AND %s
            AND WEEKDAY(selected_date) < 5
            ORDER BY selected_date
        """

        cursor.execute(sql, (user_id, start, end))
        self.auto_log_sql(sql, (user_id, start, end))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # ======================================================
        # 6️⃣ WORK TYPE FİLTRESİ (KANONİK)
        # ======================================================
        filtered = []
        unknown_days = []

        for r in rows:
            wt_db = self.normalize_db_work_type(r["ofis_bayi"])

            if wt_db is None:
                unknown_days.append(r["selected_date"])
                continue

            if work_type is None:
                filtered.append(r)
                continue

            if wt_db == work_type:
                filtered.append(r)

        # ======================================================
        # 7️⃣ GELECEKTE KAYIT YOKSA
        # ======================================================
        if is_future and not filtered:
            label = "izin" if work_type == "Izin" else work_type.lower() if work_type else "çalışma"
            return f"📭 Belirtilen tarihlerde işaretlenmiş bir <b>{label}</b> günü bulunmuyor."

        # ======================================================
        # 8️⃣ COUNT MOD
        # ======================================================
        if query_type == "count":
            label = (
                "izinli"
                if work_type == "Izin"
                else work_type.lower()
                if work_type
                else "çalışma"
            )

            response = (
                f"📊 {start.strftime('%d.%m.%Y')} – {end.strftime('%d.%m.%Y')} "
                f"aralığında toplam <b>{len(filtered)}</b> iş günü "
                f"<b>{label}</b> olarak işaretlenmiş."
            )

            if unknown_days:
                response += (
                    "<br>ℹ️ Bazı günlerde çalışma şekli net görünmüyor."
                    "Daha doğru bir sonuç için isteğini biraz daha detaylı yazabilir veya ilgili günleri haftalık takviminden kontrol edebilirsin."
                )

            return response

        # ======================================================
        # 9️⃣ LIST MOD
        # ======================================================
        if not filtered:
            return "📭 Bu tarih aralığında eşleşen bir kayıt bulunamadı."

        result = (
            f"🗓 {start.strftime('%d.%m.%Y')} – {end.strftime('%d.%m.%Y')} "
            f"aralığında işaretlenen günler:<br>"
        )

        for r in filtered:
            d = r["selected_date"]
            tip = self.normalize_db_work_type(r["ofis_bayi"])
            result += f"• {self.format_date_with_day(d)} — {tip}<br>"

        return result


    def handle_department_count(self):
        count = self.get_department_count()

        if count is None:
            return "Departman bilgilerine şu anda ulaşılamıyor."

        return f"Şirkette toplam <b>{count}</b> farklı departman bulunuyor."
    
    #llm people info company için
