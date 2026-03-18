ALLOWED_COLUMNS = [
    "name",
    "surname",
    "username",
    "email",
    "departman",
    "title",
    "TelNo",
    "plaka",
    "arac_plaka2",
    "arac_marka",

    "dogum_gun",
    "dogum_ay",
    "Kidem_Tarihi",
    "linkedin",
]

EXPORT_PRESETS = {
    # 👤 En basit: çalışan listesi
    "basic_list": [
        "name",
        "surname"
    ],

    # 🏢 Şirket çalışanları
    "company_list": [
        "name",
        "surname",
        "departman"
    ],

    # 📞 İletişim
    "contact": [
        "name",
        "surname",
        "email",
        "TelNo"
    ],

    # 🖥️ Sistem / kullanıcı
    "system": [
        "name",
        "surname",
        "username"
    ],

    # 🚗 Araç bilgileri
    "vehicle": [
        "name",
        "surname",
        "plaka",
        "arac_marka"
    ],

    "all_allowed": ALLOWED_COLUMNS
}

PEOPLE_DB_FIELDS = [
    "name",
    "surname",
    "username",
    "email",
    "departman",
    "title",
    "TelNo",
    "linkedin",
    "dogum_gun",
    "dogum_ay",
    "Kidem_Tarihi"
]
#exel verdiği fix bilgi
CORE_REQUIRED_COLUMNS = [
    "name",
    "surname"
]
