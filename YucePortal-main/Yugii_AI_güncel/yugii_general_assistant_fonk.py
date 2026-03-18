# modules/ai/general_assistant_fonk.py

import os
from openai import OpenAI
from config import OPENAI_API_KEY


def _build_openai_client():
    if not OPENAI_API_KEY:
        return None
    try:
        return OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        return None


class GeneralAssistant:
    """
    Sadece GENEL BİLGİ ve SMALLTALK FALLBACK için kullanılır.
    Yugii Brain AI'nin core logic'ine ASLA dokunmaz.
    """

    INTENT_METADATA = {
        "haftalik_takvim": "Haftalık takvim ve çalışma planı görüntüleme işlemleri.",
        "workforce_status": "Belirli tarih veya bağlamda çalışanların ofis, home, bayi durum sorgusu.",
        "work_history": "Geçmiş çalışma günleri ve gün sayısı sorguları.",
        "company_people": "Tek çalışan bilgisi görüntüleme.",
        "people_count_only": "Şirket genelindeki toplam aktif çalışan sayısı sorgusu.",
        "department_count": "Belirli bir departmandaki kişi sayısı sorgusu.",
        "department_list": "Şirketteki departmanların listelenmesi.",
        "people_export": "Departman veya toplu çalışan listesi export işlemleri.",
        "portal_link": "Portal içindeki belirli bir sayfaya yönlendirme.",
        "portal_info": "Yüce Portal hakkında genel bilgi.",
        "otopark_create": "Otopark rezervasyonu oluşturma.",
        "otopark_cancel": "Otopark rezervasyonu iptal etme.",
        "otopark_status": "Otopark müsaitlik durumu sorgulama.",
        "otopark_status_user": "Kullanıcının kendi otopark rezervasyonunu sorgulaması.",
        "charge_reservation": "Elektrikli araç şarj rezervasyonu işlemleri.",
        "currency_rate": "Güncel döviz kuru sorgulama.",
        "currency_calculation": "Döviz hesaplama işlemleri.",
        "weather": "Hava durumu sorgulama.",
        "yemek_menu": "Kafeterya yemek menüsü sorgulama.",
        "assistant_capabilities": "Asistanın rol ve yetenek bilgisi.",
        "yuce_auto_reputation": "Yüce Auto hakkında genel kurumsal bilgi.",
    }
    def __init__(self):
        self.client = _build_openai_client()

        # 🚫 ŞİRKET / HR / INTERNAL BLOK
        self.blocklist = [
            "maaş", "ücret", "izin", "personel",
            "çalışan", "departman", "yüce",
            "skoda", "şirket", "ik", "hr",
            "bordro", "yönetici"
        ]

        # 🚫 KÜFÜR / TOKSİK
        self.profanity = [
            "salak", "aptal", "küfür", "lan", "mal","argo",
        ]

        # 🚫 MODEL CEVABINDA OLMAMASI GEREKENLER
        self.forbidden_output = [
            "veritabanımız","maaş","ücret",
            "maaş bilgisi",
        ]


    def build_system_prompt(self) -> str:
        intent_lines = "\n".join(
            [f"- {k}: {v}" for k, v in self.INTENT_METADATA.items()]
        )

        return f"""
    Sen Yugii’sin, Yüce Auto’nun kurumsal dijital asistanısın.

    Eğer kullanıcı rolünü veya ne yaptığını sorarsa,
    SADECE şu cümleyi aynen yaz:

    "Ben Yüce Auto’nun kurumsal dijital asistanı Yugii’yim. Otopark rezervasyonu, haftalık takvim, çalışan bilgileri ve portal işlemlerinde yardımcı olurum."
        
    DESTEKLENEN MODÜLLER:
    {intent_lines}

    ROL SINIRI:
    - İşlem yapmazsın.
    - İşlem yaptığını ima etmezsin.
    - Uydurma bilgi üretmezsin.
    - İç sistem veya yetkilerden bahsetmezsin.

    DAVRANIŞ:

    1) Eğer kullanıcı mesajı yukarıdaki modüllerden biriyle ilişkiliyse fakat eksik veya belirsizse:
    - Mesajı kısaca yansıt.
    - Nazikçe detay iste.
    - “Yardımcı olamam” deme.

    2) Eğer mesaj yukarıdaki modüllerle açıkça ilişkili değilse
    ve hiçbir modüle makul şekilde bağlanamıyorsa:
    - Konunun desteklenen alanlar dışında kaldığını belirt ve daha detaylı yada başka bir şekilde yardımcı olabileceğini söyle sorusuna göre.
    - Yanlış umut verme.

    3) Araç teknik, fiyat, marka kıyas, rakip firma, siyaset veya ticari analiz yapma.

    CEVAP:
    - Türkçe
    - 1–2 kısa cümle
    
    """
    # --------------------------------------------------
    # 🔒 PRE FILTER
    # --------------------------------------------------
    def is_blocked(self, msg: str) -> bool:
        msg = msg.lower()
        return any(k in msg for k in self.blocklist)

    def is_profane(self, msg: str) -> bool:
        msg = msg.lower()
        return any(k in msg for k in self.profanity)

    # --------------------------------------------------
    # 🤖 LLM CALL
    # --------------------------------------------------
    def ask(self, user_message: str) -> str:
        if self.client is None:
            return "Bu isteği biraz daha net yazarsan yardımcı olmayı deneyebilirim."

        system_prompt = self.build_system_prompt()

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            max_tokens=120,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        raw = response.choices[0].message.content.strip()
        return self.sanitize(raw)


    # --------------------------------------------------
    #  POST FILTER
    # --------------------------------------------------
    def sanitize(self, text: str) -> str:
        t = text.lower()

        forbidden_phrases = [
            "yaptım", "işaretledim", "ekledim", "ayarladım",
            "ilgileniyorum", "hallederim", "kontrol ediyorum",
            "işleme aldım", "tamamlandı", "gerçekleştirildi",
            "oluşturuldu", "kaydedildi", "güncellendi"
        ]

        # Şirket / iç veri sızıntısı
        if any(k in t for k in self.forbidden_output):
            return (
                "Bu konu şirket içi bir işlemle ilgili olduğu için "
                "buradan yardımcı olamıyorum. 🙂<br><br>"
                "İstersen genel bir konuda bilgi verebilirim "
                "ya da başka bir şey sorabilirsin."
            )

        #  İŞLEM YAPIYORMUŞ GİBİ KONUŞMA YASAĞI
        if any(k in t for k in forbidden_phrases):
            return (
                "Bu isteği şu an buradan yerine getiremiyorum. 🙂<br><br>"
                "Başka bir konuda yardımcı olmamı ister misin? "
                "Genel bilgi, günlük konular veya merak ettiğin farklı bir şey olabilir."
            )

        return text

