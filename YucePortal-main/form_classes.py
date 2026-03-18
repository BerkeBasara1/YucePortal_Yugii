from wtforms import Form, StringField, TextAreaField, SelectField, PasswordField, FileField, validators, BooleanField, SubmitField, ValidationError, DateField, IntegerField, RadioField, DecimalField, FieldList, FormField, HiddenField, SelectMultipleField, widgets, DateTimeField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields import DateTimeLocalField
from wtforms.validators import Optional
from wtforms.validators import DataRequired, NumberRange, Length, Optional
import datetime
from datetime import date


# Login Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı", render_kw={"style": "border-radius: 10px; width:250px"})
    password = PasswordField("Şifre", render_kw={"style": "border-radius: 10px; width:250px"})

# Bayi Login Formu
class BayiLoginForm(Form):
    mail = StringField("Mail Adresi", render_kw={"style": "border-radius: 10px; width:250px"})
    password = PasswordField("Şifre", render_kw={"style": "border-radius: 10px; width:250px"})

class ProfileSettings_Form(Form):
    arac_marka = SelectField("Marka", choices=[("Skoda", "Skoda"), ("Skoda (Şirket Aracı)", "Skoda (Şirket Aracı)"), ("Diğer", "Diğer")], render_kw={'style': 'border-radius:10px;'})
    arac_plaka = StringField("Plaka")

# Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim", validators = [validators.Length(min = 2, max = 25)])
    surname = StringField("Soyisim", validators = [validators.Length(min = 2, max = 25)])
    username = StringField("Kullanıcı Adı", validators = [validators.Length(min = 2, max = 30)])
    email = StringField("Email Adresi", validators = [validators.Email(message = "Lütfen Geçerli bir email adresi giriniz.")])
    department = SelectField('Departman', choices=[('Bayi Geliştirme', 'Bayi Geliştirme'), 
                                                   ('Bilgi Teknolojileri', 'Bilgi Teknolojileri'),
                                                   ('Dijital Dönüşüm ve Müşteri Deneyim Yönetimi', 'Dijital Dönüşüm ve Müşteri Deneyim Yönetimi'),
                                                   ('Filo Satış', 'Filo Satış'),
                                                   ('İdari İşler', 'İdari İşler'), 
                                                   ('İnsan Kaynakları', 'İnsan Kaynakları'),
                                                   ('İş Geliştirme', 'İş Geliştirme'),
                                                   ('Mali İşler', 'Mali İşler'),
                                                   ('Pazarlama', 'Pazarlama'),
                                                   ('Satış', 'Satış'),
                                                   ('SSH', 'Satış Sonrası Hizmetler'), 
                                                   ('Stratejik Planlama ve Proje Yönetimi', 'Stratejik Planlama ve Proje Yönetimi'),
                                                   ('Ürün', 'Ürün'),
                                                   ('Yeni İş Modelleri', 'Yeni İş Modelleri'),
                                                   ('Yönetim', 'Yönetim')])
    months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    dogum_month = SelectField('Doğum Ay', choices=months, validators=[validators.DataRequired()])
    dogum_day = SelectField('Doğum Gün', choices=days, validators=[validators.DataRequired()])
    kidem_tarihi = DateField("İşe Giriş Tarihi:", render_kw={"style": "border-radius: 10px;"})

# Password Change Form
class PasswordChangeForm(Form):
    oldpw = PasswordField("Eski Şifre", validators=[validators.DataRequired(message = "Boş bırakılamaz.")])
    newpw = PasswordField("Yeni Şifre", validators=[validators.Length(min = 5, max = 45), validators.DataRequired(message = "Boş bırakılamaz."), validators.EqualTo(fieldname = "confirm", message = "Yeni şifreniz eşleşmiyor.")])
    confirm = PasswordField("Yeni Şifre Tekrar")

# PCL/PDF job formu
class PclPdfForm(Form):
    file1 = FileField('Excel dosyasını yükle', validators=[FileRequired()])
    dosya_adi = StringField("Oluşturulacak Dosya Adı", render_kw={'style': 'width: 42ch; border-radius:10px;'})
    submit = SubmitField('Upload')
    # r'[\/:*?"<>|.]'

