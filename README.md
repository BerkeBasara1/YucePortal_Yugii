# Yugii_AI_güncel Python Dosyaları Rehberi

Bu README, `Yugii_AI_güncel` klasörü içindeki **yalnızca Python dosyalarını** açıklar.  
`instructions/`, `__pycache__/`, test çıktıları veya metin tabanlı prompt dosyaları bilerek kapsam dışında bırakılmıştır.

Amaç, bu klasöre yeni giren bir geliştiricinin:

1. Hangi `.py` dosyasının ne yaptığını anlaması
2. Mesajın sisteme nasıl girdiğini ve hangi dosyalardan geçerek cevap üretildiğini görmesi
3. Hangi modülde hangi değişikliği yapması gerektiğini hızlıca bulması

## Genel Mimari

`Yugii_AI_güncel` içindeki Python yapısı dört ana katmandan oluşur:

1. **Kompozisyon katmanı**
   `yugii_brain_ai.py`, tüm mixin dosyalarını bir araya getirip tek bir `BrainAIYugii` sınıfı oluşturur.

2. **İş mantığı katmanı**
   `brain_modules/` altındaki dosyalar, büyük beyin dosyasının sorumluluklara göre bölünmüş halidir.
   Her dosya bir mixin içerir ve belirli bir konu alanını yönetir.

3. **Dil/NLP ve sabitler katmanı**
   `NLP/normalize.py`, `NLP/people_schema.py`, `NLP/yugii_brain_lists.py` dosyaları; normalize etme, alan şemaları ve anahtar kelime sözlüklerini sağlar.

4. **Destek katmanı**
   `yugii_general_assistant_fonk.py` genel fallback asistanıdır.
   `logger/yugii_logger.py` log arayüzünü sağlar.
   `test/test_runner.py` temel senaryo testleri için yardımcı dosyadır.

## Bir Mesaj Sistemde Nasıl İşlenir?

En kısa ve pratik akış şöyledir:

1. Uygulama `BrainAIYugii` sınıfını `yugii_brain_ai.py` üzerinden import eder.
2. Bu sınıf, `brain_modules/` altındaki mixin dosyalarının birleşiminden oluşur.
3. Kullanıcı mesajı `process_message()` fonksiyonuna gelir.
4. `extract_message_signals()` mesajdan tarih, soru tipi, departman, kişi, export, takvim, geçmiş sorgu gibi sinyalleri çıkarır.
5. `detect_business_intent()` önce alan bazlı bir yön tayini yapar.
6. Gerekirse `detect_main_intent()` daha ayrıntılı nihai intent kararını verir.
7. Seçilen intent’e göre uygun handler çağrılır.
   Örnek:
   `otopark_create`, `handle_otopark_create()` fonksiyonuna gider.
   `company_people`, `handle_company_people()` akışına gider.
   `weather`, `handle_weather_redirect()` fonksiyonuna gider.
8. İlgili handler, gerektiğinde:
   MySQL, Oracle, SQL Server sorguları çalıştırır
   OpenAI çağrısı yapar
   sabit listeleri kullanır
   normalize fonksiyonlarını çağırır
9. Eğer mesaj desteklenen iş akışlarından birine güvenilir biçimde bağlanamazsa, en sonda `GeneralAssistant` fallback devreye girer.

## Sınıf Birleşimi Mantığı

`BrainAIYugii` tek parça yazılmış bir sınıf değil, çok sayıda mixin’in birleşimidir.

Bu yaklaşımın amacı:

- Çok büyük bir dosyayı konu bazlı alt parçalara ayırmak
- Benzer sorumlulukları aynı dosyada toplamak
- Yeni özellik eklerken doğru modülü daha kolay bulmak

Mixin sırası önemlidir. Çünkü Python, metod ararken sınıf çözümlemesini soldan sağa yapar.
Bu projede:

- Ana yönlendirici `MessageProcessingMixin` üstte tutulur
- İş akışları konu bazlı mixin’lerde dağılmıştır
- Ortak altyapı ve temel yardımcılar `BrainBaseMixin` içinde en altta yer alır

