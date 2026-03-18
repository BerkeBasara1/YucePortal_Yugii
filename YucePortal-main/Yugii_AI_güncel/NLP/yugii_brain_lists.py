# yugii_brain_lists.py
POP_CULTURE_KEYWORDS = {
    "the_office": [
        "that's what she said",
        "thats what she said"
    ],
    "himym": [
        "legendary","legendaryy"
    ],
    "friends": [
        "we were on a break",
        "how you doin"
    ],
    "got": [
        "winter is coming"
    ],
    "batman": [
        "i'm batman",
        "im batman"
    ],
    "harry_potter": [
        "avada kedavra",
        "expelliarmus","abra kadabra",
        "hogwarts",
        "voldemort",
        "muggle"
    ],
    "se7en": [
        "what's in the box",
        "whats in the box",
        "what is in the box",
        "what's in the box"
    ],
}
# === TIME / CALENDAR KEYWORDS ===

NEXT_WEEK_KEYS = [
    "haftaya","gelecek hafta","gelecekhafta","önümüzdeki hafta","onumuzdeki hafta","önümüzdekihafta",
    "birdahaki hafta","bir dahaki hafta","bi dahaki hafta","öbür hafta","obur hafta",
    "haftya","hafatya","hftaya","hafty","haftayaa","haftyaa","haftayae",
    "onumuzdeki","onumuzdek hafta","onumudeki hafta",
    "next week","nextweek","next wk","nxt week",
    "gelecek günler","önümüzdeki günler","önümüzdeki pazartesi"
]

FULL_KEYS = [
    "tum gunler","tüm günler","tumgunler","tümgünler",
    "hafta ici","hafta içi","haftaici","haftaiçi",
    "full","ful","fll","komple","komplett","komplet","komplette",
    "tamami","tamamı","tamamiyle","tamamiyla","tamamıyla","tamamiyle",
    "hepsi","hepsini","hepisi","heps",
    "butun","bütün","butunu","butun gunler","bütün günler","komple",
    "her gun","her gün","hergün","hergun",
    "tam gun","tam gün","tamyun","tamyün"
]
FULL_MONTH_KEYS = [
    "komple",
    "boyunca","komple", "boyunca", "tamami", "tamamı",
    "tamami", "tamamı",
    "tumu", "tümü",
    "hepsi",
    "full",

    # 🔥 kritik doğal konuşmalar
    "her gun", "her gün",
    "hergun", "hergün",
    "tum gunler", "tüm günler",
    "gunlerin tamami", "günlerin tamamı",
    "ay boyunca",
    "ayi boyunca",
    "ayindaki gunler", "ayındaki günler",
    "ayin her gunu", "ayın her günü"
]
# ==============================
# 📅 BU HAFTA + GÜN ANCHOR’LARI
# ==============================


PAZARTESI_VARIANTS = ["pazartesi","pazartes","pazrtesi","pzartesi","pazertes","pazartesi̇","pzt","pzrt","pzrts","pzrtesi","pazrtsi","pazrtes","pazartesii","pazartesı","pazrts","paazartesi","pazrt","paztesi"]

SALI_VARIANTS = ["salı","sali","salıi","salıı","sal","sl","sli","saali","salii","slı","salıya","salıdan","salıda","sall","cali","şali"]

CARSAMBA_VARIANTS = ["çarşamba","carsamba","carsmba","crsmb","crsb","crsamba","çarsamba","çarsmba","çarşmaba","cars","crs","csb","carsmaba","carsmbe","carsmb","çrşmba","çrşnaba","carsnaba"]

PERSEMBE_VARIANTS = ["perşembe","persembe","perşmbe","per","prs","prsb","persmbe","prsembe","persmebe","perşembee","persembeee","perşembeee","prşmbe","prşembe","perşembeya"]

CUMA_VARIANTS = ["cuma","cum","cm","cumaa","cuuma","cma","cummaa","cumaaa"]

CUMARTESI_VARIANTS = ["cumartesi","cumrtesi","cumartes","cumartesii","cumrtsi","cumaratesi","cmt","cmrts","cmrt","cumartesı","cumartesi̇"]

PAZAR_VARIANTS = ["pazar","paz","pzr","pazarr","paazar","pazaar","pazzar","pazr","pazarrr"]

ALL_WEEKDAY_VARIANTS = (
    PAZARTESI_VARIANTS
    + SALI_VARIANTS
    + CARSAMBA_VARIANTS
    + PERSEMBE_VARIANTS
    + CUMA_VARIANTS
    + CUMARTESI_VARIANTS
    + PAZAR_VARIANTS
)

DIGER_KEYS = [
    "diğer",
    "diger",
    "dığer",
    "dger",
    "kalan",
    "geri kalan",
    "geriye kalan",
    "diğerleri",
    "kalan günler"
]

BU_WEEK_DAY_PREFIXES = [
    "bu","bu hafta","buhfta","buhafta","bu hf","buhaft","this week","thisweek","bu hafta","b hafta","bu hfta","bu haft"
]

NEXT_WEEK_KEYS = [
    "haftaya","hafty","hftaya","next week","onumuzdeki hafta","onumzüde ki hafta","hftya","hftyaa",
    "gelecek hafta",
    "gelecekhafta",
    "önümüzdeki hafta",
    "onumuzdeki hafta"
]
# 🔥 HER GÜN / HER GÜNE / HER BİR GÜN (GENİŞ + YAZIM HATALI)
EVERY_DAY_KEYS = [
    # --- doğru yazımlar ---
    "her gun", "her gün",
    "hergün", "hergun",
    "her güne", "hergüne",
    "her bir gun", "her bir gün","her gunu", "her günü",
    "her bir günü",
    "gun gun", "gün gün",
    "ay boyunca her gun", "ay boyunca her gün",
    "her bir güne",
    "tum gunler", "tüm günler",
    "tum gun", "tüm gün",
    "ayinin tamami", "ayının tamamı",
    "ayi boyunca", "ayı boyunca",
    "ayi icinde", "ayı içinde",
    # --- birleşik / konuşma dili ---
    "hergune", "hergunee","hw gün","he gun",
    "herbirgun", "herbir gün",
    "herbirkün",
    "hergunluk", "hergunluk",
    "gunluk her", "günlük her",

    # --- yazım hataları ---
    "her gn", "her gunn", "her gunu",
    "her gune", "her gunn",
    "her günu", "her günn",
    "her gunee", "her güneee","her gunu", "her günü",
    "her bir günü",
    "gun gun", "gün gün",
    "her br gun", "her bir gn",
    "her bir gunn",
    "ay boyunca her gun",
    "ayi boyunca her gun",
    "ay icinde her gun",
    "ayi icinde her gun",
    # --- eksik / devrik ---
    "gunlerin hepsi", "günlerin hepsi",
    "butun gunler", "bütün günler",
    "herzaman gun", "her zaman gun",

    # --- haftalık bağlam destek ---
    "hafta boyunca",
    "haftanin tamami", "haftanın tamamı",
    "hafta full", "hafta komple",

    # --- aylık bağlam destek ---
    "ay boyunca",
    "ayin tamami", "ayın tamamı",
    "ay full", "ay komple"
]


