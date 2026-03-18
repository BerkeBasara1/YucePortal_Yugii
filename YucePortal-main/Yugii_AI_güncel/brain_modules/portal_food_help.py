from .shared import *


class PortalFoodHelpMixin:
    def detect_link_intent(self, user_message: str) -> bool:
        """
        Kullanıcı mesajının bir portal sayfa linki isteme niyetinde olup olmadığını GPT ile tespit eder.
        """
        #  OTOPARK VARSA LINK INTENT ÇALIŞMASIN
        if any(k in self.normalize_people_text(user_message) for k in OTOPARK_KEY):
            return False
        
        prompt = f"""
    Sen Yüce Auto'nun şirket içi portalı olan YücePortal için geliştirilmiş bir dijital asistansın.

    Görevin: Kullanıcının bir portal sayfasını, raporu, modülü veya bağlantıyı arayıp aramadığını tespit etmektir.

    YücePortal’ın içerdiği modüller ve sayfalar (örnekler):
    - Otopark Rezervasyonu 
    - Şarj İstasyonu Rezervasyon
    - Sabah Raporu / Akşam Raporu / Öngörü Raporu
    - Organizasyon Şeması
    - Kafeterya Siparişleri
    - Fiktif Araç Bildirimi / Filo Fiktif Araç Bildirimi
    - Dashboard / Sayaç / İstatistik Paneli
    - Satın Alma
    - Kurgu Excel
    - Jato Verileri
    - PDF Karşılaştırma
    - YS Faaliyet Raporu
    - Ana Sayfa
    - Acil Durum Kat Planları
    - SSH sayfası

    Bu sayfalara yönlendirme isteyen kullanıcılar genellikle şu kelime veya kalıpları kullanır:
    - "sayfa", "sayfası", "panel", "modül", "ekran", "raporu", "rapor"
    - "nerede", "nerde", "nereye", "nasıl açılır", "nasıl giderim"
    - "link", "bağlantı", "linkini", "linki", "bağlantısını"
    - "aç", "göster", "götür", "bul", "ulaş", "getir"
    - "menüsünü", "menü nerede","nerde","nerede"

    AYRICA:
    Kullanıcı yanlış yazabilir. Örneğin:
    - “shh sayfası”
    - “otoprak raporo”
    - “org sçeması”
    - “fiktiv araş”
    - “ak’şam rapooru”
    - “şarj istasonu”

    Bu hatalı yazımları da bir sayfa arama niyeti olarak kabul etmelisin.

    Kullanıcı mesajı:
    "{user_message}"

    SORU:
    Bu mesaj bir portal sayfası / modülü / raporu / bağlantıyı arama, bulma veya açma amacı taşıyor mu?

    Sadece:
    EVET
    veya
    HAYIR
    diye yanıt ver.
    """

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=5
            )

            raw = resp.choices[0].message.content
            normalized = raw.strip().lower()

            print("🟦 [INTENT DEBUG] RAW:", raw)
            print("🟦 [INTENT DEBUG] NORMALIZED:", normalized)

            return normalized.startswith("e")

        except Exception as e:
            print("Intent hata:", e)
            return False


    def detect_food_intent(self, user_message: str) -> bool:
        msg = user_message.lower()
        food_words = [
            "yemek", "menü", "menu", "yemekte", "bugün ne var", "ne yiyeceğiz",
            "ne var bugün", "yemek listesi","ne yemek","yemekde","yemkde","bugun ne yesek",
            "ne yesek","ne yiyecegiz","yemekte ne var","yemek var mi","menu var mi","bugunku menu",
            "bugun yemek","yarin yemek","cuma menu",
            "pazartesi yemek","yemek kac tl","menu fiyati","yemek fiyati",
            "ucret","kac para","menu degisti mi","bugun ne cikiyor","yemek cikiyor mu"
        ]
        return any(w in msg for w in food_words)


    def resolve_food_date(self, message):
        """
        Kullanıcının istediği günü gerçek tarihe çevirir.
        Sadece bugün + 2 gün (toplam 3 gün) izin verir.
        Daha ileri tarihleri None döndürerek reddettirir.
        """

        msg = message.lower()
        today = datetime.now().date()

        # 1) BUGÜN
        if any(trigger in msg for trigger in RELATIVE_DAY_TRIGGERS["today"]):
            return today

        # 2) YARIN
        if any(trigger in msg for trigger in RELATIVE_DAY_TRIGGERS["tomorrow"]):
            return today + timedelta(days=1)

        # 3) ÖBÜR GÜN / SONRAKİ GÜN
        if "öbür gün" in msg or "sonraki gün" in msg or "ertesi gün" in msg:
            return today + timedelta(days=2)

        # 4) HAFTANIN GÜNLERİ → gün adı geçiyorsa tarihe çevir
        weekday_map = {
            "pazartesi": 0,
            "salı": 1, "sali": 1,
            "çarşamba": 2, "carsamba": 2,
            "perşembe": 3, "persembe": 3,
            "cuma": 4,
            "cumartesi": 5,
            "pazar": 6
        }

        for word, weekday_number in weekday_map.items():
            if word in msg:
                today_weekday = today.weekday()
                diff = weekday_number - today_weekday
                if diff < 0:
                    diff += 7  # gelecek haftanın günü

                target_date = today + timedelta(days=diff)

                # ❗ 3 günlük sınırı (bugün + 2 gün)
                if (target_date - today).days <= 2:
                    return target_date
                else:
                    return None  # ileri tarih

        # Hiç gün belirtilmemişse → default olarak bugün
        return today

    def get_food_menu_for_date(self, target_date):
        try:
            conn = pyodbc.connect(YA_2El_AracSatis)
            cur = conn.cursor()
            cur.execute("""
                SELECT yemek1, yemek2, yemek3, yemek4, yemek5, yemek6,
                       yemek1_fiyat, yemek2_fiyat, yemek3_fiyat,
                       yemek4_fiyat, yemek5_fiyat, yemek6_fiyat,
                       notlar
                FROM [Yuce_Portal].[dbo].[Kafeterya_Menu]
                WHERE CAST(menu_date AS DATE) = CAST(? AS DATE)
            """, (target_date,))
            row = cur.fetchone()
            conn.close()
            return row
        except Exception as e:
            print("DB yemek hata:", e)
            return None
        
    def _format_page_response(self, row):
        return (
            f"🔗 <b>{row.page_name}</b> sayfasına buradan ulaşabilirsin:<br>"
            f"<a href='{row.url}' target='_blank'>{row.url}</a><br><br>"
            f"{row.description or ''}"
        )

    #  DB'DEN SAYFA EŞLEŞTİRME (SYNONYM + FUZZY + EMBEDDING)
    def find_page_link(self, user_message: str) -> str:
        """
        Kullanıcı sayfa / link / nerede dediğinde
        DB'den en uygun portal sayfasını bulur ve
        direkt kullanıcıya cevap döndürür.
        """

        print("🔍 [PORTAL LINK] user_message:", user_message)

        try:
            conn = pyodbc.connect(YA_2El_AracSatis)
            cur = conn.cursor()
            sql = """
                SELECT page_name, url, description, synonyms
                FROM [Yuce_Portal].[dbo].[yugii_page_links]
                WHERE active = 1
            """
            cur.execute(sql)
            self.auto_log_sql(sql, None)
            rows = cur.fetchall()
            conn.close()

            message = self.normalize_people_text(user_message)

            #  SYNONYM (EN GÜÇLÜ)
            best_score = 0
            best_row = None

            for r in rows:
                if not r.synonyms:
                    continue

                synonyms = [
                    s.strip().lower()
                    for s in r.synonyms.split(",")
                    if len(s.strip()) >= 3
                ]

                score = 0
                for s in synonyms:
                    if s in message:
                        score += 2
                    elif fuzz.partial_ratio(message, s) >= 85:
                        score += 1

                if score > best_score:
                    best_score = score
                    best_row = r

            if best_row:
                return self._format_page_response(best_row)

            #  FUZZY (PAGE NAME + SYNONYM)
            FUZZY_THRESHOLD = 70
            best_score = 0
            best_row = None

            for r in rows:
                candidates = []

                if r.page_name:
                    candidates.append(r.page_name.lower())

                if r.synonyms:
                    candidates.extend(
                        s.strip().lower()
                        for s in r.synonyms.split(",")
                        if len(s.strip()) >= 3
                    )

                for c in candidates:
                    score = fuzz.partial_ratio(message, c)
                    if score > best_score:
                        best_score = score
                        best_row = r

            if best_score >= FUZZY_THRESHOLD:
                return self._format_page_response(best_row)

            # EMBEDDING (SON ÇARE)
            if not hasattr(self, "_page_link_embedder"):
                self._page_link_embedder = SentenceTransformer(
                    "paraphrase-multilingual-mpnet-base-v2"
                )

            texts = []
            row_map = []

            for r in rows:
                base = r.page_name or ""
                if r.synonyms:
                    base += " " + r.synonyms.replace(",", " ")
                texts.append(base)
                row_map.append(r)

            msg_emb = self._page_link_embedder.encode(message, convert_to_tensor=True)
            page_embs = self._page_link_embedder.encode(texts, convert_to_tensor=True)

            sims = util.cos_sim(msg_emb, page_embs)[0]
            best_idx = int(sims.argmax())
            best_sim = float(sims[best_idx])

            if best_sim >= 0.75:
                return self._format_page_response(row_map[best_idx])

            return (
                "Aradığın sayfayı net bulamadım 🤔<br>"
                "Biraz daha açık yazar mısın? (örn: haftalık takvim, otopark, ssh)"
            )

        except Exception as e:
            print("❌ PORTAL LINK HATA:", e)
            return "Şu anda sayfa bilgilerine erişemiyorum."


    def get_db_otopark_help_text(self, user_message):


        help_pool = [

            # 1
            (
                "💚 Otopark rezervasyonu yapmak oldukça pratik!<br><br>"
                "🧭 <b>Portal üzerinden:</b><br>"
                "👉 <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>Otopark Rezervasyon Sayfası</a><br><br>"
                "💬 <b>Yugii ile:</b><br>"
                "• “Yarın 10 numaralı parkı ayır”<br>"
                "• “17 kasım için park ayır”<br>"
                "• “Bu hafta park ayır”<br>"
            ),

            # 2
            (
                "🅿️ Park ayırmak çok kolay!<br>"
                "İstersen <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>portal üzerinden</a> yapabilirsin,<br>"
                "ya da bana şöyle yazabilirsin:<br>"
                "• “Yarın park ayır”<br>"
                "• “18 kasım 12 numara park ayır” 💚"
            ),

            # 3
            (
                "🌿 Elbette! Otopark rezervasyonu için:<br>"
                "👉 Portal: <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>Otopark Sayfası</a><br>"
                "👉 Yugii: “Yarın 9 numaralı parkı ayır” yazman yeterli 🙂"
            ),

            # 4
            (
                "💚 Park rezervasyonu oluşturmak için iki yol var:<br>"
                "• <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>Portal ekranından</a> oluşturabilirsin yada <br>"
                "• Ya da bana kısaca 'yarın 8 numaralı parkı ayır' yazabilirsin 🌿"
            ),

            # 5
            (
                "🅿️ Park ayırma çok pratik!<br>"
                "👉 Portal: <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>yüceportal sayfasından yada buradan</a><br>"
                "👉 Yugii: '17 kasım park ayır' demen yeterli 😊"
            ),

            # 6
            (
                "🌿 Yardımcı olayım! Otopark rezervasyonu için:<br>"
                "• Ya da bana 'yarın 11 numarayı ayır' gibi bir mesaj yazabilirsin 💚"
                "• Portal bağlantısı: <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>Buraya tıkla</a><br>"

            ),

            # 7
            (
                "💚 Park rezervasyonu oluşturmak istiyorsan;<br>"
                "👉 Ya da bana 'yarın 10 numara park ayır' yazman yeterli 🙂"
                "👉 <a href='https://yuceportal.skoda.com.tr/YA_otopark_rezerve' target='_blank'>Portal sayfasını açarakda kolay bir şekilde</a> yapabilirsin.<br>"

            ),

        ]

        return random.choice(help_pool)
    
    def generate_calendar_help_ai(self, user_message):
        try:
            prompt = f"""
            Kullanıcı haftalık takvimi nasıl işaretleyeceğini soruyor.

            Sadece şu formatta çok kısa bir mesaj üret:
            1️⃣ Kısa bir giriş cümlesi (tek cümle, max 1 emoji).
            2️⃣ Takvimin mantığını TEK cümlede açıkla: “gün + çalışma tipi yazman yeterli”.
            3️⃣ Aynı satırda 2 örnek ver: “Salı home”, “Perşembe ofis”.
            4️⃣ Son satır TEK satır olmalı ve aynen şöyle başlamalı:
            Haftalık Takvim 👇 https://yuceportal.skoda.com.tr/haftalik_takvim

            Kurallar:
            - En fazla 2–3 satır üret.
            - Paragraf yok.
            - Uzun açıklama YOK.
            - Cümleler kısa ve sade olsun.
            - Blok yapısını BOZMA.
            - Kesinlikle 3 satırı geçme.

            Kullanıcı mesajı: "{user_message}"
            """
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=80,
                temperature=0.6
            )
            return response.choices[0].message.content.strip()

        except:
            return (
                "Gün + çalışma tipi yazman yeterli 😊 Örn: Salı home, Perşembe ofis<br>"
                "Haftalık Takvim 👇 https://yuceportal.skoda.com.tr/haftalik_takvim"
            )

    def get_calendar_help_text(self, user_message=None):

        # AI tamamen kapalı — sadece static mesajlar dönecek ilerde geliştirek için ai eklenecek
        # if random.random() < 0.7:
        #     return self.generate_calendar_help_ai(user_message)

        static_pool = [
            (
                "Takvime gün eklemek çok kolay 😊<br>"
                "Örnek: “Cuma ofis” — “Salı home ekle”<br>"
                "Haftalık Takvim 👇 "
                "<a href='https://yuceportal.skoda.com.tr/haftalik_takvim' target='_blank'>Haftalık Takvim</a>"
            ),
            (
                "Gün + çalışma tipi yazman yeterli 💚<br>"
                "Mesela: “Pazartesi ofis” veya “Çarşamba home işaretle”<br>"
                "Haftalık Takvim 👇 "
                "<a href='https://yuceportal.skoda.com.tr/haftalik_takvim' target='_blank'>Haftalık Takvim</a>"
            ),
            (
                "Elbette! Takvimde bir gün işaretlemek için kısa bir komut yazman yeterli 🙂<br>"
                "Örneğin: “Perşembe home” — “Yarın ofis ekle”<br>"
                "Haftalık Takvim 👇 "
                "<a href='https://yuceportal.skoda.com.tr/haftalik_takvim' target='_blank'>Haftalık Takvim</a>"
            )
        ]

        return random.choice(static_pool)

    #help parse modülü için 
    def help_user_with_parse(self, user_message: str) -> dict:
        """
        HELP intent için mesajı parçalar.
        İşlem yapmaz, sadece rehberlik için bağlam çıkarır.
        """

        msg = user_message.lower()

        if any(k in msg for k in ["otopark", "park", "rezervasyon"]):
            topic = "otopark"
        elif any(k in msg for k in [
            "takvim", "haftalık", "ofis", "home", "izin", "işaretle"
        ]):
            topic = "haftalik_takvim"

        # 🔹 Excel / Export HELP (öncelikli!)
        elif any(k in msg for k in [
            "excel", "exel", "liste", "indir", "çıkar",
            "export", "dosya", "tablo"
        ]):
            topic = "company_people_export_help"

        elif any(k in msg for k in [
            "kim", "çalışan", "personel", "mail", "email", "telefon"
        ]):
            topic = "company_people"

        else:
            topic = "unknown"

        if any(k in msg for k in ["nasıl", "nasil", "nasıl yaparım", "nasil yaparim"]):
            question_type = "how"
        elif any(k in msg for k in [
            "yapabiliyor musun", "yapabilir misin",
            "mümkün mü", "mumkun mu"
        ]):
            question_type = "capability"
        else:
            question_type = "guide"

        keywords = []
        for k in [
            "otopark", "park", "rezervasyon",
            "takvim", "haftalık", "ofis", "home",
            "yardım", "nasıl"
        ]:
            if k in msg:
                keywords.append(k)

        return {
            "topic": topic,
            "question_type": question_type,
            "keywords": keywords
        }

    def llm_with_handle_help(self, parsed: dict, user_message: str) -> str:
        topic = parsed.get("topic")

        if topic == "unknown":
            return (
                "Hangi konuda yardım istediğini biraz açar mısın? 😊<br>"
                "Otopark, haftalık takvim veya çalışan bilgileri gibi konularda yardımcı olabilirim."
            )
        
        if topic == "company_people_export_help":
            return (
                "Çalışan listelerini Excel olarak almak için net bir komut yazman yeterli 😊<br><br>"
                "Örnekler:<br>"
                "• 'Tüm çalışanların mail adreslerini Excel al'<br>"
                "• 'IT departmanı çalışanlarını Excel çıkar'<br>"
                "• 'Çalışanların mail ve telefonlarını Excel indir'<br>"
                "• 'Tüm çalışanların tüm bilgilerini Excel ver'<br><br>"
                "Bu şekilde yazdığında Yugii Excel dosyasını otomatik oluşturur."
            )
        if topic == "otopark":
            context = (
                "Yugii, otopark rezervasyonu konusunda rehberlik eder.\n"
                "Kullanıcı isterse portal üzerinden, isterse Yugii'ye yazarak rezervasyon yapabilir.\n"
                "Örnekler:\n"
                "- 'Yarın 10 numaralı parkı ayır'\n"
                "- '17 kasım için park ayır'"
            )

        elif topic == "haftalik_takvim":
            context = (
                "Yugii, haftalık çalışma takvimi işaretleme konusunda rehberlik eder.\n"
                "Gün + çalışma tipi yazman yeterlidir.\n"
                "Örnekler:\n"
                "- 'Salı evden çalışma olarak işaretle'\n"
                "- 'Perşembe ofisten çalışacağım'"
            )

        elif topic == "company_people":
            context = (
                "Yugii, şirket içi çalışan rehberi konusunda bilgi verir.\n"
                "İsim, departman, email ve telefon bilgileri sorulabilir."
            )

        else:  # general
            context = (
                "Yugii, şirket içi işlemler ve bilgi taleplerinde yardımcı olur.\n"
                "Otopark, takvim, yemek menüsü ve çalışan bilgileri gibi konulara destek verir."
            )

        prompt = f"""
    Sen Yüce Auto'nun dijital asistanı Yugii'sin.

    Kurallar:
    - Yalnızca aşağıdaki bilgileri kullan.
    - İşlem yapma.
    - Kısa ve net cevap ver (maks 3–4 cümle).

    Bilgi:
    {context}

    Kullanıcı sorusu:
    "{user_message}"

    SADECE cevabı yaz.
    """

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=120,
                temperature=0.3
            )

            answer = resp.choices[0].message.content.strip()

            page_row = self.find_page_link(user_message)

            if isinstance(page_row, dict) and page_row.get("url"):
                answer += (
                    "<br><br>"
                    f"<a href='{page_row['url']}' target='_blank'>"
                    f"🔗 {page_row.get('page_name','Sayfa')} sayfasına git"
                    f"</a>"
                )

            return answer   

        except Exception as e:
            print("❌ llm_with_handle_help hata:", e)
            return "Bu konuda sana kısaca yardımcı olabilirim, biraz daha detay sorar mısın?"

    #otopark rezervasyon tarih anlama isim fix yapılacak otopark_parse_tarih() şeklinde