Bu sayede özel davranışlar önce, genel altyapı daha sonra çözülür.

## Klasör Bazlı Detaylı Dosya Açıklamaları

## Kök Dosyalar

| Dosya | Ne yapar? | Sistemdeki yeri |
| --- | --- | --- |
| `yugii_brain_ai.py` | Tüm mixin dosyalarını import eder ve `BrainAIYugii` sınıfını oluşturur. | Projenin giriş noktasıdır. Uygulama bu dosyadan beyni alır. |
| `yugii_general_assistant_fonk.py` | Genel bilgi ve smalltalk fallback asistanını tanımlar. | Ana iş kuralları dışında kalan sorular için son güvenli fallback katmanıdır. |

### `yugii_brain_ai.py`

Bu dosya artık iş mantığını taşımaz; ana görevi kompozisyondur.

İçerdiği ana parçalar:

- Mixin importları
- `BrainAIYugii` sınıfı
- `__all__`
- preload denemesi

Bu dosyada iş akışı kodu azdır; asıl davranış `brain_modules/` altına taşınmıştır.

### `yugii_general_assistant_fonk.py`

Bu dosya, core business logic dışında kalan ve güvenli biçimde cevaplanabilecek genel sorular için kullanılır.

Başlıca görevleri:

- OpenAI client oluşturmak
- Sistem prompt’unu kurmak
- Desteklenen intent’leri metinsel olarak modele anlatmak
- İç süreç, şirket içi veri, aksiyon yapılmış gibi görünme gibi riskleri filtrelemek
- Küfür ve bloklu konu kontrolü yapmak

Önemli nokta:

- Bu sınıf **asıl iş yapan beyin değildir**
- Otopark kaydı, çalışan sorgusu, haftalık takvim, export gibi gerçek işlemleri yapmaz
- Bunlar için sadece nazik bir fallback üretir

## `brain_modules/` Klasörü

Bu klasör, eski büyük beyin dosyasının modüler hale getirilmiş parçalarını içerir.

| Dosya | Ana sorumluluk |
| --- | --- |
| `shared.py` | Ortak importlar, yardımcı fonksiyonlar, OpenAI/DB bağlantı yardımcıları |
| `base_mixin.py` | Singleton yaşam döngüsü, prompt yükleme, normalize proxy’leri, smalltalk ve döviz akışları |
| `people_context.py` | Kişi/departman/şifre bağlamı, ön tarama ve bazı temel tespit fonksiyonları |
| `intent_signals.py` | Mesaj sinyallerini çıkarma ve üst seviye business intent belirleme |
| `intent_routing.py` | Nihai intent tespiti ve kişi/şirket ayrımı |
| `language_history.py` | Çalışma tipi, tarih özeti ve bazı dil doğallaştırma yardımcıları |
| `portal_food_help.py` | Portal linkleri, yemek menüsü ve yardım üretimi |
| `parking_create.py` | Otopark rezervasyonu oluşturma ve tarih çözümleme |
| `parking_status.py` | Otopark iptali, müsaitlik ve kullanıcı durumu |
| `calendar_parser.py` | Takvim tarih aralığı çözümleme |
| `weekly_calendar.py` | Haftalık takvim işlemleri ve tekrar desenleri |
| `work_history.py` | Geçmiş çalışma özeti ve departman sayısı |
| `people_directory.py` | Kişi tespiti, kişi çözümleme, çalışan sorgu akışı |
| `people_response.py` | Çalışan verisini çekme, formatlama, export cevapları |
| `fun_portal_info.py` | Eğlence/pop-culture türü intent’ler |
| `weather_workforce_parser.py` | Hava durumu, portal info, kurumsal bilgi, iş gücü tarih parse’ları |
| `workforce_status.py` | İş gücü durumu sorguları, simple smalltalk, şifre kılavuzu soruları |
| `analytics_dealers.py` | Trend analizi, bayi verileri, satış sayısı akışları |
| `message_processing.py` | Ana orchestration: mesajı alır, intent seçer, doğru handler’a yollar |
| `__init__.py` | Paket tanımı |

