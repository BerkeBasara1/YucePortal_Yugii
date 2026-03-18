from .shared import *


class MessageProcessingMixin:
    @log_process_message
    def process_message(self, user_message: str):

        print("🟨 [PROCESS] Gelen Mesaj:", user_message)

        signals = self.extract_message_signals(user_message)
        print("🧠 [SIGNALS]")

        # Kullanıcı bilgilerini session’dan çek
        user_info = {
            "id": session.get("ID"),
            "username": session.get("username"),
            "fullname": f"{session.get('name', '')} {session.get('surname', '')}".strip(),
            "plaka": session.get("plaka"),
            "plaka2": session.get("plaka2"),
            "departman": session.get("departman"),
            "email": session.get("email"),
            "arac_marka": session.get("arac_marka"),
        }

        #makinenin rahat anlayacağı hale getiriyor ",ğ->g ,A->a, ı->i
        msg_norm = self.normalize_people_text(user_message)

        if (
            re.search(r"\b(adin|adinın|adı|adi)\s+(ne(y|ydi)?|yugii)\b", msg_norm)
            or "ismin ne" in msg_norm or "ismin" in msg_norm
        ):
            return "Ben Yugii’yim 🙂 Sana nasıl yardımcı olabilirim?"
    
        company_only = self.is_company_only(user_message)

        if company_only:
            if "skoda" in self.normalize_people_text(user_message):
                return self.handle_skoda_reputation()
            else:
                return self.handle_yuce_auto_reputation()
            
        #  1) SİNYALLERİ TOPLA
        
        items = list(signals.items())
        for i in range(0, len(items), 3):
            chunk = items[i:i+3]
            print(" | ".join(f"{k}={v}" for k, v in chunk))


        #  2) DOMAIN KARARI VER
        intent = self.detect_business_intent(user_message, signals)
        print("🟪 [DOMAIN]:", intent)

        #  3) domaşn karar sonrası intent fonk seçme
        if intent is None:
            intent = self.detect_main_intent(user_message, signals )

        print("🧠 [FINAL INTENT]:", intent)
            
        # 🔹 3) SADECE İSİM VARSA (AMA SORU DEĞİLSE!)
        if (
            intent is None
            and not signals["has_question"]
            and not any(k in msg_norm for k in [
                "yuce portal",
                "yuceportal",
                "yuce auto","yuce autodaki","yuce autonun",
                "yuce oto",
                "sirket","skoda",
                "portal","yüce portal"
            ])
        ):
            prescan = self.detect_person_prescan(user_message)
            if prescan:
                intent = "company_people"

        
        if intent == "assistant_capabilities":
            return STATIC_CAPABILITY_TEXT

        if any(k in msg_norm for k in KIM_YAPTI_SORUSU):
            return "Beni Yüce Auto’nun IT ekibinden Sude Bayhan geliştirdi 🙂 Teknik sorularınız için Sude Bayhan ile iletişime geçebilirsiniz."
            
        try:
            if not user_info["plaka"] and not user_info["plaka2"]:
                conn = pyodbc.connect(YA_2El_AracSatis)
                cur = conn.cursor()
                cur.execute("""
                    SELECT TOP 1 plaka, plaka2
                    FROM [Yuce_Portal].[dbo].[users1]
                    WHERE LOWER(username) = LOWER(?)
                """, (user_info["username"],))
                row = cur.fetchone()
                conn.close()
                if row:
                    # Önce plaka, yoksa plaka2
                    user_info["plaka"] = row[0] or row[1]
                    print("🧩 users1 fallback → plaka bulundu:", user_info["plaka"])
        except Exception as e:
            print("⚠️ users1 plaka kontrol hatası:", e)

        print("👤 USER INFO:", user_info)
        
        if self.is_password_guide_question(user_message):
            return self.handle_password_guide()
        
        if self.has_password_request(user_message):

            other_fields_requested = False
            norm_msg = self.normalize_people_text(user_message)

            for keywords in RAW_FIELD_KEYWORDS.values():
                for k in keywords:
                    if self.normalize_people_text(k) in norm_msg:
                        other_fields_requested = True
                        break
            if not other_fields_requested :
                return (
                    "🔒 Şifre gibi kişisel ve gizli bilgiler paylaşılamaz.<br>"
                    "Güvenliğiniz için bu tür taleplerde bulunmamanızı rica ederim."
                )

            sanitized = user_message
            for k in self.SENSITIVE_PASSWORD_KEYWORDS:
                sanitized = sanitized.replace(k, "")

            user_message = sanitized
            msg_norm = self.normalize_people_text(user_message)

        if intent == "today_day":
            return self.handle_today_question(msg_norm)
        
        if self.detect_food_intent(user_message):
            print(" [PROCESS] Yemek menüsü isteği algılandı.")
            target_date = self.resolve_food_date(user_message)
            print(" [PROCESS] Menü tarihi:", target_date)

            intro = self.naturalize_food_intro()
            outro = self.naturalize_food_outro()

            
            if target_date is None:
                body = "🍽 Şu anda sadece <b>bugün</b>, <b>yarın</b> ve <b>sonraki gün</b> için yemek menüsü görüntülenebiliyor."
                return f"{intro}<br>{body}"   

            
            if target_date.weekday() >= 5:
                body = "🍽 Hafta sonları yemek menüsü bulunmamaktadır."
                return f"{intro}<br>{body}"   

            row = self.get_food_menu_for_date(target_date)
            readable = target_date.strftime("%d.%m.%Y")

            if not row:
                body = f"🍽 <b>{readable}</b> için menü bilgisi henüz girilmemiş."
                return f"{intro}<br>{body}"   

            
            body = f"🍽 <b>{readable}</b> menüsü:<br>"
            for i in range(1, 7):
                yemek = row[i-1]
                fiyat = row[6 + i - 1]
                if yemek:
                    line = f"{i}. {yemek}"
                    if fiyat:
                        line += f" — {fiyat} ₺"
                    body += line + "<br>"
            if row[-1]:
                body += f"<br>📝 Not: {row[-1]}"

            return f"{intro}<br>{body}<br>{outro}"
 
        if self.is_plate_add_question(user_message):
            return (
                "🚗 Araç plakanı şu an için profil sayfası üzerinden ekleyebilirsin 😊<br><br>"
                "Profil sayfanda araç bilgileri bölümünden ekleme veya güncelleme yapabilirsin.<br>"
                "Yugii üzerinden plaka ekleme için geliştirmeler ilerleyen dönemde planlanıyor."
            )
        
        if intent == "charge_reservation":
            return self.handle_charge_reservation_redirect()
        
        if intent == "weather":
            return self.handle_weather_redirect(user_message)
    
        if intent == "portal_info":
            return self.handle_portal_info()
        
        if intent == "yuce_auto_reputation":
            return self.handle_yuce_auto_reputation()
         
        if intent == "fun_request":
            return self.handle_fun_intent(user_message)
 
        if intent == "currency_rate":
            return self.handle_currency_rate()
        
        if intent == "currency_calculation":
            return self.handle_currency_calculation(user_message)

        if intent == "department_count":
            return self.handle_department_count()
        
        if intent == "department_list":
            return self.handle_department_list()

        is_link = False

        if (
            intent is None
            and not self.contains_department_word(user_message)
            and not self.looks_like_company_people(user_message)
        ):
            is_link = self.detect_link_intent(user_message)
            print("🧪 [TEST] detect_link_intent:", is_link)

        if intent == "help":
            parsed_help = self.help_user_with_parse(user_message)
            return self.llm_with_handle_help(parsed_help, user_message)
        
        if intent == "people_count_only":
            return self.handle_people_count_only()
        
        if intent == "people_export":
            return self.handle_people_export(user_message, user_info, msg_norm)
        
        if intent == "portal_link":
            return self.find_page_link(user_message)
        
        if intent == "otopark_create":
            return self.handle_otopark_create(user_message, user_info)

        if intent == "otopark_cancel":
            return self.handle_otopark_cancel(user_message, user_info)

        if intent == "otopark_status":
            return self.handle_otopark_status(user_message, user_info)

        if intent == "otopark_status_user":
            return self.handle_otopark_status_user(user_message, user_info)
        
        
        if intent == "haftalik_takvim":
            return self.handle_haftalik_takvim(user_message, user_info)
        
        if intent == "work_history":
            return self.control_work_history(user_message, user_info)

        if intent == "company_people":
            return self.handle_company_people(user_message)
        
        if intent == "cancel_without_context":
            return self.handle_cancel_without_context()
        
        if intent == "monthly_trend_analysis":
            data = self.get_trend_analysis()
            return self.format_trend_response(data)
        
        if intent == "bayi_about":
            return self.hanlde_bayi_about(user_message)

        if intent == "satis_sayisi":
            return self.handle_satis_count(msg_norm)
        
        if intent == "workforce_status":
            result = self.handle_workforce_status(user_message, user_info)
            if result:
                return result
            
        # İşlem niyeti var ama intent net değilse → statik netleştirme
        if (
            intent is None
            and self.detect_haftalik_takvim_intent(user_message)
        ):
            return (
                "Takvimde işlem yapabilmem için gün ve çalışma tipini biraz daha net yazar mısın?<br><br>"
                "Örnekler:<br>"
                "• “Haftaya tüm günler ofis olarak işaretle”<br>"
                "• “Gelecek hafta pazartesi–cuma evden çalışma işaretle”"
            )
        
        if intent is None:
            pop_category = self.detect_pop_culture_category(user_message)
            if pop_category:
                return self.generate_pop_culture_response(pop_category)

        #SMALLTALK → ask_gpt (KONTROLLÜ)
        if self.is_simple_smalltalk(user_message):
            print("🟦 [PROCESS] Smalltalk → ask_gpt")
            return self.ask_gpt(user_message)

        # Genel bilgi asistanı else
        if not self.general_assistant.is_blocked(user_message):

            if self.general_assistant.is_profane(user_message):
                return (
                    "Bu şekilde yardımcı olamam. Sormak istediğiniz farklı bir konu varsa yardımcı olmak isterim 🙂. "
                )

            answer = self.general_assistant.ask(user_message)
            return self.general_assistant.sanitize(answer)
            

        print("hiçbir yere girmiyor return metin.")
        return "Sormak istediğin konuyu biraz daha detaylandırabilir misin? Şuan için ne demek istediğini anlamadım veya bu konuda yetkim yok diyebilirim.🙂"