# === DEPARTMENT WORD VARIANTS ===
DEPARTMENT_WORD_VARIANTS = [
    "departman","depatman","departmanlar",
    "departmn","departmanı","departmanında","departmannda",
    "departmen",
    "deparman",
    "depertman",
    "departmant","deparmtan","depatman","depattman","departman",
    "dpartman",
    "depatman",
    "dept",
    "depart",
    "depman",
]

CURRENCY_KEYWORDS = [
    "doviz", "döviz", "kur", "kuru", "kurlar",
    "euro", "eur", "avro",
    "dolar", "usd",
    "euro kac", "euro kaç",
    "dolar kac", "dolar kaç",
    "bugunku kur", "bugünkü kur",
    "anlik kur", "anlık kur",
    "doviz kuru", "döviz kuru",
    "euro tl", "eur tl",
    "usd tl", "dolar tl"
]
DEPARTMENT_COUNT_HINTS = [
    "kac", "kaç",
    "adet", "adedi",
    "sayi", "sayisi", "sayısı",
    "toplam",  "toplamı",
    "tane"
]

DEPARTMENT_LIST_HINTS = [
    # temel
    "neler", "nelerdir",
    "hangileri", "hangiler",
    "hangi", "hangi var", "hangi departmanlar",
    # çeşit / tür
    "cesit", "cesidi", "cesitleri",
    "tür", "turu", "turleri",
    "farkli", "farkli olan",
    # listeleme dili
    "sirketteki", "şirketteki","hangi", "hangileri", "nelerdir", "neler", "çeşitleri",
    "ofisteki", "ofiste",
    "organizasyondaki",
    "yapida", "yapida yer alan"
]

YUCE_AUTO_REPUTATION_ROOTS = [
    "yuce auto","yuce autoddaki","yuce autoda","yuce auto'nun","yuce auto'da ki","yuce autonun","yuce autonun",
    "yuce auto",
    "yuce oto",
    "yuce oto",
    "firma","kurum","kurumumuz",
    "sirket","skoda",
    "şirket","şirketimiz","firma","burası","firmamız","yüce auto","yüceauto","yuceauto","yuce outo"
]

YUCE_AUTO_REPUTATION_QUESTIONS = [
    # nasıl / tanım
    "nasil",
    "nasıl",
    "nasil bir",
    "nasıl bir",

    # kalite / iyi mi
    "iyi mi",
    "iyi",
    "basarili",
    "başarılı",
    "guclu",
    "güçlü","nasıl bir yer","nasıl bir şirket"

    # görüş / fikir
    "gorusun",
    "görüşün",
    "fikrin",
    "fikir",
    "dusuncen",
    "düşüncen",
    "ne dusunuyorsun",
    "ne düşünüyorsun",

    # kariyer / çalışma
    "kariyer",
    "calisma ortami",
    "çalışma ortamı",
    "calisanlar icin",
    "çalışanlar için",
    "is ortami",
    "iş ortamı",

    # genel bilgi
    "hakkinda",
    "hakkında","hakkındaki","hakkında ki","alakalı","ilgili","ile ilgili",
    "bilgin",
    "bilgi",
    "tanit",
    "tanıt",
    "anlat",
    "kisa bilgi","hakkındakiler","hakkında",
    "kısaca","fikrin nedir","fikrin","nasıl bir şirket","nasıl bir yer","hakkında","bilgi ver","bilgi"

]
WORK_HISTORY_COUNT_KEYS = [
    # çekirdek
    "kac", "kaç","kaç gün","kac gün","kac gun","kç gun","kaç gn","kaç güün",
    "ne kadar",
    "toplam",
    "say", "sayi", "sayisi", "sayısı",

    # gün odaklı
    "kac gun", "kaç gün",
    "gun sayisi", "gün sayısı",
    "gunum", "gunlerim", "günlerim",

    # tekrar / frekans
    "kac kere", "kaç kere",
    "kac defa", "kaç defa",
    "kac kez", "kaç kez",

    # doğal dil
    "ne kadar geldim",
    "ne kadar calistim",
    "ne kadar izin aldim",
    "toplam kac gun",
    "toplam ne kadar",

    # eksik / bozuk yazımlar
    "kacgn", "kcgün", "kcgün",
    "nekadar", "nekdr",
    "toplm", "toplm kac",
]
AY_NORMALIZE = {
    #  Ocak
    "oc": "ocak", "oca": "ocak", "ocag": "ocak", "ocak": "ocak", "ocagı": "ocak",
    "ocagi": "ocak", "ocagim": "ocak", "ocagın": "ocak", "ocaginda": "ocak","ocağın":"ocak","ocağa":"ocak",

    #  Şubat
    "sub": "şubat", "şub": "şubat", "subat": "şubat", "şubat": "şubat",
    "subaat": "şubat", "subatt": "şubat", "subad": "şubat", "suba": "şubat","şubata":"şubat","subata":"şubat",

    # Mart
    "mar": "mart", "martt": "mart", "martı": "mart", "mrt": "mart",

    #  Nisan
    "nis": "nisan", "nıs": "nisan", "nisn": "nisan", "nisan": "nisan",
    "nısan": "nisan", "nıssan": "nisan", "nısn": "nisan",

    #  Mayıs
    "may": "mayıs", "mayis": "mayıs", "mayıs": "mayıs",
    "mays": "mayıs", "mayiz": "mayıs", "mayss": "mayıs", "mayiss": "mayıs",

    #  Haziran
    "haz": "haziran", "hazi": "haziran", "hazir": "haziran", "hazrn": "haziran",
    "haziran": "haziran", "haziarn": "haziran", "hazirn": "haziran",

    #  Temmuz
    "tem": "temmuz", "temm": "temmuz", "temuz": "temmuz", "temmuz": "temmuz",
    "temuz": "temmuz", "temmız": "temmuz", "temmuz": "temmuz",

    #  Ağustos
    "agu": "ağustos", "ağu": "ağustos", "agust": "ağustos", "ağust": "ağustos",
    "agustos": "ağustos", "ağustos": "ağustos", "agusts": "ağustos", "ağusts": "ağustos",
    "august": "ağustos", "aug": "ağustos", "ağustoz": "ağustos",

    #  Eylül
    "eyl": "eylül", "eylu": "eylül", "eylul": "eylül", "eylül": "eylül",
    "eylulü": "eylül", "eyül": "eylül", "eyüll": "eylül", "eylülün": "eylül",

    #  Ekim
    "ek": "ekim", "ekm": "ekim", "ekım": "ekim", "ekim": "ekim",
    "ekmim": "ekim", "ekımm": "ekim", "ekimm": "ekim", "ekın": "ekim",

    #  Kasım
    "kas": "kasım", "kasim": "kasım", "kasım": "kasım", "kası": "kasım",
    "kasm": "kasım", "kasın": "kasım", "kasımm": "kasım", "kasınm": "kasım",

    #  Aralık
    "ara": "aralık", "aral": "aralık", "arl": "aralık", "aralık": "aralık",
    "aralik": "aralık", "arlk": "aralık", "aralhk": "aralık", "aralıkta": "aralık"
}