### `shared.py`

Bu dosya, diğer mixin dosyalarının ortak bağımlılık katmanıdır.

Burada bulunan temel unsurlar:

- ortak importlar
- `print` için güvenli Unicode wrapper
- `_build_openai_client()`
- `_mysql_conn()`
- `gpt_fix_text()`
- `get_effective_today()`
- sabitler ve ortak sözlüklerin re-export edilmesi

Bu modül, teknik olarak merkezi “toolbox” gibi davranır.
Mixin dosyalarının çoğu `from .shared import *` ile buradaki isimleri kullanır.

### `base_mixin.py`

Bu dosya beyin sınıfının temel iskeletini taşır.

Ana görevleri:

- `get_instance()` ile singleton yönetimi
- `__init__()` ile client, prompt ve cache alanlarını hazırlama
- Oracle bağlantısı açma
- prompt dosyasını yükleme
- `normalize.py` fonksiyonlarını sınıf metodu gibi sunma
- küçük sohbet/fallback için `ask_gpt()`
- döviz kuru okuma ve döviz hesaplama akışları
- SQL log buffer desteği

Bu dosya, “beyin çalışabilsin” diye gerekli olan temel altyapıyı sağlar.

### `people_context.py`

Bu modül, kişi ve departman temelli soruların daha işlenmeden önce kokusunu alır.

Öne çıkan işler:

- kişi alan köklerini hazırlamak
- mesajda kişi/departman bağlamı aramak
- toplu çalışan referansı var mı tespit etmek
- şifre talebi olup olmadığını anlamak
- departman sayısı için DB sorgusu başlatmak
- haftalık takvim niyeti var mı önceden sezmek
- isim token’larını daha akıllı normalize etmek

Bu dosya doğrudan cevap üretmekten çok, sonraki intent kararlarını güçlendirir.

### `intent_signals.py`

Bu modül, mesajdan yapılandırılmış sinyal çıkarma işini yapar.

Burada tipik olarak şu sorulara cevap aranır:

- Mesaj soru mu?
- Tarih içeriyor mu?
- Takvim aksiyonu içeriyor mu?
- Geçmiş sorgusu mu?
- Export talebi var mı?
- Toplu çalışan sorgusu mu?
- Departman listesi mi isteniyor?

`extract_message_signals()` bu bilgileri tek bir sözlükte toplar.
`detect_business_intent()` ise önce alan bazlı kaba yönlendirme yapar.

Bu yüzden bu dosya, routing kararının ilk yarısıdır.

### `intent_routing.py`

Bu modül, sinyallerden sonra daha kesin intent kararı verir.

Başlıca konular:

- `detect_main_intent()`
- şirket itibarı soruları
- portal bilgi/link soruları
- hava durumu
- otopark intent ayrımları
- kişi adı gerçekten çalışan mı, yoksa şirket adı mı ayrımı

Bu dosya, sistemin “bu mesaj tam olarak hangi akışa gitmeli?” sorusunu cevaplar.

### `language_history.py`

Bu modül hem cevap tonunu doğallaştırır hem de çalışma tipi/tarih çözümlemesinde kullanılır.

Ana işleri:

- metni daha doğal hale getirme
- yemek giriş/çıkış cümleleri üretme
- çalışma tipi tespiti yapmak
- tarih aralığı çıkarımı yapmak
- geçmiş çalışma sorgularında kullanılacak tarihleri çözmek
- plaka ekleme gibi bazı bilgilendirici soruları yakalamak

Bu dosya teknik olarak NLP ile response polishing arasında bir köprü gibidir.

### `portal_food_help.py`

Bu modül üç ayrı ama ilişkili konuyu yönetir:

- portal link bulma
- yemek menüsü sorgulama
- kullanıcı yardım isteme akışı

İçindeki önemli parçalar:

- `detect_link_intent()`
- `detect_food_intent()`
- `resolve_food_date()`
- `get_food_menu_for_date()`
- `find_page_link()`
- `help_user_with_parse()`
- `llm_with_handle_help()`

Kısacası bu dosya, “beni şu sayfaya yönlendir”, “bugün yemek ne var”, “bunu nasıl yaparım?” gibi mesajları kapsar.

### `parking_create.py`

Bu modül, otopark rezervasyonu oluşturma akışının en kritik parçasıdır.

Ana görevleri:

- doğal dilde tarih çözmek
- hafta içi/gün/ay bağlamlarını parse etmek
- gerekirse GPT ile tarih yazımını düzeltmek
- metinden tarih çıkarmak
- tarih aralıklarını normalize etmek
- yeni otopark rezervasyonu oluşturmak

Bu dosya özellikle tarih anlama konusunda yoğundur.
Otopark oluşturma sırasında yanlış tarih yorumlanmaması için çok sayıda koruma içerir.

### `parking_status.py`

Bu modül, oluşturma dışındaki otopark işlemlerini yürütür:

- rezervasyon iptali
- belirli gün için müsaitlik sorgusu
- kullanıcının kendi rezervasyonunu sorgulaması
- çalışma günü atama metinlerini parse etme

Otopark dünyasının “okuma ve iptal” tarafı burada yaşar.

### `calendar_parser.py`

Bu dosya büyük ölçüde bir uzman parser dosyasıdır.

Ana işi:

- serbest yazılmış takvim cümlesinden tarih aralığı çıkarmak

Bu parser:

- mutlak tarih
- göreli tarih
- hafta/ay bağlamı
- hafta içi grupları
- günlük tekrar mantıkları

gibi karmaşık tarih desenlerini çözmeye çalışır.

Takvim işlemlerinin en zor parçası olan tarih aralığı parse işlemi burada izole edilmiştir.

### `weekly_calendar.py`

Bu modül, haftalık takvim iş kurallarını uygular.

Başlıca görevleri:

- haftalık takvim işleme
- ay içi tekrar desenleri üretme
- tüm ay tarih listesi oluşturma
- haftalık takvim sonucunu kullanıcıya daha anlaşılır anlatmak

Yani `calendar_parser.py` tarihi anlar, `weekly_calendar.py` ise bu anlamı işleme dönüştürür.

### `work_history.py`

Bu modül geçmiş çalışma kayıtlarıyla ilgilenir.

Görevleri:

- DB’deki çalışma tipi değerlerini normalize etmek
- tarih aralığı ve sorgu tipine göre geçmiş özet üretmek
- çalışma günü sayısını doğal dile dökmek
- geçmiş kayıtları kontrol etmek
- departman kişi sayısı işlemini sonuçlandırmak

Bu dosya özellikle “geçen hafta kaç gün ofisteydim?” türü sorular için önemlidir.

### `people_directory.py`

Bu modül çalışan/kişi sorgularının giriş tarafıdır.

Yaptığı işler:

- çalışan sorgusunu başlatmak
- metindeki kişi varlığını resolve etmek
- hızlı parse yapmak
- gerekirse mini LLM parse kullanmak

Bu modül, kullanıcı mesajından “hangi kişi veya kişiler kastediliyor?” bilgisini çıkarmaya odaklanır.

### `people_response.py`

Bu modül kişi sorgularının veri ve çıktı tarafıdır.

Ana görevleri:

- ilgili çalışan verisini DB’den almak
- departman adını çıkarmak
- profil linkleri eklemek
- cevabı HTML/Türkçe biçiminde oluşturmak
- export taleplerini yönetmek
- bekleyen kişi çözümlemelerini tamamlamak

Kısacası `people_directory.py` soruyu parse eder, `people_response.py` sonucu üretir.

### `fun_portal_info.py`

Bu modül iş açısından kritik olmayan ama kullanıcı deneyimi için eklenen hafif akışları içerir.

Örnek görevler:

- pop-culture türü soruları tanımak
- buna uygun güvenli cevaplar üretmek
- eğlence intent’ini yönetmek

### `weather_workforce_parser.py`

Bu modül birden fazla “yardımcı servis” akışını toplar.

İçerdiği alanlar:

- portal hakkında bilgi
- Yüce Auto / Skoda kurumsal bilgi cevapları
- departman listesi
- şarj rezervasyonu yönlendirmesi
- hava durumu günü ve soru tipi çözümleme
- hava durumu cevabı üretimi
- “bugün hangi gün?” tarzı cevaplar
- iş gücü sorguları için tarih çözümleme

Bu dosya, doğrudan ana intent motoruna bağlı ama kendi içinde birden fazla mini modül barındırır.

### `workforce_status.py`

Bu modül, iş gücü durumu sorgularının nihai uygulama tarafıdır.

Başlıca görevleri:

- belirli tarih veya dönem için iş gücü durumunu hesaplamak
- simple smalltalk tespiti yapmak
- şifre rehberi sorusu tespiti yapmak

Bu modül, `weather_workforce_parser.py` ile birlikte çalışır:

- biri tarih ve niyet bağlamını hazırlar
- diğeri asıl sonucu üretir

### `analytics_dealers.py`

Bu modül, bayi ve satış/trend tarafındaki iş akışlarını toplar.

Ana parçalar:

- aylık trend analizi alma
- trend cevabını formatlama
- şehir tespiti
- bayi listesini cache’li çekme
- yıla göre satış sayısı alma
- bayi bilgisi ve bayi sayısı cevaplama

Bu dosya, diğer modüllere göre daha raporlama/analitik ağırlıklıdır.

### `message_processing.py`

Bu dosya, sistemin gerçek orkestra şefidir.

`process_message()` şunları yapar:

- kullanıcı mesajını alır
- session’dan kullanıcı bilgilerini toplar
- mesajı normalize eder
- sinyalleri çıkarır
- business intent belirler
- gerekirse final intent belirler
- güvenlik kontrollerini yapar
- doğru handler’a dallanır
- hiçbir akış tutmazsa fallback assistant’a gider

Bu modül olmadan diğer tüm modüller ayrı yetenekler olarak kalırdı.
Sistemi tek bir karar ağacında birleştiren katman burasıdır.

## `NLP/` Klasörü

## `normalize.py`

Bu dosya, yazım farklılıklarını ve Türkçe karakter varyasyonlarını normalize eder.

Başlıca işlevleri:

- kişi sorgusu için genel normalize
- takvim metni normalize
- alan adı normalize
- kişi adı token normalize
- departman eklerini budama
- fuzzy match yardımcıları
- ay adı eklerini temizleme
- tarihi gün adıyla formatlama

Bu dosya neredeyse tüm intent ve parser modüllerinin temel bağımlılığıdır.

## `people_schema.py`

Bu dosya, çalışan verisinin hangi alanlarının dışa aktarılabilir olduğunu tanımlar.

İçeriği daha çok şema/sabit ağırlıklıdır:

- izinli kolonlar
- export preset’leri
- kişi DB alanları
- çekirdek zorunlu alanlar

Özellikle export ve kişi listeleme akışları bu dosyadan beslenir.

## `yugii_brain_lists.py`

Bu dosya, projenin anahtar kelime ve sabit bankasıdır.

İçinde çok sayıda sözlük ve liste vardır:

- gün ve ay varyasyonları
- hafta/ay bağlam kelimeleri
- hava durumu kelimeleri
- portal link kelimeleri
- yardım fiilleri
- export ipuçları
- eğlence kelimeleri
- otopark anahtar kelimeleri
- kişi/departman alan kelimeleri
- şirket itibarı soru kalıpları
- statik capability metinleri

Bu dosyada algoritma çok az, veri çok fazladır.
Sistemin dilsel kapsama alanını genişleten ana sözlük deposu burasıdır.

## `logger/` Klasörü