# SSH Sabah Raporu Form
class SSHSabahRaporuForm(Form):
    turkuazusername = StringField("Turkuaz Kullanıcı Adı", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    turkuazpw = PasswordField("Turkuaz Şifre", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    first_day_check = BooleanField("Geçen ay kümüle rapor")   

# Sabah Raporu Form
class SabahRaporuForm(Form):
    # Turkuaz Info is no longer in use after RPA part is changed to OraDB
    #turkuazusername = StringField("Turkuaz Kullanıcı Adı", render_kw={'style': 'width: 28ch; border-radius:10px;'})
    #turkuazpw = PasswordField("Turkuaz Şifre", render_kw={'style': 'width: 28ch; border-radius:10px;'})
    Ithalat_Perakende = StringField("İthalat adedi (perakende)", render_kw={'style': 'border-radius:10px;'})
    Ithalat_Filo = StringField("İthalat adedi (filo)", render_kw={'style': 'border-radius:10px;'})
    ToptanFatura_perakende = StringField("Toptan Fatura adedi (perakende)", render_kw={'style': 'border-radius:10px;'})
    ToptanFatura_filo = StringField("Toptan Fatura adedi (filo)", render_kw={'style': 'border-radius:10px;'})
    Euro_kur = StringField("Euro kuru (ithalat yapıldıysa)", render_kw={'style': 'border-radius:10px;'})
    SadeceBanaGonderilsin = BooleanField("Rapor sadece bana gönderilsin")

# Akşam Raporu Form
class AksamRaporuForm(Form):
    turkuazusername = StringField("Turkuaz Kullanıcı Adı", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    turkuazpw = PasswordField("Turkuaz Şifre", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    #potansiyel_yeniSuperb = StringField("Yeni Superb Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    #potansiyel_yeniOctavia = StringField("Yeni Octavia Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})

# 
class jato_form(Form):
    file1 = FileField('Kampanya Excelini Yükleyiniz', validators=[FileRequired()], render_kw={'style': 'width: 30ch; border-radius:10px; text-align:center'})

#
class odd_form(Form):
    current_year = datetime.datetime.now().year
    years = [(str(year), str(year)) for year in range(current_year, current_year - 10, -1)]
    year=SelectField('Yıl', choices=years, validators=[validators.DataRequired()])

    quarters = ['Q1','Q2','Q3', 'Q4']
    quarter=SelectField('Çeyrek', choices=quarters, validators=[validators.DataRequired()])

    file1 = FileField('ODD Dosyası', validators=[FileRequired()], render_kw={'style': 'width: 30ch; border-radius:10px; text-align:center'})

#
class satis_hedef_mail(Form):
    current_year = datetime.datetime.now().year
    years = [(str(year), str(year)) for year in range(current_year + 1, current_year - 1, -1)]
    year = SelectField('Yıl', choices=years, validators=[validators.DataRequired()])

    months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    month = SelectField('Ay', choices=months, validators=[validators.DataRequired()])

    email = StringField("Mail", validators=[validators.DataRequired()])
    password = PasswordField("Şifre",validators=[validators.DataRequired()])

    file1 = FileField('Hedef Exceli', validators=[FileRequired()], render_kw={'style': 'width: 30ch; border-radius:10px; text-align:center'})

    def __init__(self, *args, **kwargs):
        super(satis_hedef_mail, self).__init__(*args, **kwargs)
        # Set default values for year and month
        self.year.data = str(datetime.datetime.now().year)

class satis_ongoru_sabah_Form(Form):
    potansiyel_fabia = StringField("Fabia Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_kamiq = StringField("Kamiq Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_karoq = StringField("Karoq Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_kodiaq = StringField("Kodiaq Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_octavia = StringField("Octavia Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_scala = StringField("Scala Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_superb = StringField("Superb Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_elroq = StringField("Elroq Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_enyaq = StringField("Enyaq Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_enyaqcoupe = StringField("Enyaq Coupe Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    potansiyel_superbESportline = StringField("Superb E-Sportline Potansiyeli", render_kw={'style': 'width: 30ch; border-radius:10px;'})

    kurgu_fabia = StringField("Kurgu - Fabia", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_kamiq = StringField("Kurgu - Kamiq", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_karoq = StringField("Kurgu - Karoq", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_kodiaq = StringField("Kurgu - Kodiaq", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_octavia = StringField("Kurgu - Octavia", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_scala = StringField("Kurgu - Scala", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_superb = StringField("Kurgu - Superb", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_elroq = StringField("Kurgu - Elroq", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_enyaq = StringField("Kurgu - Enyaq", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_enyaqcoupe = StringField("Kurgu - Enyaq Coupe", render_kw={'style': 'width: 30ch; border-radius:10px;'})
    kurgu_superbESportline = StringField("Kurgu - Superb E-Sportline", render_kw={'style': 'width: 30ch; border-radius:10px;'})

    OncekiGunYOK = BooleanField("Rapora önceki gün eklenmesin!")
    SadeceBenimlePaylas = BooleanField("Raporu sadece benimle paylaş!")

class pdf_comparison_Form(Form):
    file1 = FileField('PDF 1:', validators=[FileRequired()], render_kw={'style': 'width: 30ch; border-radius:10px; text-align:center;'})
    file2 = FileField('PDF 2:', validators=[FileRequired()], render_kw={'style': 'width: 30ch; border-radius:10px; text-align:center;'})

#
class garanti_imha_user_detailreport(Form):
    SadeceBanaGonderilsin = BooleanField("Rapor sadece bana gönderilsin", render_kw={'style': 'width: 30ch;'})

class otomotiv_haberleri_Form(Form):
    haber_kategorisi = SelectField("Haber Kategorisi", choices=["Otomotiv", "Ekonomik", "Siyasi", "Diğer"])
    haber_tarihi = DateField("Haber Tarihi", validators=[DataRequired()])
    haber = TextAreaField("Haber", render_kw={"id": "haber", "style": "border-radius: 10px; height:35%"})

class yuce_auto_user_arac_ekleme_Form(Form):
    plaka_no = SelectField("Şirket Araçları", validators=[DataRequired()])
    model = StringField("Model", render_kw={'style': 'width: 40ch;', 'readonly': True})
    yil = StringField("Yıl", render_kw={'readonly': True})
    renk = StringField("Renk", render_kw={'readonly': True})
    km = StringField("KM")
    servis_gecmisi = FileField("Servis Geçmişi")
    eksper_raporu = FileField("Eksper Raporu")

    arac_teklif_formu = FileField("Araç Teklif Formu")

    arac_foto_1 = FileField("Araç Fotoğrafı 1")
    arac_foto_2 = FileField("Araç Fotoğrafı 2")
    arac_foto_3 = FileField("Araç Fotoğrafı 3")
    arac_foto_4 = FileField("Araç Fotoğrafı 4")
    arac_foto_5 = FileField("Araç Fotoğrafı 5")

    deadline_tarihi = DateField("Kapanış Tarihi:", render_kw={"style": "border-radius: 10px; width: 30%;"})
    mail_subject = StringField("Mail Konusu:")
    mail_body = TextAreaField("Mail İçeriği:")

    def __init__(self, *args, **kwargs):
        super(yuce_auto_user_arac_ekleme_Form, self).__init__(*args, **kwargs)
        self.populate_araceklemeForm_id() 

    def populate_araceklemeForm_id(self):
        # Missing source module removed from this workspace.
        results = []
        self.plaka_no.choices = [('', 'Plaka seçiniz')] + [(result[0], result[0]) for result in results]

class satistaki_araclar_Form(Form):
    ya_deadline = DateField("Yüce Auto Kapanış Tarihi", validators=[DataRequired()])

class bayii_user_teklif_verme_Form(Form):
    teklif = StringField("", validators=[Length(max=9)])
    teklif_ver_checkbox = BooleanField("") 
    aciklama = TextAreaField("Açıklama (İsteğe bağlı)")

class YA_user_teklif_verme_Form(Form):
    teklif_ver_checkbox = BooleanField("") 
    aciklama = TextAreaField("Açıklama (İsteğe bağlı)")

class BayiiRegisterForm(Form):
    def validate_name(form, field):
        if any(char.isdigit() for char in field.data):
            raise validators.ValidationError("İsim alanına sadece harf girişi yapılabilir.")
        
    def validate_surname(form, field):
        if any(char.isdigit() for char in field.data):
            raise validators.ValidationError("Soyisim alanına sadece harf girişi yapılabilir.")

    name = StringField("İsim", validators = [validators.Length(min = 2, max = 25), validate_name])
    surname = StringField("Soyisim", validators = [validators.Length(min = 2, max = 25), validate_surname])
    email = StringField("Email Adresi", validators = [validators.Email(message = "Lütfen Geçerli bir email adresi giriniz.")])
    password = PasswordField("Şifre:", validators=[validators.DataRequired(message = "Lütfen şifre giriniz."), validators.EqualTo(fieldname = "confirm", message = "Şifreniz uyuşmuyor.")])
    confirm = PasswordField("Şifre Doğrulama")

    DSD = BooleanField("DSD")
    Arac2El = BooleanField("2. El Araç Teklif")

    bayii = SelectField('Bayi')

    def __init__(self, *args, **kwargs):
        super(BayiiRegisterForm, self).__init__(*args, **kwargs)
        self.populate_bayii_choices()
    
    def populate_bayii_choices(self):
        from db_funcs import AssignDBContenttoListWithQuery
        from config import YA_2El_AracSatis
        Bayiler_listesi_isim = AssignDBContenttoListWithQuery(YA_2El_AracSatis, "SELECT dealerName FROM [Bayiiler] WHERE [isActive]=1 ORDER BY [dealerName] ASC;")
        self.bayii.choices = Bayiler_listesi_isim

class bayi_mail_tanim_ekrani_Form(Form):
    bayi_to = StringField("")
    bayi_cc = StringField("")

    mail_subject = StringField("Mail Konusu")
    mail_body = TextAreaField("Mail İçeriği")

class fiktif_bayi_mail_tanim_ekrani_Form(Form):
    bayi_to = StringField("")
    bayi_cc = StringField("")

    mail_subject = StringField("Mail Konusu")
    mail_body = TextAreaField("Mail İçeriği")

class fiktif_bayi_mailing_Form(Form):
    tarih = DateField("Tarih:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px"})
    tarih2 = DateField("Tarih (2):", render_kw={"style": "border-radius: 10px"})
    tarih3 = DateField("Tarih (3):", render_kw={"style": "border-radius: 10px"})
    mail_konu = StringField("Mail Konu:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px;", "readonly": True})
    mail_body = TextAreaField("Mail İçerik:", render_kw={"style": "border-radius: 10px;", "readonly": True})

class filo_fiktif_bayi_mail_tanim_ekrani_Form(Form):
    bayi_to = StringField("")
    bayi_cc = StringField("")

    mail_subject = StringField("Mail Konusu")
    mail_body = TextAreaField("Mail İçeriği")

class filo_fiktif_bayi_mailing_Form(Form):
    tarih = DateField("Tarih:", render_kw={"style": "border-radius: 10px"})
    tarih2 = DateField("Tarih (2):", render_kw={"style": "border-radius: 10px"})
    tarih3 = DateField("Tarih (3):", render_kw={"style": "border-radius: 10px"})
    mail_konu = StringField("Mail Konu:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px;", "readonly": True})
    mail_body = TextAreaField("Mail İçerik:", render_kw={"style": "border-radius: 10px;", "readonly": True})

class ys_faaliyet_raporu_Form(Form):
    gorusme_tarihi = DateField("Görüşme Tarihi:", default=date.today, validators=[DataRequired()], render_kw={"style": "border-radius: 10px; width: 50%;"})

    bayi_adi = SelectField("Bayi:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    
    aday_adi = StringField("Aday Adı:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    cinsiyet = RadioField("Cinsiyet:", choices=[('Kadın', 'Kadın'), ('Erkek', 'Erkek')], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    satis_servis = RadioField("Satış/Servis:", choices=[('Satış', 'Satış'), ('Servis', 'Servis')], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    aday_durumu = RadioField("Aday Durumu:", choices=[('Olumlu', 'Olumlu'), ('Olumsuz', 'Olumsuz'), ('Beklemede', 'Beklemede'), ('Diğer', 'Diğer')], render_kw={"style": "border-radius: 10px;"})
    aday_durumu_diger = SelectField("Diğer:", choices=[('', '--- SEÇİNİZ ---'), ('Aday Gelmedi', 'Aday Gelmedi'), ('Bayi İptal Etti', 'Bayi İptal Etti'), ('Pozisyon Kapandı', 'Pozisyon Kapandı')], render_kw={"style": "border-radius: 10px;"})
    sinav_sayisal = DecimalField("Sayısal:", render_kw={"style": "border-radius: 10px;"})
    sinav_sozel = DecimalField("Sözel:", render_kw={"style": "border-radius: 10px;"})
    sinav_envanter = DecimalField("Envanter:", render_kw={"style": "border-radius: 10px;"})
    pozisyon_adi = SelectField("Pozisyon Adı:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    aksiyon = RadioField("Terfi/İşe Alım:", choices=[('Terfi', 'Terfi'), ('İşe Alım', 'İşe Alım'), ('Rotasyon', 'Rotasyon')], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})

    bolgeci = StringField("Bölge Yöneticisi:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})

    gorusme_baglam = RadioField("Görüşme Ortamı:", choices=[('Yüz Yüze', 'Yüz Yüze'), ('Online', 'Online') ], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    
    ik_bolgeci = SelectField("İK Bölge Yöneticisi:", choices=[('Nurçin Bohur', 'Nurçin Bohur') ], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    ise_baslama_tarihi = DateField("İşe Başlama Tarihi:", render_kw={"style": "border-radius: 10px;"})
    isten_cikis_tarihi = DateField("İşten Çıkış Tarihi:", render_kw={"style": "border-radius: 10px;"})
    cv = FileField("Aday CV:", render_kw={"style": "border-radius: 10px;"})
    notlar = TextAreaField("Notlar:", render_kw={"style": "border-radius: 10px; height:35%"})

    def __init__(self, *args, **kwargs):
        super(ys_faaliyet_raporu_Form, self).__init__(*args, **kwargs)
        self.populate_bayii_choices()
        self.populate_position_choices()

    def populate_bayii_choices(self):
        from db_funcs import AssignDBContenttoListWithQuery
        from config import YuceDashboardDB
        Bayiler_listesi_isim = AssignDBContenttoListWithQuery(YuceDashboardDB, "SELECT [Name] from Bayi  WHERE Firm_ID NOT IN (24992,24953,24818,22002,1,23203) ORDER BY [Name]")
        Bayiler_listesi_isim = [(name, name) for name in Bayiler_listesi_isim]
        self.bayi_adi.choices = [('', '--- SEÇİNİZ ---'), ('', 'Yeni Bayi')] + Bayiler_listesi_isim
    
    def populate_position_choices(self):
        from db_funcs import AssignDBContenttoListWithQuery
        from config import YA_2El_AracSatis
        positions_listesi_isim = AssignDBContenttoListWithQuery(YA_2El_AracSatis, "SELECT [PozisyonAdi] FROM [Yuce_Portal].[dbo].[YS_Faaliyet_PozisyonAdları] WHERE active=1 ORDER BY PozisyonAdi;")
        positions_listesi_isim =[(name, name) for name in positions_listesi_isim]
        self.pozisyon_adi.choices = [('', '--- Seçiniz ---')] + positions_listesi_isim

class ys_faaliyet_raporu_listesi_Form(Form):
    aday_durumu = RadioField("Aday Durumu:", choices=[('Olumlu', 'Olumlu'), ('Olumsuz', 'Olumsuz'), ('Beklemede', 'Beklemede'), ('Diğer', 'Diğer')], render_kw={"style": "border-radius: 10px;"})
    aday_durumu_diger = SelectField("Diğer:", choices=[('', '--- SEÇİNİZ ---'), ('Aday Gelmedi', 'Aday Gelmedi'), ('Bayi İptal Etti', 'Bayi İptal Etti'), ('Pozisyon Kapandı', 'Pozisyon Kapandı')], render_kw={"style": "border-radius: 10px;"})
    sinav_sayisal = DecimalField("Sayısal:", render_kw={"style": "border-radius: 10px;"})
    sinav_sozel = DecimalField("Sözel:", render_kw={"style": "border-radius: 10px;"})
    sinav_envanter = DecimalField("Envanter:", render_kw={"style": "border-radius: 10px;"})
    ise_baslama_tarihi = DateField("İşe Başlama Tarihi:", render_kw={"style": "border-radius: 10px;"})
    isten_cikis_tarihi = DateField("İşten Çıkış Tarihi:", render_kw={"style": "border-radius: 10px;"})
    bildirme_tarihi = DateField("Bayi Bilgilendirilme Tarihi:", render_kw={"style": "border-radius: 10px;"})
    gorusme_tarihi = DateField("Görüşme Tarihi:", validators=[DataRequired()], render_kw={"style": "border-radius: 10px; width: 50%;"})
    ik_bolgeci = SelectField("İK Bölge Yöneticisi:", choices=[('Nurçin Bohur', 'Nurçin Bohur')], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    cv = FileField("Aday CV:", render_kw={"style": "border-radius: 10px;"})
    notlar = TextAreaField("Notlar:", render_kw={"style": "border-radius: 10px; height:35%"})
    gorusme_baglam = RadioField("Görüşme Ortamı:", choices=[('Yüz Yüze', 'Yüz Yüze'), ('Online', 'Online') ], validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})

class aylik_kurgu_Form(Form):
    yolda_status_excluded = BooleanField('Yolda Status Excluded')
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])

class GeciciAracTahsis_AracTanimlama_Form(Form):
    plaka_no = SelectField("Şirket Araçları", validators=[DataRequired()])
    sasi_no = StringField("Şasi No", render_kw={'readonly': True})
    model = StringField("Model", render_kw={'style': 'width: 40ch;', 'readonly': True})
    trafikCikis_Tarihi = StringField("Trafiğe Çıkış", render_kw={'readonly': True})
    renk = StringField("Renk", render_kw={'readonly': True})
    km = StringField("KM")
    YA_AlisTarihi = DateField("Yüce Auto'ya Alış", render_kw={"style": "border-radius: 10px;"}, validators=[DataRequired()])

    # Modal içerisindeki veriler

    ya_arac_satilma_tarihi = DateField("", render_kw={"style": "border-radius: 10px;"})
    arac_geri_alim_bedeli = StringField("")
    trafik_sigortasi = StringField("")
    kasko = StringField("")
    bakim_ve_onarim = StringField("")
    ikinci_el_satis_bedeli = StringField("")
    arac_maliyet_toplam = StringField("", render_kw={'readonly': True})
    fonlama_maliyeti = StringField("", render_kw={'readonly': True})
    ikame_arac_kullanim_gun_sayisi = StringField("")
    ikame_arac_kullanim_maliyeti = StringField("", render_kw={'readonly': True})
    kar_zarar = StringField("", render_kw={'readonly': True})
    
    
    def __init__(self, *args, **kwargs):
        super(GeciciAracTahsis_AracTanimlama_Form, self).__init__(*args, **kwargs)
        self.populate_arac_tahsis_plate_id() 

    def populate_arac_tahsis_plate_id(self):
        results = []
        # Missing source module removed from this workspace.
        self.plaka_no.choices = [('', 'Plaka seçiniz')] + [(result[0], result[0]) for result in results]
    
class GeciciAracTahsis_FonlamaOrani_Form(Form):
    months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    years = ['2025', '2026', '2027']
    ay = SelectField("Ay", choices=months)
    yil = SelectField("Yıl", choices=years)
    fonlama_orani = StringField("Fonlama Oranı (%)")

class GeciciAracTahsis_IkameAracBedeli_Form(Form):
    years = ['2024', '2025', '2026', '2027']
    yari_yil_values = [('1', '1. Yarıyıl'), ('2', '2. Yarıyıl')]
    yari_yil = SelectField("Yarı Yıl", choices=yari_yil_values, validators=[DataRequired()])
    models = SelectField("Model", validators=[DataRequired()])
    yil = SelectField("Yıl", choices=years, validators=[DataRequired()])
    ikame_arac_bedeli = StringField("İkame Araç Bedeli")

    def __init__(self, *args, **kwargs):
        super(GeciciAracTahsis_IkameAracBedeli_Form, self).__init__(*args, **kwargs)
        self.populate_arac_tahsis_models() 

    def populate_arac_tahsis_models(self):
        results = []
        # Missing source module removed from this workspace.
        self.models.choices = [('', 'Model seçiniz')] + [(result[0], result[0]) for result in results]

class GeciciAracTahsis_arac_ekleme_form(Form):
    arac_plaka = StringField("Araç Plaka")

class Dashboard_Yetkilendirme_Form(Form):
    bayi_adi = SelectField("Bayi")
    user_email = StringField("Kullanıcı E-mail")
    satis = BooleanField("Satış")
    servis = BooleanField("Servis")
    aktif_pasif = BooleanField("Aktif/Pasif", default=True)
    aciklama= StringField("Açıklama")

    def __init__(self, *args, **kwargs):
        super(Dashboard_Yetkilendirme_Form, self).__init__(*args, **kwargs)
        self.populate_bayii_choices()

    def populate_bayii_choices(self):
        from db_funcs import AssignDBContenttoListWithQuery
        from config import YA_2El_AracSatis
        Bayiler_listesi_isim = AssignDBContenttoListWithQuery(YA_2El_AracSatis, "SELECT [dealerName] FROM [YA_2El_AracSatis].[dbo].[Bayiiler] where [isActive]=1 ORDER BY [dealerName]")
        Bayiler_listesi_isim = [(name, name) for name in Bayiler_listesi_isim]
        self.bayi_adi.choices = [('', 'Bayi Seçiniz')] + Bayiler_listesi_isim

class Otopark_Rezerve_Form(Form):
    Tarih = DateField("Tarih", default=date.today, render_kw={"style": "border-radius: 10px;"}, validators=[DataRequired()])
    Otopark = SelectField("Otopark No", validators=[DataRequired()], render_kw={'style': 'border-radius:10px;'})
    Plaka = SelectField("Plaka", render_kw={'style': 'border-radius:10px;'})
    ofis_gunu_isaretle = BooleanField("Ofisten Çalışma Kaydet")

class Otopark_Iptal_Form(Form):
    aciklama = StringField("İptal Açıklaması", render_kw={'style': 'border-radius:10px;'})

class Otopark_Rapor_Form(Form):
    date = DateField("", default=date.today, render_kw={"style": "border-radius: 10px;"})
    park_status = BooleanField("")
    aciklama = StringField("")

class Kafeterya_Menu_Form(Form):
    menu_date = DateField("Tarih", default=date.today, render_kw={"style": "border-radius: 10px;"})
    Yemek1 = StringField("Çorba")
    Yemek2 = StringField("Ana Yemek")
    Yemek3 = StringField("Ana Yemek (2)")
    Yemek6 = StringField("Ana Yemek (3)")
    Yemek4 = StringField("Salata")
    Yemek5 = StringField("Garnitür")

    Yemek1_Fiyat = IntegerField("Fiyat")
    Yemek2_Fiyat = IntegerField("Fiyat")
    Yemek3_Fiyat = IntegerField("Fiyat")
    Yemek6_Fiyat = IntegerField("Fiyat")
    Yemek4_Fiyat = IntegerField("Fiyat")
    Yemek5_Fiyat = IntegerField("Fiyat")

    Not = TextAreaField("Not:")

def default_deadline():
    now = datetime.datetime.now()
    deadline = now + datetime.timedelta(days=7)
    return deadline.replace(hour=17, minute=0, second=0, microsecond=0)

class Add_Story_Form(Form):
    deadline_date_hr = DateTimeLocalField(
        "Gösterim Bitiş Tarihi",
        format="%Y-%m-%dT%H:%M",
        default=default_deadline,
        render_kw={"style": "border-radius: 10px;"}
    )
    image = FileField(
        "Hikaye Görseli Yükle",
        render_kw={"style": "margin-top: 10px; border-radius: 10px;"}
    )
    dept_adina_paylas = BooleanField("Departmanım Adına Paylaş")

class create_post_Form(Form):
    subject = StringField("Konu", render_kw={'style': 'border-radius:10px;'}, validators=[Length(max=64, message="Subject cannot exceed 200 characters.")])
    content = TextAreaField("İçerik", render_kw={"id": "editor", "style": "border-radius: 10px; height:35%"})
    image = FileField('Duyuru Görseli', validators=[FileRequired()], render_kw={'style': 'border-radius:10px; text-align:center'})
    mail_reminder = BooleanField("Mail yoluyla bilgilendir")
    YA_users = BooleanField("Yüce Auto için paylaş")
    YS_users = BooleanField("YS için paylaş")

class ForgotPasswordForm(Form):
    email = StringField("E-mail", render_kw={"style": "border-radius: 10px; width:250px"})

class UrunBilgileriForm(Form):
    talep_no           = IntegerField('Talep No', render_kw={"style": "border-radius: 10px;"})
    talep_edilen_urun  = StringField('Ürün Adı',       validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    talep_edilen_miktar= IntegerField('Miktar',        validators=[DataRequired(), NumberRange(min=1)], render_kw={"style": "border-radius: 10px;"})
    urun_birim_fiyat   = DecimalField('Birim Fiyat', render_kw={"style": "border-radius: 10px;"})
    para_birimi        = SelectField('Birim', choices=[('', '') ,('TL', 'TL'), ('Dolar', 'Dolar'), ('Euro', 'Euro')], render_kw={"style": "border-radius: 10px;"})
    urun_toplam_fiyat  = DecimalField('Toplam Fiyat',  validators=[DataRequired()], render_kw={"style": "border-radius: 10px;", 'readonly': True})
    butce_kalemi = SelectField('Bütçe Kalemi', choices=[
                                                    ('Bütçe Dışı', 'Bütçe Dışı'),
                                                    ('Bütçe 1', 'Bütçe 1'),
                                                    ('Bütçe 2', 'Bütçe 2')],
                                                    validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    teklif_pdf = FileField("Teklif PDF")

class SatinAlma_TeklifForm(Form):
    Miktar            = IntegerField('Miktar',        validators=[DataRequired(), NumberRange(min=1)], render_kw={"style": "border-radius: 10px;"})
    urun_birim_fiyat   = DecimalField('Birim Fiyat', render_kw={"style": "border-radius: 10px;"})
    para_birimi        = SelectField('Birim', choices=[('', '') ,('TL', 'TL'), ('Dolar', 'Dolar'), ('Euro', 'Euro')], render_kw={"style": "border-radius: 10px;"})
    urun_toplam_fiyat  = DecimalField('Toplam Fiyat',  validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    urun_tedarikci     = StringField('Ürün Tedrik Eden Firma', render_kw={"style": "border-radius: 10px;"})
    teklif_pdf = FileField("Teklif PDF")
    satin_alma_sorumlu_aciklama = TextAreaField("Açıklama", render_kw={"style": "border-radius: 10px;"}) 

class SatinAlmaForm(Form):
    talep_eden_dept = StringField('Talep Eden Departman', render_kw={'readonly': True})
    talep_edilen_dept = SelectField('Talep Kategorisi', choices=[
                                                    ('', 'Kategori Seçiniz'),
                                                    ('Danışmanlık Hizmetleri', 'Danışmanlık Hizmetleri'),
                                                    ('Eğitim Hizmetleri', 'Eğitim Hizmetleri'),
                                                    ('Pazarlama', 'Pazarlama'),
                                                    ('Bilgi Teknolojileri (IT)', 'Bilgi Teknolojileri (IT)'),
                                                    ('Bayi Geliştirme', 'Bayi Geliştirme'),
                                                    ('E-Mobilite', 'E-Mobilite'),
                                                    ('Diğer', 'Diğer')],
                                                    validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    talep_tarihi    = DateField('Tarih', validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"})
    items           = FieldList(FormField(UrunBilgileriForm), min_entries=1, max_entries=20, render_kw={"style": "border-radius: 10px;"})
    aciklama = TextAreaField("Açıklama (Talep Sahibi):", render_kw={"style": "border-radius: 10px; height:15%"})
    final_total     = StringField('Genel Toplam:', validators=[DataRequired()], render_kw={"style": "border-radius: 10px;", 'readonly': True})
    finans_aciklama = TextAreaField("Açıklama (Finansal Raporlama, Bütçe ve İç Kontrol Birimi):", render_kw={"style": "border-radius: 10px; height:15%"})

class SatinAlmaKriterForm(Form):
    satin_alma_muduru_limit = IntegerField("İnsan Kaynakları Müdürü Onay Limiti", render_kw={"style": "border-radius: 10px;"})
    cfo_limit = IntegerField("Mali İşler Genel Müdür Yardımcısı Onay Limiti", render_kw={"style": "border-radius: 10px;"})
    ceo_limit = IntegerField("Genel Müdür Onay Limiti", render_kw={"style": "border-radius: 10px;"})

class Soru_veya_Oneri_Form(Form):
    modul = SelectField(
        'Modül',
        choices=[
            ('', 'Kategori Seçiniz'),
            ('Haftalık Takvim', 'Haftalık Takvim'),
            ('Otopark', 'Otopark'),
            ('Organizasyon Şeması', 'Organizasyon Şeması'),
            ('Rozetler', 'Rozetler'),
            ('DSD', 'DSD'),
            ('Hikaye Ekleme', 'Hikaye Ekleme'),
            ('Duyurular', 'Duyurular'),
            ('RPA Raporu', 'RPA Raporu'),
            ('Profil Syfası', 'Profil Syfası'),
            ('Vive Cafe Menu', 'Vive Cafe Menu'),
            ('Yugii', 'Yugii'),
            ('Satın Alma', 'Satın Alma'),
            ('Diğer', 'Diğer')
        ],
        validators=[DataRequired()],
        render_kw={"style": "border-radius: 10px;"}
    )
    soru_oneri = TextAreaField("Soru / Öneri", render_kw={"style": "border-radius: 10px;"}) 
    onerimi_herkes_gorsun = BooleanField("Önerim herkes tarafından gözüksün")

class DC_Sarj_Rezerv_Form(Form):
    plaka = SelectField("Plaka", render_kw={'style': 'border-radius:10px;'})
    istasyon = SelectField("İstasyon No", choices=[
                                        ('', 'İstasyon Seçiniz'),
                                        ('Giriş 1', 'Giriş 1'),
                                        ('Giriş 2', 'Giriş 2'),
                                        #('İstasyon 1', 'İstasyon 1'),
                                        ('İstasyon 2', 'İstasyon 2'),
                                        ('İstasyon 3', 'İstasyon 3'),
                                        ('İstasyon 4', 'İstasyon 4')],
                                        validators=[DataRequired()], render_kw={'style': 'border-radius:10px;'})
    tarih = DateField("Tarih", default=date.today, render_kw={"style": "border-radius: 10px;"}, validators=[DataRequired()])
    saat = SelectField("Saat", choices=[
                                        ('', 'Saat Seçiniz'),
                                        ('00:00', '00:00'),
                                        ('01:00', '01:00'),
                                        ('02:00', '02:00'),
                                        ('03:00', '03:00'),
                                        ('04:00', '04:00'),
                                        ('05:00', '05:00'),
                                        ('06:00', '06:00'),
                                        ('07:00', '07:00'),
                                        ('08:00', '08:00'),
                                        ('09:00', '09:00'),
                                        ('10:00', '10:00'),
                                        ('11:00', '11:00'),
                                        ('12:00', '12:00'),
                                        ('13:00', '13:00'),
                                        ('14:00', '14:00'),
                                        ('15:00', '15:00'),
                                        ('16:00', '16:00'),
                                        ('17:00', '17:00'),
                                        ('18:00', '18:00'),
                                        ('19:00', '19:00'),
                                        ('20:00', '20:00'),
                                        ('21:00', '21:00'),
                                        ('22:00', '22:00'),
                                        ('23:00', '23:00')],
                                        validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"},)

class AC_Sarj_Rezerv_Form(Form):
    plaka = SelectField("Plaka", render_kw={'style': 'border-radius:10px;'})
    istasyon = SelectField("İstasyon No", choices=[
                                        ('', 'İstasyon Seçiniz'),
                                        ('İstasyon 5', 'İstasyon 5'),
                                        ('İstasyon 6', 'İstasyon 6'),
                                        ('İstasyon 7', 'İstasyon 7'),
                                        ('İstasyon 8', 'İstasyon 8'),
                                        ('İstasyon 9', 'İstasyon 9')],
                                        validators=[DataRequired()], render_kw={'style': 'border-radius:10px;'})
    tarih = DateField("Tarih", default=date.today, render_kw={"style": "border-radius: 10px;"}, validators=[DataRequired()])
    saat = SelectField("Saat", choices=[
                                        ('', 'Saat Seçiniz'),
                                        ('00:00', '00:00'),
                                        ('06:00', '06:00'),
                                        ('12:00', '12:00'),
                                        ('18:00', '18:00')],
                                        validators=[DataRequired()], render_kw={"style": "border-radius: 10px;"},)
    
class DSD_Onay_Form(Form):
    onay1 = BooleanField("İlgi alanlarınıza ve ihtiyaçlarınıza göre tasarlanmış pazarlama ve tanıtım faaliyetlerinde kişisel verilerinizi kullanmak istiyoruz.", validators=[validators.DataRequired()])
    onay2 = BooleanField("Kampanya, teklif, değerlendirme ve anketlerimizle ilgili olarak aşağıdaki iletişim bilgileriniz üzerinden sizlere ulaşmak istiyoruz.", validators=[validators.DataRequired()])
    onay3 = BooleanField("Aydınlatma metninde anılan amaçlarla, kişisel verilerinizi, Doğuş Bilgi İşlem ve Teknoloji Hizmetleri A.Ş, Doğuş Holding A.Ş ile onun iştirakleri/bağlı ortaklıklarıyla ve aydınlatma metninde geçen sözleşme ilişkisi içerisinde olduğumuz üçüncü taraflarla paylaşmak istiyoruz.", validators=[validators.DataRequired()])

# BÖLGESEL

class SatisChecklistForm(Form):
    kategori = SelectField(
        "Kategori",
        choices=[
            ("", "--- Seçiniz ---"),
            ("Müşteri", "Müşteri"),
            ("Süreç", "Süreç"),
            ("Raporlama", "Raporlama"),
            ("Hedef", "Hedef"),
            ("Diğer", "Diğer"),
        ],
        validators=[DataRequired(message="Kategori seçiniz.")],
        render_kw={"style": "border-radius: 10px;"}
    )

    etki_alani = SelectField(
        "Etki Alanı",
        choices=[("", "--- Seçiniz ---"), ("1","1"), ("2","2"), ("3","3"), ("4","4"), ("5","5")],
        validators=[DataRequired(message="Etki Alanı seçiniz.")],
        render_kw={"style": "border-radius: 10px;"}
    )

    baslik = StringField(
        "Başlık",
        validators=[DataRequired(message="Başlık giriniz."), Length(max=255)],
        render_kw={"style": "border-radius: 10px;"}
    )

    onem_derecesi = SelectField(
        "Önem Derecesi",
        choices=[(0, "Normal"), (1, "Kritik")],
        coerce=int,
        validators=[DataRequired()],
        render_kw={"style": "border-radius: 10px;"}
    )

    zorunlu_alan = BooleanField("Zorunlu?")
    hedef_baslik = BooleanField("Hedef?")

    def __init__(self, *args, kategori_choicelari=None, etki_alan_choicelari=None, **kwargs):
        super().__init__(*args, **kwargs)

        if kategori_choicelari:
            self.kategori.choices = [("", "--- Seçiniz ---")] + [
                (k, k) if isinstance(k, str) else k for k in kategori_choicelari
            ]

        if etki_alan_choicelari:
            self.etki_alani.choices = [("", "--- Seçiniz ---")] + [
                (e, e) if isinstance(e, str) else e for e in etki_alan_choicelari
            ]

PHOTO_SECTIONS = [("","--- Seçiniz ---"), ("Showroom", "Showroom"), ("Dış Cephe", "Dış Cephe"), ("Araç Teslim Alanı", "Araç Teslim Alanı"), 
                  ("Giriş", "Giriş"), ("Servis", "Servis"), ("Mekanik Atölye", "Mekanik Atölye"), ("Kaporta Atölye", "Kaporta Atölye"),
                  ("Boya Atölye", "Boya Atölye")]

class BayiPhotoEntry(Form):
    photo = FileField("Fotoğraf", validators=[Optional(), FileAllowed(["jpg","jpeg","png","webp","gif"], "Sadece resim dosyaları yükleyin.")])

    photo_desc = SelectField(
        "Fotoğraf Bölümü",
        choices=PHOTO_SECTIONS,
        validators=[Optional()],
        render_kw={"style": "border-radius: 10px;"}
    )

    existing_file_path         = HiddenField()
    existing_original_filename = HiddenField()
    existing_content_type      = HiddenField()
    existing_file_size         = HiddenField()

class bayi_bilgileri_edit_Form(Form):
    acilis_tarihi = DateField("Bayi Açılış Tarihi", validators=[Optional()], render_kw={"style": "border-radius: 10px;"})
    firma_sahipleri = FieldList(StringField("Firma Sahibi", render_kw={"style": "border-radius: 10px;"}),min_entries=1,max_entries=50)
    maps_link =  StringField("Maps Linki", render_kw={"style": "border-radius: 10px;"})
    digital_showroom = BooleanField("Digital Showroom var")
    digital_since = DateField("Ne zamandan beri dijital?", validators=[Optional()], render_kw={"style": "border-radius: 10px;"})
    has_360kw = BooleanField("360 kW var")
    iso_performansi = SelectField(
        "ISO performansı",
        choices=[
            ("", "--- Seçiniz ---"),
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
        ],
        validators=[Optional()],
        render_kw={"style": "border-radius: 10px;"}
    )
    iso_not = TextAreaField("ISO Notu (opsiyonel)", validators=[Optional()], render_kw={"style": "border-radius: 10px;"})
    bayi_resimleri = FieldList(FormField(BayiPhotoEntry), min_entries=1, max_entries=100)

    def validate(self):
        ok = super().validate()
        if self.digital_showroom.data and not self.digital_since.data:
            self.digital_since.errors.append("Digital showroom için başlangıç tarihini giriniz.")
            ok = False
        return ok


class KismiKatilimSatiri(Form):
    participant_id = HiddenField()
    kismi     = BooleanField("Kısmi?")
    baslangic = DateField("Ziyaret Başlangıç Tarihi", validators=[Optional()], render_kw={"type": "date"})
    bitis     = DateField("Ziyaret Bitiş Tarihi",     validators=[Optional()], render_kw={"type": "date"})

class BayiZiyaretOlusturmaForm(Form):
    bayi = SelectField("Ziyaret Edilecek Bayi", choices=[], coerce=int, validators=[DataRequired()])
    ziyaret_tipi = SelectField("Ziyaret Tipi", choices=[("satış", "Satış"), ("ssh", "SSH"), ("bayi geliştirme", "Bayi Geliştirme")], validators=[DataRequired()])
    sebep = SelectField("Ziyaret Sebebi", choices=[("", "Seçiniz"), ("Genel", "Genel"), ("Denetim", "Denetim"), ("Eğitim", "Eğitim")], validators=[DataRequired()])
    baslangic = DateField("Ziyaret Başlangıç Tarihi", validators=[DataRequired()], render_kw={"type": "date"})
    bitis     = DateField("Ziyaret Bitiş Tarihi",     validators=[DataRequired()], render_kw={"type": "date"})

    satis_bolgeci = StringField("Satış Bölge Yöneticisi", render_kw={"readonly": True})
    ssh_bolgeci   = StringField("SSH Bölge Yöneticisi",   render_kw={"readonly": True})

    katilimcilar = SelectMultipleField("Katılımcılar", choices=[], coerce=int)

    kismi_katilim_satirlari = FieldList(FormField(KismiKatilimSatiri), min_entries=0, max_entries=200)

    notlar = TextAreaField("Not:", render_kw={"style": "border-radius: 10px; height:25%"})

    def __init__(self, *args, bayiler=None, kisiler=None, satis_bolgeci_adi=None, ssh_bolgeci_adi=None, **kwargs):
        super().__init__(*args, **kwargs)

        if bayiler:
            self.bayi.choices = [(int(b[0]), b[1]) for b in bayiler]
        if kisiler:
            self.katilimcilar.choices = [(int(k[0]), k[1]) for k in kisiler]

        if satis_bolgeci_adi:
            self.satis_bolgeci.data = satis_bolgeci_adi
        if ssh_bolgeci_adi:
            self.ssh_bolgeci.data = ssh_bolgeci_adi

class BayiZiyaretForm(Form):
    bayi_dis = FileField("Bayi Dış Cephe", render_kw={"multiple": True})
    showroom = FileField("Showroom", render_kw={"multiple": True})
    resepsiyon = FileField("Resepsiyon", render_kw={"multiple": True})
    sarj_istasyonlari = FileField("Şarj İstasyonları", render_kw={"multiple": True})
    test_araclari = FileField("Test Araçları", render_kw={"multiple": True})

    Pazarlama_calismalari = TextAreaField("Pazarlama Çalışmaları")
    personel = TextAreaField("Personel")
    is_gelistirme = TextAreaField("İş Geliştirme")
    Genel_Degerlendirme = TextAreaField("Genel Değerlendirme")