WEATHER_KEYWORDS = [
    "hava",
    "hava durumu",
    "kac derece",
    "bugun hava",
    "yarin hava",
    "hava nasil","hava",
    "hava durumu",
    "kac derece",
    "bugun hava",
    "yarin hava",
    "hava nasil",
    "derece",
    "hava nasıl",
    "hava nsl",
    "hava güzelmi",
    "hava güzel mi",
    "derece","hava nasıl","hava nsl","hava güzelmi","hava güzel mi"
]

CHARGE_ROOTS = [
    "sarj", "şarj","saj"
]

CHARGE_ACTIONS = [
    "rezervasyon", "rezerve", "ayir", "ayir", "ayirma","istasyonu","yeri","bul","ayr","rez et","rez","rezv","rezv et","rezv ","rezervasyonu"
]  
known_cities = [
    # 🔹 İstanbul ilçeleri
    "kadıköy", "üsküdar", "beşiktaş", "şişli", "fatih", "beyoğlu", "beykoz",
    "ataşehir", "maltepe", "pendik", "tuzla", "kartal", "bakırköy", "avcılar",
    "beylikdüzü", "silivri", "arnavutköy", "sarıyer", "zeytinburnu", "bayrampaşa",
    "gaziosmanpaşa", "esenler", "bağcılar", "küçükçekmece", "başakşehir", "sancaktepe",
    "ümraniye", "eyüpsultan", "sultanbeyli", "bahçelievler", "esenyurt", "kağıthane",
    "çatalca", "adalar", "bostancı",

    # 🔹 81 il
    "adana", "adıyaman", "afyonkarahisar", "ağrı", "amasya", "ankara", "antalya", "artvin",
    "aydın", "balıkesir", "bilecik", "bingöl", "bitlis", "bolu", "burdur", "bursa",
    "çanakkale", "çankırı", "çorum", "denizli", "diyarbakır", "edirne", "elazığ",
    "erzincan", "erzurum", "eskişehir", "gaziantep", "giresun", "gümüşhane", "hakkari",
    "hatay", "ısparta", "mersin", "istanbul", "izmir", "kars", "kastamonu", "kayseri",
    "kırklareli", "kırşehir", "kocaeli", "konya", "kütahya", "malatya", "manisa",
    "kahramanmaraş", "mardin", "muğla", "muş", "nevşehir", "niğde", "ordu", "rize",
    "sakarya", "samsun", "siirt", "sinop", "sivas", "tekirdağ", "tokat", "trabzon",
    "tunceli", "şanlıurfa", "uşak", "van", "yozgat", "zonguldak", "aksaray", "bayburt",
    "karaman", "kırıkkale", "batman", "şırnak", "bartın", "ardahan", "ığdır", "yalova",
    "karabük", "kilis", "osmaniye", "düzce"
]
cities = {
    # 🔹 İstanbul ilçeleri
    "kadikoy": (40.9929, 29.0281),
    "uskudar": (41.0220, 29.0157),
    "besiktas": (41.0430, 29.0081),
    "sisli": (41.0600, 28.9870),
    "fatih": (41.0122, 28.9558),
    "beyoglu": (41.0369, 28.9768),
    "beykoz": (41.1445, 29.0983),
    "ataşehir": (40.9925, 29.1273),
    "maltepe": (40.9395, 29.1554),
    "pendik": (40.8700, 29.2700),
    "tuzla": (40.8150, 29.3050),
    "kartal": (40.8990, 29.1870),
    "bakirkoy": (40.9780, 28.8670),
    "avcilar": (40.9794, 28.7213),
    "beylikduzu": (40.9923, 28.6418),
    "silivri": (41.0748, 28.2452),
    "arnavutkoy": (41.1990, 28.7400),
    "sariyer": (41.1700, 29.0500),
    "zeytinburnu": (40.9915, 28.9075),
    "bayrampasa": (41.0380, 28.9040),
    "gaziosmanpasa": (41.0610, 28.9170),
    "esenler": (41.0330, 28.8900),
    "bagcilar": (41.0395, 28.8567),
    "kucukcekmece": (41.0007, 28.7776),
    "basaksehir": (41.1027, 28.8006),
    "sancaktepe": (41.0000, 29.2500),
    "umraniye": (41.0160, 29.1250),
    "eyupsultan": (41.0800, 28.9300),
    "arnavutkoy": (41.1830, 28.7420),
    "sultanbeyli": (40.9690, 29.2690),
    "bahcelievler": (40.9920, 28.8550),
    "esenyurt": (41.0275, 28.6735),
    "beykoz": (41.1350, 29.1000),
    "kagithane": (41.0750, 28.9750),
    "catalca": (41.1469, 28.4644),
    "adalar": (40.8708, 29.0971),
    # 🔹 81 il
    "adana": (37.0000, 35.3213),
    "adiyaman": (37.7648, 38.2786),
    "afyon": (38.7638, 30.5403),
    "agri": (39.7191, 43.0503),
    "amasya": (40.6539, 35.8333),
    "ankara": (39.9208, 32.8541),
    "antalya": (36.8841, 30.7056),
    "artvin": (41.1828, 41.8183),
    "aydin": (37.8450, 27.8396),
    "balikesir": (39.6484, 27.8826),
    "bilecik": (40.1500, 29.9833),
    "bingol": (38.8853, 40.4983),
    "bitlis": (38.4000, 42.1167),
    "bolu": (40.7395, 31.6116),
    "burdur": (37.7269, 30.2889),
    "bursa": (40.1826, 29.0669),
    "canakkale": (40.1450, 26.4064),
    "cankiri": (40.6000, 33.6167),
    "corum": (40.5506, 34.9556),
    "denizli": (37.7765, 29.0864),
    "diyarbakir": (37.9144, 40.2306),
    "edirne": (41.6667, 26.5667),
    "elazig": (38.6743, 39.2226),
    "erzincan": (39.7500, 39.5000),
    "erzurum": (39.9000, 41.2700),
    "eskisehir": (39.7843, 30.5192),
    "gaziantep": (37.0662, 37.3833),
    "giresun": (40.9128, 38.3895),
    "gumushane": (40.4603, 39.4817),
    "hakkari": (37.5833, 43.7333),
    "hatay": (36.2000, 36.1667),
    "isparta": (37.7648, 30.5566),
    "mersin": (36.8000, 34.6333),
    "istanbul": (41.0082, 28.9784),
    "izmir": (38.4192, 27.1287),
    "kars": (40.6167, 43.1000),
    "kastamonu": (41.3887, 33.7827),
    "kayseri": (38.7312, 35.4787),
    "kirklareli": (41.7333, 27.2167),
    "kirsehir": (39.1500, 34.1667),
    "kocaeli": (40.8533, 29.8815),
    "konya": (37.8667, 32.4833),
    "kutahya": (39.4167, 29.9833),
    "malatya": (38.3552, 38.3095),
    "manisa": (38.6191, 27.4289),
    "kahramanmaras": (37.5736, 36.9371),
    "mardin": (37.3122, 40.7351),
    "mugla": (37.2153, 28.3636),
    "mus": (38.7433, 41.5069),
    "nevsehir": (38.6247, 34.7143),
    "nigde": (37.9667, 34.6833),
    "ordu": (40.9833, 37.8833),
    "rize": (41.0201, 40.5234),
    "sakarya": (40.7569, 30.3784),
    "samsun": (41.2928, 36.3313),
    "siirt": (37.9333, 41.9500),
    "sinop": (42.0231, 35.1531),
    "sivas": (39.7477, 37.0179),
    "tekirdag": (40.9833, 27.5167),
    "tokat": (40.3167, 36.5500),
    "trabzon": (41.0015, 39.7178),
    "tunceli": (39.1075, 39.5475),
    "sanliurfa": (37.1591, 38.7969),
    "usak": (38.6823, 29.4082),
    "van": (38.4942, 43.3831),
    "yozgat": (39.8200, 34.8147),
    "zonguldak": (41.4500, 31.8000),
    "aksaray": (38.3725, 34.0254),
    "bayburt": (40.2603, 40.2280),
    "karaman": (37.1811, 33.2150),
    "kirikkale": (39.8468, 33.5153),
    "batman": (37.8812, 41.1351),
    "sirnak": (37.5133, 42.4540),
    "bartin": (41.6333, 32.3375),
    "ardahan": (41.1105, 42.7022),
    "igdir": (39.9167, 44.0333),
    "yalova": (40.6550, 29.2769),
    "karabuk": (41.2000, 32.6333),
    "kilis": (36.7184, 37.1212),
    "osmaniye": (37.0742, 36.2470),
    "duzce": (40.8438, 31.1565)
}
HELP_ACTION_KEYS = [
    "nasil yaparim", "nasıl yaparım",
    "nasil yapabilirim", "nasıl yapabilirim",
    "nasıl yapılır",
    "nasıl ayarlarım",
    "nasıl işaretlerim",
    "nasıl iptal ederim",
    "yardım", "yardim",
    "yardım eder misin", "yardim eder misin",
    "mümkün mü", "mumkun mu"
]

