from .shared import *


class AnalyticsDealersMixin:
    def get_trend_analysis(self):

        conn = _mysql_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            DATE_FORMAT(selected_date, '%Y-%m') AS ay,
            COUNT(*) AS toplam,
            SUM(ofis_bayi = 'Ofis') AS ofis,
            SUM(ofis_bayi = 'Home') AS home,
            SUM(ofis_bayi = 'Bayi') AS bayi,
            SUM(ofis_bayi IS NULL) AS izin
        FROM ofis_gunleri
        WHERE selected_date >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
        GROUP BY ay
        ORDER BY ay;
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(rows) < 2:
            return {"error": "Yeterli veri yok"}

        def calc_ratio(val, total):
            if total == 0:
                return 0
            return round((val / total) * 100, 1)

        last = rows[0]
        this = rows[1]

        return {
            "this_month": {
                "ay": this["ay"],
                "Ofis": calc_ratio(this["ofis"], this["toplam"]),
                "Home": calc_ratio(this["home"], this["toplam"]),
                "Bayi": calc_ratio(this["bayi"], this["toplam"]),
                "Izin": calc_ratio(this["izin"], this["toplam"]),
            },
            "last_month": {
                "ay": last["ay"],
                "Ofis": calc_ratio(last["ofis"], last["toplam"]),
                "Home": calc_ratio(last["home"], last["toplam"]),
                "Bayi": calc_ratio(last["bayi"], last["toplam"]),
                "Izin": calc_ratio(last["izin"], last["toplam"]),
            }
        }
    
    def format_trend_response(self, data):

        if "error" in data:
            return "Aylık kıyas raporu için yeterli veri bulunamadı."

        this_m = data["this_month"]
        last_m = data["last_month"]

        prompt = f"""
        Aşağıdaki iki aylık çalışma dağılım verisini değerlendir.

        {this_m['ay']}:
        Ofis: %{this_m['Ofis']}
        Home: %{this_m['Home']}
        Bayi: %{this_m['Bayi']}
        Izin: %{this_m['Izin']}

        {last_m['ay']}:
        Ofis: %{last_m['Ofis']}
        Home: %{last_m['Home']}
        Bayi: %{last_m['Bayi']}
        Izin: %{last_m['Izin']}

        Kurumsal ve sade bir değerlendirme yaz.
        'kanal', 'artış', 'düşüş' kelimelerini kullanma.
        Yeni sayı üretme. en fazla 3 cümle net kısa olsun.
        """

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Kurumsal ve net bir yönetici değerlendirmesi yaz."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        comment = response.choices[0].message.content[:300]

        return f"""
    📊 <b>Aylık Çalışma Kıyas Raporu</b><br><br>

    <b>{this_m['ay']}:</b><br>
    🏢 Ofis: %{this_m['Ofis']}<br>
    🏠 Home: %{this_m['Home']}<br>
    🏢 Bayi: %{this_m['Bayi']}<br>
    🌴 İzin: %{this_m['Izin']}<br><br>

    <b>{last_m['ay']}:</b><br>
    🏢 Ofis: %{last_m['Ofis']}<br>
    🏠 Home: %{last_m['Home']}<br>
    🏢 Bayi: %{last_m['Bayi']}<br>
    🌴 İzin: %{last_m['Izin']}<br><br>

    ⚡ <b>Analiz sonucu:</b><br>
    {comment}
    """
    
    all_cities = {
        "adana","adiyaman","afyonkarahisar","agri","amasya","ankara","antalya",
        "artvin","aydin","balikesir","bilecik","bingol","bitlis","bolu","burdur",
        "bursa","canakkale","cankiri","corum","denizli","diyarbakir","edirne",
        "elazig","erzincan","erzurum","eskisehir","gaziantep","giresun","gumushane",
        "hakkari","hatay","isparta","mersin","istanbul","izmir","kars","kastamonu",
        "kayseri","kirklareli","kirsehir","kocaeli","konya","kutahya","malatya",
        "manisa","kahramanmaras","mardin","mugla","mus","nevsehir","nigde",
        "ordu","rize","sakarya","samsun","siirt","sinop","sivas","tekirdag",
        "tokat","trabzon","tunceli","sanliurfa","usak","van","yozgat","zonguldak",
        "aksaray","bayburt","karaman","kirikkale","batman","sirnak","bartin",
        "ardahan","igdir","yalova","karabuk","kilis","osmaniye","duzce"
    }


    def detect_city_from_text(self, msg_norm):

        print("CITY FUNC INPUT:", msg_norm)
        words = re.findall(r"\w+", msg_norm)
        print("ALL CITIES SAMPLE:", list(self.all_cities)[:10])
        print("MSG NORM:", msg_norm)
        print("ankara in all_cities:", "ankara" in self.all_cities)
        for word in words:

            for city in self.all_cities:

                # direkt eşleşme
                if word == city:
                    return city

                # ekli versiyon (ankara + da/de)
                if word.startswith(city):
                    return city

                # fuzzy eşleşme (ankarda → ankara)
                if difflib.SequenceMatcher(None, word, city).ratio() > 0.85:
                    return city

        return None
    
    def get_all_dealers(self, force_refresh=False):

        # 10 dakika cache
        if (
            not force_refresh
            and self._dealer_cache
            and self._dealer_cache_time
            and datetime.now() - self._dealer_cache_time < timedelta(minutes=10)
        ):
            return self._dealer_cache

        conn = self._oracle_conn()
        if not conn:
            return []

        QUERY = """
        SELECT
            YS.FK_EDUCATION_FIRM_ID AS FIRM_ID,
            YS.FIRM_CODE,
            MAX(CASE WHEN DR.REGION_TYPE = 'S' THEN DRC.REGION_CHIEF_FULL_NAME END),
            MAX(CASE WHEN DR.REGION_TYPE = 'L' THEN DRC.REGION_CHIEF_FULL_NAME END),
            CC.CITY_NAME
        FROM
            YUCE_DM.TBL_DW_GEN_DIM_DEALER YS
            INNER JOIN YUCE_DM.TBL_DW_GEN_DIM_DEALER_REGION DR
                ON YS.DEALER_ID = DR.FK_DEALER_ID
            AND DR.REGION_TYPE IN ('S','L')
            INNER JOIN YUCE_DM.TBL_DW_GEN_DIM_DEALER_REGION_CHIEF DRC
                ON DRC.FK_REGION_DEALER_ID = DR.REGION_DEALER_ID
            INNER JOIN YUCE_DM.TBL_DW_GEN_DIM_FIRM GEN_FIRM
                ON GEN_FIRM.EDUCATION_FIRM_ID = YS.FK_EDUCATION_FIRM_ID
            LEFT JOIN YUCE_DM.TBL_DW_GEN_DIM_CITY_COUNTY CC
                ON CC.CODE = YS.FK_CITY_CODE
        WHERE
            YS.STATUS_EXPLANATION = 'Yürürlükte'
            AND YS.FIRM_CODE NOT IN ('YÜCE AUTO')
        GROUP BY
            YS.FK_EDUCATION_FIRM_ID, YS.FIRM_CODE, CC.CITY_NAME
        ORDER BY
            YS.FIRM_CODE ASC
        """

        try:
            cursor = conn.cursor()
            cursor.execute(QUERY)
            rows = cursor.fetchall()

            dealers = []
            for r in rows:
                dealers.append({
                    "firm_id": r[0],
                    "firm_code": r[1],
                    "sales_manager": r[2],
                    "ssh_manager": r[3],
                    "city": r[4]
                })

            # cache'e yaz
            self._dealer_cache = dealers
            self._dealer_cache_time = datetime.now()

            return dealers

        except Exception as e:
            print("❌ Dealer sorgu hatası:", e)
            return []

        finally:
            cursor.close()
            conn.close()

    def get_satis_count_by_year(self, year: int):
        conn = self._oracle_conn()
        if not conn:
            return None

        cursor = conn.cursor()

        sql = """
            SELECT COUNT(DISTINCT VEHICLE_ID)
            FROM YUCE_DM.TBL_DW_VEH_RPT_VEHICLE_STATUS_UP_TO_DATE D
            WHERE EXTRACT(YEAR FROM D.AD_INVOICE_DATE) = :year
        """

        cursor.execute(sql, {"year": year})
        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return result

    def handle_satis_count(self, msg: str):

        current_year = datetime.now().year
        years = []

        # Yıl yakalama (2025, 2026 vs.)
        found_years = re.findall(r"20\d{2}", msg)

        if found_years:
            years = [int(y) for y in found_years]

        elif "gecen yil" in msg or "geçen yıl" in msg:
            years = [current_year - 1]

        else:
            # Direkt "kaç satış yaptık" → bu yıl + geçen yıl
            years = [current_year, current_year - 1]

        responses = []

        for year in years:
            count = self.get_satis_count_by_year(year)

            if count is not None:
                responses.append(
                    f"🚗 {year} yılına baktığımızda, toplamda {count:,} adet araç satışı gerçekleştirmişiz. "
                    f"Oldukça güçlü bir performans görünüyor."
                )
            else:
                responses.append(
                    f"🚗 {year} yılı için satış verisine şu anda ulaşılamadı."
                )

        return "<br><br>".join(responses)

    def hanlde_bayi_about(self, user_message):

        msg = self.normalize_tr(user_message)

        COUNT_KEYS = [
            "kaç", "kac",
            "adet", "tane",
            "toplam", "total",
            "sayisi", "sayısı","adeti","adeti","syısı"
        ]

        # 1️⃣ Önce COUNT kontrol edilir
        if any(k in msg for k in COUNT_KEYS):
            return self._handle_bayi_count(msg)

        # 2️⃣ Sonra liste intenti
        if "bayi" in msg:
            return self._handle_bayi_list_with_count(msg)

        return "Bayi ile ilgili isteğini biraz daha net yazabilir misin?"
    
    def normalize_tr(self, text: str) -> str:
        if not text:
            return ""

        text = text.lower()

        replacements = {
            "ı": "i",
            "i̇": "i",
            "ş": "s",
            "ç": "c",
            "ğ": "g",
            "ü": "u",
            "ö": "o",
        }

        for k, v in replacements.items():
            text = text.replace(k, v)

        return text.strip()
    
    def _handle_bayi_list_with_count(self, msg):

        data = self.get_all_dealers()
        if not data:
            return "Bayi verisi alınamadı."

        msg_norm = self.normalize_tr(msg)

        city_found = None

        for d in data:
            city_raw = d.get("city")
            if not city_raw:
                continue

            city_norm = self.normalize_tr(city_raw)

            pattern = rf"\b{re.escape(city_norm)}(da|de|daki|deki)?\b"

            if re.search(pattern, msg_norm):
                city_found = city_raw
                break

        if not city_found:
            return "Hangi şehir için bayi listesi istediğini belirtir misin?"

        filtered = [
            d for d in data
            if d["city"] == city_found
        ]

        count = len(filtered)

        if count == 0:
            return f"📍 {city_found} ilinde aktif bayi bulunmamaktadır."

        firm_list = sorted([
            d["firm_code"] for d in filtered
            if d["firm_code"]
        ])

        response = f"📍 {city_found} ilinde {count} adet aktif bayi bulunmaktadır.\n\n"

        for firm in firm_list:
            response += f"- {firm}\n"

        return response
    
    def _handle_bayi_count(self, msg):

        data = self.get_all_dealers()
        if not data:
            return "Bayi verisi alınamadı."

        msg_norm = self.normalize_tr(msg)

        # 81 il üzerinden şehir yakala
        detected_city = self.detect_city_from_text(msg_norm)
        print("DETECTED CITY:", detected_city)
        # DB şehir seti
        db_cities = {
            self.normalize_tr(d["city"]).strip()
            for d in data if d["city"]
        }

        # -------------------------
        # ŞEHİR YAZILMIŞ
        # -------------------------
        if detected_city:

            if self.normalize_tr(detected_city) not in db_cities:
                return (
                    f"📍 {detected_city.title()} ilinde aktif bayimiz bulunmamaktadır.\n\n"
                    "Yetkili satıcı ve servis noktalarımızı aşağıdaki bağlantıdan kontrol edebilirsiniz:\n"
                    "🔗 https://www.skoda.com.tr/yetkili-satici-ve-servisler"
                )

            count = len([
                d for d in data
                if self.normalize_tr(d["city"]) == detected_city.strip()
            ])

            if count == 1:
                return f"📍 {detected_city.title()} ilinde 1 adet aktif bayi bulunmaktadır."

            return f"📍 {detected_city.title()} ilinde {count} adet aktif bayi bulunmaktadır."

        # -------------------------
        # GENEL COUNT
        # -------------------------
        total = len(data)
        return f"🇹🇷 Türkiye genelinde toplam {total} adet aktif bayi bulunmaktadır."
