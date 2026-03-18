import os
from pathlib import Path
from dotenv import load_dotenv

_CONFIG_DIR = Path(__file__).resolve().parent
for _env_path in (_CONFIG_DIR / ".env", _CONFIG_DIR.parent / ".env"):
    if _env_path.exists():
        load_dotenv(_env_path)
        break
else:
    load_dotenv()


sabahraporu_email=os.getenv("sabahraporu_email")
sabahraporu_email_Password=os.getenv("sabahraporu_email_Password")

mailName=os.getenv("mailName")
aksamrapor_mailName=os.getenv("aksamrapor_mailName")

yuceportal_mail=os.getenv("yuceportal_mail")
yuceportal_pwd=os.getenv("yuceportal_pwd")


Skoda_Satis_Stok_Raporu=os.getenv("Skoda_Satis_Stok_Raporu")
Model_Kirilimli=os.getenv("Model_Kirilimli")


YuceDB=os.getenv("YuceDB")
YuceDashboardDB=os.getenv("YuceDashboardDB")
YA_2El_AracSatis=os.getenv(
    "YA_2El_AracSatis",
    r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.0.0.20\SQLYC;DATABASE=YA_2El_AracSatis;UID=YuceUser;PWD=APTw7r2C",
)
Garanti_imha_DB=os.getenv("Garanti_imha_DB")
SkodabotDB=os.getenv("SkodabotDB")

Jira_API_KEY=os.getenv("Jira_API_KEY")

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


YA_RPA_MYSQL = {
    "host": os.getenv("YA_RPA_MYSQL_HOST"),
    "user": os.getenv("YA_RPA_MYSQL_USER"),
    "password": os.getenv("YA_RPA_MYSQL_PASSWORD"),
    "database": os.getenv("YA_RPA_MYSQL_DATABASE")
}


username=os.getenv("username")
userpwd=os.getenv("userpwd")
host=os.getenv("host")
port=os.getenv("port")
service_name=os.getenv("service_name")
dsn=os.getenv("dsn")



bilgilendirme_mail=os.getenv("bilgilendirme_mail")
bilgilendirme_mail_pw=os.getenv("bilgilendirme_mail_pw")


satin_alma_sorumlulari_aslist = ["zeynepg", "oguzt"]
satin_alma_finans_sorumlulari_aslist = ["ugurcana"]




MS_CLIENT_ID=os.getenv("MS_CLIENT_ID")
MS_TENANT_ID=os.getenv("MS_TENANT_ID")
MS_AUTHORITY=os.getenv("MS_AUTHORITY")
MS_CLIENT_SECRET=os.getenv("MS_CLIENT_SECRET")







PHOTO_SAVE_ROOT = r"C:\Users\yuceappadmin\Documents\GitHub\RPA-Projects\static\bolgesel_bayi_resimleri"
PHOTO_WEB_ROOT = "bolgesel_bayi_resimleri"
MS_SCOPES = ["User.Read", "Calendars.ReadWrite"]
MS_REDIRECT_PATH = "/ms-auth/redirect"
MS_REDIRECT_URI = "https://yuceportal.skoda.com.tr/ms-auth/redirect"

fiktif_araclar_mail_subject = "Fiktifteki Araçlar"
fiktif_araclar_mail_body = "Değerli Yetkili Satıcımız,<br><br>Aşağıdaki araçlarınız fiktif konumludur ve fiktif çekim talepleri bulunmamaktadır.<br><br>Aşağıdaki araçlara **.**.**** tarihli talep girilmesini rica ederiz.<br><br>İyi çalışmalar."
fiktif_araclar_mail_subject_filo = "Filo - Stok ve Fiktif Konumundaki Araçlar Hakkında"
fiktif_araclar_mail_body_filo = "Değerli Yetkili Satıcımız,<br><br>Aşağıda bilgileri bulunan araçlar stok ve fiktif konumunda bulunup, fatura talepleri iletilmemiştir.<br><br> Tüm araçlar için sevk yeri bilgileri ve fatura onaylarının iletilmesini önemle rica ederiz.<br><br>İyi çalışmalar,<br>Skoda Filo Satış Departmanı"