EXPORT_HINTS = [
    "liste", "listele", "liste ver","listesi",
    "excel", "exel",
    "title", "unvan",
    "sırala","dök","göster","list"
]

FUN_REQUEST_KEYWORDS = [
    "komik bir sey soyle","espiri yap","şaka yap","espiri patlat","espiri yap","esipiri yap","paylai espiri","espirii yap","saka yap","espirilimisin",
    "komik bisey soyle","şaka patlat","espiri","sakala","şakala"
    "beni guldur",
    "bir saka yap",
    "espri yap",
    "komiklik yap",
    "komik bi sey",
    "komik bir sey",
    "komik sey",
    "beni biraz eglendir",
    "moral ver"
] 

TODAY_DAY_KEYS = [
    "bugun gunlerden ne",
    "bugun hangi gun",
    "bugun ne gun",
    "bugun gun ne",    
    "yarin gunlerden ne",
    "yarin hangi gun",
    "yarin ne gun",
    "hangi gundeyiz","hangi gündeyiz","hangi gün bugün",
    "bugun gundeyiz","bugün hangi gün","bu gün ne günü","haftanın hangi günündeyiz","yarın günlerden ne","yarın hangi gün"
    ]
ALL_PEOPLE_KEYWORDS = [
    

    "herkes","herkesin","tüm çalışanlar", "tum calisanlar","tüm departmanlar","tüm departmnlar","tüm departman","tüm departmn","tüm çlşanlar",
    "tüm personel", "tum personel","tüm şirket","tüm personel","tüm personellerin","tüm çalışan","çalışanların","personellerin",
    "tüm kişiler", "tum kisiler","tum çalısan",
    "şirketteki herkes", "sirketteki herkes","tüm şirket çalışanları","şirketteki herkesin","herkesin","tüm şirketin",
    "şirketin tamamı","ofisteki herkes", "ofiste çalışan herkes","tüm calısan","çalışan","tüm çalşanlar",
    "iş yerindeki herkes", "isyeri calisanlari",   "çalışanlar", "calisanlar","tum calisanlar",
    "personel", "tüm personel","kişiler", "tüm kişiler","tüm herkes","herkes","tüm personel","personeller","personellerin","tüm personeller","tüm personellerin",
    "herkes", "şirketteki herkes","şirketteki kişiler","herkesin","herkezin","sirket","çalışanların","tüm çalışanların",
    "tum sirket","herkes","calisanlar","çalışanlar","şirketteki herkes","şirketteki herkes","sirketin","tum sirketin","tum sirket","tüm şirket","tum sirketin","tüm şirketin"
]
SCOPE_WORDS = [
    # tüm / hepsi
    "tum", "tüm", "tmm", "tm","her",
    "hepsi", "hepisi", "heps",
    "tamami", "tamamı", "tamamiyle", "tamamıyla",

    # herkes
    "herkes", "herkees", "herkezin", "herkesin",

    # şirket / işyeri
    "sirket", "şirket", "sirketin", "şirketin",
    "tum sirket", "tüm şirket",
    "isyeri", "is yeri", "işyeri", "iş yeri",
    "isyeri", "isyeri",
    "ofisteki", "ofiste",
    "şirketteki", "sirketteki"
]

