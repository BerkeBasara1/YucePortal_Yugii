from .shared import *


class FunPortalInfoMixin:
    def detect_pop_culture_category(self, message: str):
        if not message:
            return None

        m = self.normalize_people_text(message)

        m_compact = m.replace(" ", "")

        for category, keywords in POP_CULTURE_KEYWORDS.items():
            for kw in keywords:
                kw_norm = self.normalize_people_text(kw)
                kw_compact = kw_norm.replace(" ", "")

                if kw_norm in m:
                    return category

                if kw_compact in m_compact:
                    return category

                score = fuzz.partial_ratio(m_compact, kw_compact)
                if len(kw_compact) >= 6 and score >= 85:
                    return category

        return None

    
    def generate_pop_culture_response(self, category: str):
        RESPONSES = {
            "the_office": [
                "😄 Bunu yazdığına göre The Office hayranı olabilirsin. Michael Scott modu kapalı ama ben buradayım 🙂",
                "The Office referansını yakaladım. Peki sana nasıl yardımcı olayım?"
            ],
            "himym": [
                "😎 Legendary dedin… How I Met Your Mother sevenlerden misin?",
                "HIMYM havası aldım 🙂 Bugünün efsane geçmesini dilerim?"
            ],
            "friends": [
                "☕ Bunu yazan biri büyük ihtimalle Friends izleyicisidir 🙂",
                "😄 Joey tarzı bir selam yakaladım. Ben iyiyim, sana nasıl yardımcı olayım?"
            ],
            "got": [
                "❄️ Bunu yazan biri Game of Thrones izlemiştir diye tahmin ediyorum 🙂",
                "Kış geliyor havası aldım ama burada işler net ilerliyor 😄"
            ],
            "batman": [
                "🦇 Gotham havası sezdim 🙂 Ben Batman değilim ama yardımcı olabilirim."
            ],
            "harry_potter": [
                "🪄 Harry Potter evrenini sevdiğini fark ettim 🙂 Ama ben daha çok portal işlerinde güçlüyüm."
            ],
            "se7en": [
            "😅 O sahneyi hatırladım… Seven izleyenler genelde bunu kaçırmaz.",
            "🎬 Bu repliği yazan biri muhtemelen Seven izlemiştir. Merak uyandırıcı bir sahneydi. Peki sana nasıl yardımcı olabilirim🙂"
        ]
        }
        return random.choice(RESPONSES.get(category, []))
    
    
    def handle_fun_intent(self, user_message: str):

        pop_category = self.detect_pop_culture_category(user_message)
        if pop_category:
            return self.generate_pop_culture_response(pop_category)

        JOKES = [
            
            "😄 Kısa bir ara ver ki, bilgisayar senden önce pes etmesin.",
            "😄 Bir kahve molası ver, en azından kahve seni yarı yolda bırakmaz.",
            "😄 Ayağa kalkıp iki adım yürü, sandalyeyle aranı biraz soğut.",
            "😄 Bir mola ver, belki çözüm dönünce seni bekliyordur.",
            "😄 Kısa bir ara ver; işler kaçmıyor ama sen kaçabilirsin.",
            "😄 Bir su iç, bilgisayar değilsen yeniden başlatmaya gerek yok."
        ]

        return random.choice(JOKES)
     

