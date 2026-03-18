from datetime import datetime, timedelta
import warnings
import calendar
import pymysql
warnings.filterwarnings("ignore", category=DeprecationWarning)
from satis_ongoru_sabah.satis_ongoru_sabah_email_html import satis_ongoru_sabah_email_html
from format_with_period import format_with_period
from satis_ongoru_sabah.satis_ongoru_sabah_ora import *
from send_email import send_email, send_email_2
from config import *


def Satis_Ongoru_Sabah_Complete(potansiyel_fabia, potansiyel_scala, potansiyel_octavia, potansiyel_superb, potansiyel_kamiq, potansiyel_karoq, potansiyel_kodiaq, kurgu_fabia, kurgu_scala, kurgu_octavia, kurgu_superb, kurgu_kamiq, kurgu_karoq, kurgu_kodiaq, OncekiGunYOK):
    today = datetime.today().strftime("%d-%m-%Y")
    today = today.replace("-", ".")
    month_start = "01" + today[2:].replace("-", ".")
    yil = datetime.now().year
    year_start = '01.01.' + str(yil)

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()

    date_obj = datetime.strptime(today, "%d.%m.%Y")
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
    last_day_date = datetime(date_obj.year, date_obj.month, last_day)
    is_sunday = last_day_date.weekday() == 6

    # HOW MANY SUNDAYS ARE THERE IN THE CURRENT MONTH
    num_days = calendar.monthrange(date_obj.year, date_obj.month)[1]
    sundays_count = 0
    for day in range(1, num_days + 1):
        if datetime(date_obj.year, date_obj.month, day).weekday() == 6:
            sundays_count += 1

    # IF THE LAST DAY OF THE MONTH IS SUNDAY 
    if is_sunday:
        num_days_in_month = (num_days - (0.5 * sundays_count)) - 0.5
    else:
        num_days_in_month = (num_days - (0.5 * sundays_count)) - 1
    
    import math
    num_days_in_month = math.ceil(num_days_in_month)
    
    todays_day = date_obj.day
    if todays_day != 1:
        todays_day -= 1
        yesterday = date_obj - timedelta(days=1)
        yesterday = yesterday.strftime("%d.%m.%Y")
    else:
        todays_day = todays_day
        yesterday = date_obj
        yesterday = yesterday.strftime("%d.%m.%Y")

    if todays_day >= num_days_in_month:
        num_days_in_month = int(today[0:2])

    fatura_adetleri_asdict = return_fatura_adetleri_fromOraDB(month_start, yesterday)
    baglanti_adetleri_asdict = return_baglanti_adetleri_fromOraDB(today, today)

    def replace_turkish_characters_and_words(dictionary):
        turkish_to_english = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
        new_dict = {}
        for key, value in dictionary.items():
            new_key = key.translate(turkish_to_english)
            new_key = new_key.replace("Yeni ", "").replace("Combi", "").lower()
            new_key = new_key.strip()
            if new_key in new_dict:
                new_dict[new_key] += value
            else:
                new_dict[new_key] = value
        return new_dict

    fatura_adetleri_asdict = replace_turkish_characters_and_words(fatura_adetleri_asdict)
    baglanti_adetleri_asdict = replace_turkish_characters_and_words(baglanti_adetleri_asdict)

    if "fabia" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["fabia"] = 0
    if "scala" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["scala"] = 0
    if "octavia" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["octavia"] = 0
    if "superb" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["superb"] = 0
    if "kamiq" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["kamiq"] = 0
    if "karoq" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["karoq"] = 0
    if "kodiaq" not in baglanti_adetleri_asdict:
        baglanti_adetleri_asdict["kodiaq"] = 0    
    
    if "fabia" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["fabia"] = 0
    if "scala" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["scala"] = 0
    if "octavia" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["octavia"] = 0
    if "superb" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["superb"] = 0
    if "kamiq" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["kamiq"] = 0
    if "karoq" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["karoq"] = 0
    if "kodiaq" not in fatura_adetleri_asdict:
        fatura_adetleri_asdict["kodiaq"] = 0

    def sum_values_of_dicts(dict1, dict2):
        summed_dict = {}
        for key in dict1:
            summed_value = dict1[key] + dict2.get(key, 0)
            summed_dict[key] = summed_value
        return summed_dict
    
    def WriteTextInto_txt(filepath, content):
        with open(filepath, 'r', encoding='utf-8') as file:
            txtfile_content = file.read()
        with open(filepath, 'w', encoding='utf-8') as file:
            pass
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        return txtfile_content
    

    toplam_asdict = sum_values_of_dicts(fatura_adetleri_asdict, baglanti_adetleri_asdict)

    daily_pred_asdict = {}
    monthly_pred_asdict = {}
    for key in toplam_asdict:
        daily_pred = round(toplam_asdict[key] / todays_day)
        daily_pred_asdict[key] = daily_pred
        monthly_pred_asdict[key] = round(toplam_asdict[key] / todays_day * num_days_in_month)
    

    if "fabia" not in monthly_pred_asdict:
        fixed_pred_fabia = 0
        bg_fabia = "#fff"
    if "scala" not in monthly_pred_asdict:
        fixed_pred_scala = 0
        bg_scala = "#fff"
    if "octavia" not in monthly_pred_asdict:
        fixed_pred_octavia = 0
        bg_scala = "#fff"
    if "superb" not in monthly_pred_asdict:
        fixed_pred_superb = 0
        bg_superb = "#fff"
    if "kamiq" not in monthly_pred_asdict:
        fixed_pred_kamiq = 0
        bg_kamiq = "#fff"
    if "karoq" not in monthly_pred_asdict:
        fixed_pred_karoq = 0
        bg_karoq = "#fff"
    if "kodiaq" not in monthly_pred_asdict:
        fixed_pred_kodiaq = 0
        bg_kodiaq = "#fff"

    for key in monthly_pred_asdict:
        if key == "fabia":
            if monthly_pred_asdict[key] > potansiyel_fabia:
                fixed_pred_fabia = potansiyel_fabia
                bg_fabia = "#f7b046"
            else:
                fixed_pred_fabia = monthly_pred_asdict[key]
                bg_fabia = "#fff"
            if potansiyel_fabia != 0:
                perc_fabia = "%" + str(round((fixed_pred_fabia/potansiyel_fabia)*100))
            else:
                perc_fabia = "-"
        elif  key == "scala":
            if monthly_pred_asdict[key] > potansiyel_scala:
                fixed_pred_scala = potansiyel_scala
                bg_scala = "#f7b046"
            else:
                fixed_pred_scala = monthly_pred_asdict[key]
                bg_scala = "#fff"
            if potansiyel_scala != 0:
                perc_scala = "%" + str(round((fixed_pred_scala/potansiyel_scala)*100))
            else:
                perc_scala = "-"
        elif  key == "octavia":
            if monthly_pred_asdict[key] > potansiyel_octavia:
                fixed_pred_octavia = potansiyel_octavia
                bg_octavia = "#f7b046"
            else:
                fixed_pred_octavia = monthly_pred_asdict[key]
                bg_octavia = "#fff"
            if potansiyel_octavia != 0:
                perc_octavia = "%" + str(round((fixed_pred_octavia/potansiyel_octavia)*100))
            else:
                perc_octavia = "-"
        elif  key == "superb":
            if monthly_pred_asdict[key] > potansiyel_superb:
                fixed_pred_superb = potansiyel_superb
                bg_superb = "#f7b046"
            else:
                fixed_pred_superb = monthly_pred_asdict[key]
                bg_superb = "#fff"
            if potansiyel_superb != 0:
                perc_superb = "%" + str(round((fixed_pred_superb/potansiyel_superb)*100))
            else:
                perc_superb = "-"
        elif  key == "kamiq":
            if monthly_pred_asdict[key] > potansiyel_kamiq:
                fixed_pred_kamiq = potansiyel_kamiq
                bg_kamiq = "#f7b046"
            else:
                fixed_pred_kamiq = monthly_pred_asdict[key]
                bg_kamiq = "#fff"
            if potansiyel_kamiq != 0:
                perc_kamiq = "%" + str(round((fixed_pred_kamiq/potansiyel_kamiq)*100))
            else:
                perc_kamiq = "-"
        elif  key == "karoq":
            if monthly_pred_asdict[key] > potansiyel_karoq:
                fixed_pred_karoq = potansiyel_karoq
                bg_karoq = "#f7b046"
            else:
                fixed_pred_karoq = monthly_pred_asdict[key]
                bg_karoq = "#fff"
            if potansiyel_karoq != 0:
                perc_karoq = "%" + str(round((fixed_pred_karoq/potansiyel_karoq)*100))
            else:
                perc_karoq = "-"
        elif  key == "kodiaq":
            if monthly_pred_asdict[key] > potansiyel_kodiaq:
                fixed_pred_kodiaq = potansiyel_kodiaq
                bg_kodiaq = "#f7b046"
            else:
                fixed_pred_kodiaq = monthly_pred_asdict[key]
                bg_kodiaq = "#fff"
            if potansiyel_kodiaq != 0:
                perc_kodiaq = "%" + str(round((fixed_pred_kodiaq/potansiyel_kodiaq)*100))
            else:
                perc_kodiaq = "-"
    
    baglanti_sum = sum(baglanti_adetleri_asdict.values())
    fatura_sum = sum(fatura_adetleri_asdict.values())
    toplam_sum = sum(toplam_asdict.values())
    daily_sum = sum(daily_pred_asdict.values())
    monthly_sum = sum(monthly_pred_asdict.values())
    potansiyel_sum = potansiyel_fabia + potansiyel_scala + potansiyel_octavia + potansiyel_superb + potansiyel_kamiq + potansiyel_karoq + potansiyel_kodiaq
    fixed_sum = fixed_pred_fabia + fixed_pred_scala + fixed_pred_octavia + fixed_pred_superb + fixed_pred_kamiq + fixed_pred_karoq + fixed_pred_kodiaq
    perc_sum = "%" + str(round((fixed_sum/potansiyel_sum)*100))

    if monthly_sum > potansiyel_sum:
        bg_sum = "#f7b046"
    else:
        bg_sum = "#fff"


    lastcol_fabia = "%" + str(round((fixed_pred_fabia / kurgu_fabia)*100))
    lastcol_scala = "%" + str(round((fixed_pred_scala / kurgu_scala)*100))
    lastcol_octavia = "%" + str(round((fixed_pred_octavia / kurgu_octavia)*100))
    lastcol_superb = "%" + str(round((fixed_pred_superb / kurgu_superb)*100))
    lastcol_kamiq = "%" + str(round((fixed_pred_kamiq / kurgu_kamiq)*100))
    lastcol_karoq = "%" + str(round((fixed_pred_karoq / kurgu_karoq)*100))
    lastcol_kodiaq = "%" + str(round((fixed_pred_kodiaq / kurgu_kodiaq)*100))

    kurgu_toplam = kurgu_fabia + kurgu_scala + kurgu_octavia + kurgu_superb + kurgu_kamiq + kurgu_karoq + kurgu_kodiaq

    lastcol_toplam = "%" + str(round((fixed_sum / kurgu_toplam)*100))

    email_body_start = f"""
            <p>Değerli Yöneticilerimiz ve Çalışma Arkadaşlarımız,</p>
            <p>{today} tarihli Öngörü raporunu bilgilerinize sunarız.</p>
            <p>İyi çalışmalar.</p>
            <br>
        """
    
    email_body = satis_ongoru_sabah_email_html.format(today, 
    baglanti_adetleri_asdict["fabia"], fatura_adetleri_asdict["fabia"], toplam_asdict["fabia"], daily_pred_asdict["fabia"], monthly_pred_asdict["fabia"], bg_fabia, potansiyel_fabia, bg_fabia, fixed_pred_fabia, perc_fabia, kurgu_fabia, lastcol_fabia,
    baglanti_adetleri_asdict["scala"], fatura_adetleri_asdict["scala"], toplam_asdict["scala"], daily_pred_asdict["scala"], monthly_pred_asdict["scala"], bg_scala, potansiyel_scala, bg_scala, fixed_pred_scala, perc_scala, kurgu_scala, lastcol_scala,
    baglanti_adetleri_asdict["octavia"], fatura_adetleri_asdict["octavia"], toplam_asdict["octavia"], daily_pred_asdict["octavia"], monthly_pred_asdict["octavia"], bg_octavia, potansiyel_octavia, bg_octavia, fixed_pred_octavia, perc_octavia, kurgu_octavia, lastcol_octavia,
    baglanti_adetleri_asdict["superb"], fatura_adetleri_asdict["superb"], toplam_asdict["superb"], daily_pred_asdict["superb"], monthly_pred_asdict["superb"], bg_superb, potansiyel_superb, bg_superb, fixed_pred_superb, perc_superb, kurgu_superb, lastcol_superb,
    baglanti_adetleri_asdict["kamiq"], fatura_adetleri_asdict["kamiq"], toplam_asdict["kamiq"], daily_pred_asdict["kamiq"], monthly_pred_asdict["kamiq"], bg_kamiq, potansiyel_kamiq, bg_kamiq, fixed_pred_kamiq, perc_kamiq, kurgu_kamiq, lastcol_kamiq,
    baglanti_adetleri_asdict["karoq"], fatura_adetleri_asdict["karoq"], toplam_asdict["karoq"], daily_pred_asdict["karoq"], monthly_pred_asdict["karoq"], bg_karoq, potansiyel_karoq, bg_karoq, fixed_pred_karoq, perc_karoq, kurgu_karoq, lastcol_karoq,
    baglanti_adetleri_asdict["kodiaq"], fatura_adetleri_asdict["kodiaq"], toplam_asdict["kodiaq"], daily_pred_asdict["kodiaq"], monthly_pred_asdict["kodiaq"], bg_kodiaq, potansiyel_kodiaq, bg_kodiaq, fixed_pred_kodiaq, perc_kodiaq, kurgu_kodiaq, lastcol_kodiaq,
    baglanti_sum, fatura_sum, toplam_sum, daily_sum, monthly_sum, bg_sum, potansiyel_sum, bg_sum, fixed_sum, perc_sum, kurgu_toplam, lastcol_toplam)

    txtfile_content = WriteTextInto_txt("satis_ongoru_sabah\prevday_html.txt", email_body)

    last_line_text_tobeadded = "<p>Kurumsal bilgiler içermektedir. Sadece ilgili ekipler ve 3. taraflar ile kontrollü olarak paylaşılmalıdır. \ Contains corporate information. It should only be shared in a controlled manner with the relevant teams and third parties.</p>"

    select_query_toplam = "SELECT * FROM ongoru_toplam_lastday where ID=2"
    cursor.execute(select_query_toplam)
    yday_ongoru_toplam = cursor.fetchone()
    diff_dict = {}
    diff_dict["fabia"] = toplam_asdict["fabia"] - yday_ongoru_toplam[1]
    diff_dict["scala"] = toplam_asdict["scala"] - yday_ongoru_toplam[2]
    diff_dict["octavia"] = toplam_asdict["octavia"] - yday_ongoru_toplam[3]
    diff_dict["superb"] = toplam_asdict["superb"] - yday_ongoru_toplam[4]
    diff_dict["kamiq"] = toplam_asdict["kamiq"] - yday_ongoru_toplam[5]
    diff_dict["karoq"] = toplam_asdict["karoq"] - yday_ongoru_toplam[6]
    diff_dict["kodiaq"] = toplam_asdict["kodiaq"] - yday_ongoru_toplam[7]
    diff_dict["toplam"] = diff_dict["fabia"] + diff_dict["scala"] + diff_dict["octavia"] + diff_dict["superb"] + diff_dict["kamiq"] + diff_dict["karoq"] + diff_dict["kodiaq"]

    from satis_ongoru_sabah.extension_email_html import extension_email_html
    extension_email_html = extension_email_html.format(str(diff_dict["fabia"]), 
                                                       str(diff_dict["scala"]), 
                                                       str(diff_dict["octavia"]), 
                                                       str(diff_dict["superb"]), 
                                                       str(diff_dict["kamiq"]),
                                                       str(diff_dict["karoq"]),
                                                       str(diff_dict["kodiaq"]),
                                                       str(diff_dict["toplam"])
                                                       )
    
    if OncekiGunYOK == False:
        email_body = email_body_start + email_body + txtfile_content + "\n<br>\n" + extension_email_html + "\n<br>\n" + last_line_text_tobeadded
    elif OncekiGunYOK == True:
        email_body = email_body_start + email_body + "\n<br>\n" + last_line_text_tobeadded

    email_subject = "ÖNGÖRÜ RAPORU " + today
    sender_email = "bilgilendirme@skoda.com.tr"
    sender_password = "Skoda.2023"
    mail_to = ["SkodaSatis@skoda.com.tr", "SkodaUrun@skoda.com.tr", "SkodaPazarlamaYonetimi@skoda.com.tr"]
    mail_cc = ["z.basar@skoda.com.tr","s.ekmen@skoda.com.tr"]
    mail_bcc = ["btyazilim@skoda.com.tr", "SkodaDashboard@skoda.com.tr", "l.yilmaz@skoda.com.tr"]
    #send_email_2(sender_email, sender_password, email_subject, email_body, "a.sarikaya@skoda.com.tr", None, None, None)
    try:
        send_email_2(sender_email, sender_password, email_subject, email_body, mail_to, mail_cc, mail_bcc, None)
    except:
        send_email(email_body, email_subject, ["c.colak@skoda.com.tr", "b.yurdasiper@skoda.com.tr"], ["d.ozkutuk@skoda.com.tr", "s.ozcelik@skoda.com.tr"], sender_email="bilgilendirme@skoda.com.tr")
        send_email(email_body, email_subject, ["SkodaSatis@skoda.com.tr", "SkodaUrun@skoda.com.tr"], sender_email="bilgilendirme@skoda.com.tr")
        send_email(email_body, email_subject, ["l.yilmaz@skoda.com.tr"], sender_email="bilgilendirme@skoda.com.tr")
        send_email(email_body, email_subject, ["d.ozkutuk@skoda.com.tr", "s.ozcelik@skoda.com.tr"])


    upd_query_toplam = f"""UPDATE ongoru_toplam_lastday SET 
        Fabia={toplam_asdict["fabia"]}, 
        Scala={toplam_asdict["scala"]}, 
        Octavia={toplam_asdict["octavia"]}, 
        Superb={toplam_asdict["superb"]}, 
        Kamiq={toplam_asdict["kamiq"]}, 
        Karoq={toplam_asdict["karoq"]}, 
        Kodiaq={toplam_asdict["kodiaq"]} 
        WHERE ID=2;"""
    cursor.execute(upd_query_toplam)
    conn.commit()
    cursor.close()
    conn.close()