PEOPLE_WORDS = [
    # çalışan kökü
    "calisan", "çalisan", "çalışan",
    "calisanlar", "çalisanlar", "çalışanlar",
    "calisanin", "çalisanin", "çalışanın",
    "calısan", "çalısan", "çlşan", "çlşanlar",
    "çalşan", "çalışn",

    # personel kökü
    "personel", "personeller", "personellerin",
    "persnel", "perssonel", "personl",
    "prsnel",

    # kişi kökü
    "kisi", "kişi",
    "kisiler", "kişiler",
    "kisilerin", "kişilerin",
    "kiler", "kişlr",

    # ekip / insanlar
    "ekip", "ekibi", "ekiptekiler",
    "insanlar", "insnlar"
]

KIDEM_INTENT_KEYWORDS = [
    "kidem",
    "kıdem",
    "kidem tarihi",
    "kıdem tarihi",
    "ne zamandir",
    "ne zamandır","ne zamman","ne zmaan","ne zmaandır",
    "kac yildir",
    "kaç yıldır",
    "ne kadar zamandir",
    "ne kadar zamandır",
    "burada ne zamandir",
    "burada ne zamandır",
    "sirkette ne zamandir",
    "şirkette ne zamandır",
    "bizimle ne zamandir",
    "bizimle ne zamandır",

    "ne zaman basladi",
    "ne zaman başladı",
    "ise ne zaman basladi",
    "işe ne zaman başladı",
    "ise giris tarihi",
    "işe giriş tarihi",
    "ise baslama tarihi","ne zamandr","ne zmndr","ne kadrdır","ne kadardır",
    "işe başlama tarihi","ne zaman başladı","ne zmaandr","ne zamaandr","ne zamandr","ne zamaandr"
]
USER_PARK_STATUS_KEYS = [
# klasik
"rezervasyonum", "rezervasyonlarım","yaptigim", "yaptığım","otoparkda yaptığım","otoparkta yaptığım","ayırdığım yerler",
"ayirdigim", "ayırdığım",
"rezervasyonlarim","rezervasyonlarım",
"yerlerim", "parklarim", "parklarım",
"larim","lerim",
"benim rezervasyon",
"aktif rezervasyon",
"otopark rezervasyonlarım",
"ayırdığım yerler",
"otoparkta ayırdığım","otoparkda ayırdığım","ayırdıklarım","ayırdığım yerler","rezerve ettiğim park yerleri","rezerve ettiklerim",

"ayırdığım yerlerim",
"otopark yerlerim",
"park yerlerim",
"otoparkta ayırdıklarım",

# konuşma dili
"ayırmışım", "ayirdim", "ayırdım",
"aldım mı", "almışım",
"rezervasyon var mı",
"rezervasyonum var mı",

"rezervasyonum","rezervasyonlarım",
"benim rezervasyon","aktif rezervasyonlarım",
"otopark rezervasyonlarım","park nolarım","park no'larım","park rezervasyonlarım","park yerlerim","prk yerlerim",
"otopark ayırdığım","ayırdığım park","ayırdıklarım","parklarım","ayırdığım parklar","ayırdığım numaralar","hangi park","hangi park no","hangi parkı ayırmışım",
"ayırdığım yerler","ayırdıgım yerler","ayrdgım yerler"

]

RELATIVE_DAY_TRIGGERS = {
    "today": [
        "bugün", "bugun", "bugünü", "bugunu",
        "bgn", "bugn", "bu gün","bugin"
    ],
    "tomorrow": [
        "yarın", "yarin", "yarını", "yarını",
        "yrn", "yarn","yrna"
    ],
    "yesterday": [
        "dün", "dun", "dünü", "dunu"

    ]
}