| Dosya | Rol |
| --- | --- |
| `yugii_logger.py` | Logger singleton ve process decorator tanımlar |
| `__init__.py` | Paket tanımı |

### `yugii_logger.py`

Şu an oldukça hafif bir implementasyondur.

İçerdiği parçalar:

- `YugiiLogger` singleton sınıfı
- `log_db_query()`
- `write_plain()`
- `log_process_message()` decorator’ü

Şu anki haliyle metotlar no-op davranır, yani gerçek log yazmaz.
Ama mimari olarak loglama için ortak bir giriş noktası tanımlar.

## `test/` Klasörü

### `test_runner.py`

Bu dosya, tam otomatik bir unit test altyapısı değil; daha çok senaryo bazlı manuel test yardımcı aracıdır.

Nasıl çalışır:

1. Minimal bir Flask app kurar
2. `session` içine örnek kullanıcı bilgisi yazar
3. `BrainAIYugii.get_instance()` ile beyni alır
4. Önceden tanımlı soru listesini tek tek `process_message()` içine gönderir
5. Sonuçları `outputs.txt` dosyasına yazar

Bu dosya özellikle entegrasyon davranışını hızlı gözden geçirmek için faydalıdır.

## Paket İşaretleyici Dosyaları

Bu dosyalar iş mantığı taşımaz, ama import düzeni için gereklidir:

- `brain_modules/__init__.py`
- `logger/__init__.py`

Görevleri, ilgili klasörleri Python paket alanı olarak işaretlemek ve import yapısını düzenli tutmaktır.

## En Önemli Bağımlılıklar ve Veri Kaynakları

Bu klasördeki Python dosyaları aşağıdaki dış bağımlılıklarla çalışır:

- OpenAI API
- MySQL
- Oracle
- SQL Server / `pyodbc`
- Flask `session`
- `sentence_transformers`
- `rapidfuzz`
- `requests`
- `pandas`

Bu yüzden birçok handler yalnızca saf Python mantığı değil, aynı zamanda veri tabanı ve dış servis entegrasyonu da içerir.

## Hangi Değişiklik İçin Hangi Dosyaya Bakılmalı?

Kısa rehber:

- Yeni intent eklemek için:
  önce `intent_signals.py` ve `intent_routing.py`
- Ana karar ağacını değiştirmek için:
  `message_processing.py`
- Kişi/çalışan sorgusu değiştirmek için:
  `people_context.py`, `people_directory.py`, `people_response.py`
- Haftalık takvim için:
  `calendar_parser.py`, `weekly_calendar.py`
- Otopark için:
  `parking_create.py`, `parking_status.py`
- Hava durumu veya iş gücü için:
  `weather_workforce_parser.py`, `workforce_status.py`
- Sözlük/anahtar kelime kapsamı genişletmek için:
  `NLP/yugii_brain_lists.py`
- Normalize davranışını düzeltmek için:
  `NLP/normalize.py`
- Genel fallback cevaplarını değiştirmek için:
  `yugii_general_assistant_fonk.py`

## Sonuç

`Yugii_AI_güncel` içindeki Python yapısı tek bir chatbot dosyasından ibaret değildir.
Bu klasör aslında:

- routing
- parsing
- intent detection
- çalışan dizini sorgulama
- otopark yönetimi
- takvim yönetimi
- hava durumu ve bilgi modülleri
- fallback LLM katmanı
- normalize ve sabit sözlük katmanı

gibi alt sistemlerden oluşan modüler bir çalışma alanıdır.

Bu klasörü anlamanın en doğru yolu şu sırayla ilerlemektir:

1. `yugii_brain_ai.py`
2. `brain_modules/message_processing.py`
3. `brain_modules/intent_signals.py`
4. `brain_modules/intent_routing.py`
5. İlgilendiğin özellik alanına ait mixin dosyası
6. Gerekirse `NLP/normalize.py` ve `NLP/yugii_brain_lists.py`

Bu sıra, hem çağrı zincirini hem de gerçek bakım noktalarını en hızlı şekilde anlamanı sağlar.