NEXT_WEEK_PREFIXES = [
    "haftaya","hftaya","haftya",
    "gelecek hafta",
    "önümüzdeki hafta",
    "ileriki hafta",
    "önüzümüzde ki hafta",
    "haftya"
]
KIM_YAPTI_SORUSU = [
    "sen kimin isisin",
    "seni kim yapti bakalim",
    "kim yapti",
    "kim yapti seni",
    "seni kim yapti",
    "seni kim gelistirdi",
    "kim gelistirdi",
    "kim yazdi",
    "gelistiricin kim",
    "gelistiricinin ismi ne",
    "gelistiren kim",
    "seni gelistiren kim",
    "seni yapan kisi",
    "yapan kim seni",
    "yazilimini yapan kim",
    "yazilimi kim yapti",
    "kim tarafindan yapildin",
    "kim tarafindan gelistirildin",
    "kim uapti seni","gelistiricen kim"
]
STATIC_CAPABILITY_TEXT_old = (
    "Yugii olarak şunlarda yardımcı olabilirim 😊<br><br>"
    "• 🅿️ Otopark rezervasyonu yapma, iptal etme ve müsaitlik sorgulama<br>"
    "• 🗓️ Haftalık çalışma takvimini işaretleme (ofis / home / izin)<br>"
    "• 👥 Şirket çalışan bilgileri (email, telefon, departman)<br>"
    "• 📊 Çalışan listelerini Excel olarak alma (mail, telefon, departman vb.)<br>"
    "• 🍽️ Günlük yemek menüsü sorgulama<br>"
    "• 🏢 Günlük çalışma durumu sorgulama<br> " 
    "   (şirket , departman veya kişi bazında bugün kimler ofiste, evden veya izinli)<br>"
    "• 🌦️ Hava durumu bilgisi sorgulama (bugün / yarın)<br>"
    "• 💱 Güncel döviz kuru bilgisi sorgulama (USD / EUR)<br>"
    "• 🔗 Portal sayfalarına yönlendirme<br><br>"
    "İstersen bunlardan biriyle devam edebilirsin."
)
STATIC_CAPABILITY_TEXT = (
    "Ben Yugii’yim.<br>"
    "Yüce Portal’ın kurumsal dijital asistanıyım ve günlük işlerini kolaylaştırmak için buradayım.<br><br>"

    "• Otopark rezervasyonu oluşturabilir, iptal edebilir veya müsaitlik sorgulayabilirsin.<br>"
    "• Haftalık çalışma takvimini ofis, home ya da izin olarak işaretleyebilirsin.<br>"
    "• Çalışanların iletişim bilgilerini sorgulayabilir, istersen Excel listesi alabilirsin.<br>"
    "• Bugün kimlerin ofiste, evden ya da izinli olduğunu öğrenebilirsin.<br>"
    "• Günlük yemek menüsüne bakabilirsin.<br>"
    "• Hava durumu (bugün / yarın) ve döviz kuru bilgisi alabilirsin.<br>"
    "• Portal içindeki sayfalara hızlıca yönlendirebilirim.<br><br>"

    "Hazırsan bir konuyla başlayalım."
)

PORTAL_LINK_STRONG_HINTS = [
    "sayfa", "sayfasi", "sayfayi",
    "link", "linki", "baglanti",
    "ekran", "panel", "modul","sayfasını ver","aç","sayfasını aç"
]

PORTAL_LINK_VERBS = [     
    "nerede", "nerde",
    "ac", "acilir",
    "bul", "bulamiyorum",
    "sayfasını ver", "goster",
    "nasil acilir", "nasil giderim"
]
PARK_CREATE_ACTION_VERBS = [
    # ayır / ayarla kökü
    "ayır", "ayir", "ayr", "ayrla","yer ayır", "prk ayır","park ayır", "park ayir", "park ayr",

    # doğal konuşma
    "otoparktan yer al","otoparkta yer al",
    "otoparkdan rezerve yap","ayır", "ayir","ayarla", "ayarla","rezerve et",
    "rezerve wt", "rezrve et", "rezrv",
    "rezervasyon yap","ayr","yer ayır","rezv yap","rezerve yap","ayrla","prk ayır",
    "park ayır", "park ayir","rezervasyon yap","rezerve et","ayır","ayarla","rezerv et","park ayr","yer ayır","otoparktan yer al","otoparkta yer al","otoparkdan rezerve yap"
]
THIS_MONTH_KEYS = [
    "bu ay","bu ayki","buu ay","bu ayda","bu ay ki",
    "buayi", "buay", "bu aay",
    "şu ay", "su ay"
]

PAST_MONTH_KEYS = [
    "gecen ay","geçen ay","onceki ay","önceki ay"
]
THIS_WEEK_KEYS = [
    "bu hafta","bu haftada","bu haftaya","bu haftada da","bu haftaya da",
    "bu haftaki","bu haftada","bu haftaya","bu hfta","bu haftaki",
    ]

PAST_WEEK_KEYS = [
    "gecen hafta","onceki hafta","gecen hafya","gecen hafta","gecmis hafta","önceki hafta","bir onceki hafta",
    "bir önceki hafta","geçen hafta","onceki hafta","önceki hafta","bir onceki hafta","bir önceki hafta"
]
WORKFORCE_LIST_KEYS = [
    # kim
    "kim", "kimler","kişileri","isimleri","isimler","kimler var","kimler va"

    # hangi
    "hangi",
    "hangi calisanlar","ulunanalar","bulunanalar","olanlar","olan kişi","olanlar",
    "hangi çalışanlar","çalışanlar","kadrosu","kadrosundakiler","kadrodakiler",
    "hangi kisiler","personel","personeller",
    "hangi kişiler",
    "hangi personeller",
    "hangi personel","olanlar",

    # çoğul
    "calisanlar",
    "çalışanlar",
    "personeller",
    "personel",
    "kisiler",
    "kişiler",

    # dolaylı
    "gelenler",
    "ofistekiler",
    "şirkettekiler",
    "sirkettekiler"
]

WORKFORCE_COUNT_KEYS = [
    # temel
    "kac",
    "kaç",

    # kişi / çalışan
    "kac kisi",
    "kaç kişi",
    "kac calisan",
    "kaç çalışan",
    "kac personel",
    "kaç personel",

    # adet / tane
    "kac adet",
    "kaç adet",
    "kac tane",
    "kaç tane",

    # birleşik varyasyonlar
    "kac adet calisan",
    "kaç adet çalışan",
    "kac kisi calisan",
    "kaç kişi çalışan",
    "kac personel calismis",
    "kaç personel çalışmış",

    # sayı kelimeleri
    "sayi",
    "sayisi",
    "sayısı",
    "adet",
    "toplam","totel","total"
]

PEOPLE_COUNT_KEYS = {
    "kac", "kaç","kac kısı","kac kısı",
    "kac kisi", "kaç kisi",
    "ne kadar", "nekadar",
    "sayisi", "sayısı",
    "toplam",
    "adet",
    "tane"
}

CANCEL_KEYS = {
    "iptal", "iptel", "iptall", "iptaal","ıptal et","iptal er",
    "sil", "kaldir", "cancel", "geri","iptal et","iptal edin","iptal etsene","iptal etmek","iptal edelim","vazgec","vazgeç","sil","kaldir","kaldır"
}

OTOPARK_KEY = [
    "otopark", "otopak", "otoprak", "otopar","yer","yerler","park yeri","otpark","yerler",
    "park", "park yeri", "parkeri",
    "rezervasyon", "rez",
    "park ayır", "park ayarla","otopark", "park", "rezervasyon",
    "park yeri", "araç yeri", "otoparkta",
    "araç yeri", "prk yeri","prk yeri","otprk","prk","rezerve","rzrve","prk ayrla","otoprk ayrla","otopark ayr","otoprk","rzrve"
]
PARK_AVAILABILITY_KEYWORDS = [
    "boş", "dolu","boş yer vrmı ",
    "müsait", "musait", "uygun",
    "müsaitlik",
    "yer var", "yer var mı", "yer varmı",
    "boş park", "boş park var mı",
    "park yeri var mı", "park yeri varmı",
    "hangi yer", "hangi yerler",
    "neresi müsait", "nereler müsait", "boş", "dolu", "müsait", "musait", "müsaitlik",
    "yer var", "yer varmı", "yer var mı",
    "boşluk", "uygun","park yeri varmı","boş park varmı","boş park","var mı "

]

PERSONEL_KEY = {
"calisan","calisanlar","calisanin","calısan","calısanlar","caisan","caisanlar","calsan","calsanlar",
"personel","personeller","personellerin","peronel","persnel","personl",
"kisi","kisiler","kisileri","kisilerin",
"isim","isimler","isimleri",
"ekip","ekipuyesi","ekip uyesi","ekiptekiler",
"sirkettekiler",
"olan","olanlar","calisan", "çalışan",
"personel",
"kisi", "kişi",
"ekip"
}


FIELD_TO_COLUMN = {
    # 👤 USERNAME
    "kullanici adi": "username",
    "kullanıcı adı": "username",
    "kullanici ismi": "username",
    "kullanıcı ismi": "username",
    "username": "username",
    "login": "username",
    "giris adi": "username",
    "giriş adı": "username",
    "portal giris adi": "username",
    "portal giriş adı": "username",

    # 📅 KIDEM TARİHİ (İŞE BAŞLANGIÇ)
    "kidem": "Kidem_Tarihi",
    "kıdem": "Kidem_Tarihi",
    "kidem tarihi": "Kidem_Tarihi",
    "kıdem tarihi": "Kidem_Tarihi",
    "ne zaaman": "Kidem_Tarihi",
    "ne zaaman başlafı": "Kidem_Tarihi",
    "ne zaaman başladı": "Kidem_Tarihi",
    "ne zaman başladı": "Kidem_Tarihi",
    "ne zmaan başladı": "Kidem_Tarihi",
    "ne zamn başladı": "Kidem_Tarihi",
    "ne zmaan başladı": "Kidem_Tarihi",
    "ne zamandir": "Kidem_Tarihi",
    "hangi gün başladı": "Kidem_Tarihi",
    "hangi yıl başladı": "Kidem_Tarihi",
    "hangi tarihte başladı": "Kidem_Tarihi",
    "ne zamandan beri": "Kidem_Tarihi",
    "ne zaman basladi": "Kidem_Tarihi",
    "ise ne zaman basladi": "Kidem_Tarihi",
    "kac yildir": "Kidem_Tarihi",
    "kaç yıldır": "Kidem_Tarihi",
    "bizimle ne zamandir": "Kidem_Tarihi",
    "sirkette ne zamandir": "Kidem_Tarihi",
    "burada ne zamandir": "Kidem_Tarihi",
    "ne kadar zamandir": "Kidem_Tarihi",
    "zmanıdr burda": "Kidem_Tarihi",
    "zamandır burad": "Kidem_Tarihi",

    "ne zaaman": "Kidem_Tarihi",
    "ne kadar işe girdi": "Kidem_Tarihi",
    "ne zamandır  bizimle": "Kidem_Tarihi",
    "işe başlama tarihi": "Kidem_Tarihi",
    "işe başlama zamanı": "Kidem_Tarihi",
    "kidem": "Kidem_Tarihi",
    "kıdem": "Kidem_Tarihi",
    "kidem tarihi": "Kidem_Tarihi",
    "kıdem tarihi": "Kidem_Tarihi",
    "ise giris tarihi": "Kidem_Tarihi",   

    # 📧 EMAIL
    "mail": "email",
    "email": "email",
    "e-mail": "email",
    "eposta": "email",
    "e posta": "email",
    "mail adresi": "email",
    "email adresi": "email",
    "eposta adresi": "email",
    "kurumsal mail": "email",
    "şirket maili": "email",
    "sirket maili": "email",
    "mail adresi": "email",
    "şirket maili": "email",
    "maili": "email",
    # 📞 TELEFON
    "telefon": "TelNo",
    "tel": "TelNo",
    "telefonu": "TelNo",
    "telefon numarası": "TelNo",
    "telefon numarasi": "TelNo",
    "tel no": "TelNo",
    "gsm": "TelNo",
    "cep": "TelNo",
    "cep telefonu": "TelNo",
    "dahili": "TelNo",
    "dahili numara": "TelNo",

    # 👤 USERNAME
    "kullanıcı adı": "username",
    "kullanici adi": "username",
    "username": "username",
    "login": "username",

    # 🏢 DEPARTMAN
    "departman": "departman",
    "birim": "departman",
    "ekip": "departman",
    "departmanı": "departman",
    "departmani": "departman",
    "departmanı": "departman",
    "departmanda": "departman",
    "departmanında": "departman",

    # 🧑‍💼 UNVAN / TITLE
    "unvan": "title",
    "ünvan": "title",
    "title": "title",
    "pozisyon": "title",
    "görev": "title",
    "gorev": "title",
    # 🚗 ARAÇ
    "plaka": "plaka",
    "araç plakası": "plaka",
    "arac plakasi": "plaka",
    "2. plaka": "arac_plaka2",
    "ikinci plaka": "arac_plaka2",
    "araç markası": "arac_marka",
    "arac markasi": "arac_marka",

    # ======================
    "doğum günü": "dogum_gun",
    "dogum gunu": "dogum_gun",
    "doğduğu gün": "dogum_gun",
    "doğum ayı": "dogum_ay",
    "dogum ayi": "dogum_ay",
    "dogdudu gün": "dogum_ay",
    "ne zaman dodgdu": "dogum_ay",
    "dogum tarihi": "dogum_ay",
    "dogum tarıh": "dogum_ay",
    "dogum tarihini": "dogum_ay",


    "kıdem": "Kidem_Tarihi",
    "kidem": "Kidem_Tarihi",
    "kıdem tarihi": "Kidem_Tarihi",
    "işe giriş tarihi": "Kidem_Tarihi",
    "ise giris tarihi": "Kidem_Tarihi",


    "linkedin": "linkedin",
    "linkedin profili": "linkedin",
    "linkedin hesabı": "linkedin",
    "linkedin hesabi": "linkedin",
    "linkedin linki": "linkedin",
}


COMPANY_PEOPLE_KEYWORDS = [
    # kişi bilgisi
    "kim", "kimdir","ekiibi","kmler vr","tel","tel no","telefon numarası","meili","e postası","e-postası","şirket maili","iş maili","ünvanı","title'ı",
    "ne is yapiyor", "isi nedir",
    "gorevi", "unvani", "pozisyonu",

    # departman
    "hangi departmanda",
    "hangi birimde","hangi birimde","hangi alanda",
    "departmani","departmnı","alanı","birimi","çalıştığı yer",

    # iletişim
    "mail", "email", "eposta",
    "telefon", "tel", "numarasi",

    # ekip / liste
    "ekip", "ekibi", "ekibinde",
    "calisan", "calisanlar",
    "calisiyor", "calisiyorlar",
    "kimler var"
    ]

COMPANY_PEOPLE_EXCLUDE = [
    "adin ne",
    "senin adin","işin ne",
    "ismin ne", "ne işin var","ne iş yapıyorsun","neler yapabilirsin","neler yapabilirisin","görevin neler","görevlerini anlat","görevlerin"
    ]

RAW_FIELD_KEYWORDS = {
    "username": [
        "kullanici adi",
        "kullanıcı adı",
        "kullanici ismi",
        "kullanıcı ismi",
        "username",
        "user name",
        "login",
        "giris adi",
        "giriş adı",
        "portal giris adi",
        "portal giriş adı",
        "yuce portal giris",
        "yuce portal kullanici adi",
        "sisteme giris adi",
        "sisteme giriş adı"
    ],
    "email": [
        "mail", "email", "e mail",
        "eposta", "e posta",

        "mail adresi",
        "email adresi",
        "eposta adresi",

        "kurumsal mail",
        "sirket maili",
        "şirket maili",

        "maili",
        "mailini",
        "mailini ver",
        "mail adresini soyle",

        "epostasi",
        "epostasini",
        "epostasini soyle",

        "iletisim maili",
        "mail bilgisi",
        "eposta bilgisi"
    ],

    "TelNo": [
        # temel
        "telefon", "tel",
        "telefon numarasi",
        "numara", "numarasi",

        "gsm",
        "cep",
        "cep telefonu",
        "cep numarasi",
        "sirket hatti", "şirket hatti",
        "ofis hatti",
        "sabit hat",
        "dahili",
        "dahili numara",
        "dahili hatti",
        "dahili telefon",

        "iletisim numarasi",
        "ulasim numarasi",
        "telefon bilgisi",
        "telefonu nedir",
        "numarasini soyle",
        "telefonunu ver"
    ],

    "title": [
        "title",
        "unvan", "unvani",

        "gorev", "gorevi",
        "pozisyon", "pozisyonu",

        "rolu",
        "hangi rolde",

        "ne is yapiyor",
        "isi nedir",
        "ne olarak calisiyor",

        "meslegi",
        "calisma alani"
    ],

    "departman": [
        "departman","depatmani",
        "birim","hangi departmanda",
        "departmani ne",
        "departman",
        "departmani",
        "departmanini",
        "departmanda",
        "departmandan",
        "birim",
        "birimi",
        "biriminde",
        "hangi departman",
        "hangi departmanda",
        "departmani ne",
        "departmani nedir",
        "departmani neydi",
        "calistigi departman",
        "calistigi birim",
        "hangi birimde",
        "calistigi departman",
        "calistigi birim",

        "ekibi",
        "hangi ekipte",
        "takimi",
        "hangi takimda"
    ],
    "linkedin": [
        "linkedin",
        "linked in",
        "linkedn",
        "linkdn",
        "linkedin adresi",
        "linkedin profili",
        "linkedin hesabi",
        "linkedin linki",
        "sosyal medya",
        "sosyal medya hesabi",
        "profesyonel profil",
        "linkedin sayfasi"
    ],
    "dogum_gun": [
        "dogum gunu",
        "dogum tarihi",
        "dogdugu gun",
        "dogdugun gun",
        "dogmus",
        "ne zaman dogmus",
        "dunyaya gelmis",
        "dunyaya ne zaman gelmis",
        "dogum gununu kutla",
        "dogum gununu kutlayacagim",
        "gununu soyle",
        "hangi gun dogmus"
    ],

    "dogum_ay": [
        "hangi ay dogmus",
        "dogdugu ay",
        "dogum ayi"
    ],

    "identity": [
        "kim",
        "kimdir",
        "kisi kim",
        "bilgileri",
        "bilgileri ver",
        "detay",
        "detayli bilgi",
        "hakkinda",
        "hakkinda bilgi"
    ],
    "Kidem_Tarihi": [
        # temel
        "kidem"," işe başlangıç tarihi","işe başlangç tarihi"," işe başlama zamanı"," işe başlama vakti"," işe başlangıç tarh",
        "kıdem","ne zamandır","ne zaamandır","ne zamandr","kaç zamandır","kaç yıldır burdayım","kaç zaamandır burda","ne kadardır",
        "kidem tarihi",
        "kıdem tarihi",
        "kidem bilgisi",
        "kıdem tarihi",

        # işe başlangıç / süre
        "ne zamandir calisiyor",
        "ne zamandır çalışıyor",
        "ne zamandir bizimle",
        "ne zamandır bizimle",
        "sirkette ne zamandir",
        "şirkette ne zamandır",
        "burada ne zamandir",
        "burada ne zamandır",

        # başlangıç soruları
        "ne zaman basladi",
        "ne zaman başladı",
        "ise ne zaman basladi",
        "işe ne zaman başladı",
        "ise baslama tarihi",
        "işe başlama tarihi",
        
        "ne zaman ise basladi",

        # süre soruları
        "kac yildir",
        "kaç yıldır",
        "kac senedir",
        "kaç senedir",
        "ne kadar zamandir",
        "ne kadar zamandır",
        
        "ne zaman ise basladi",
        "ne zaman ise basladi",
        "ise ne zaman basladi",
        "ne zaman basladi",
        "ise giris tarihi",
        "ise baslama tarihi",
        
        "calisma suresi",
        "çalışma süresi",
        "zmanıdr burda","zamandır burad",
        "zamandır burda","zamandır burada","ne kadar işe girdi","ne zamandır  bizimle","işe başlama zamanı"
    ]

}
