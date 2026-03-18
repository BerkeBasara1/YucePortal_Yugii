from excelreader import ExcelRead, ExcelRead2, ExcelRead3, format_with_period
from sabahraporu_ora import *
#from TurkuazDataScraper import TurkuazDataReader
#from percantage_calc import perc_calculator
#from email_reader import email_reader
from email_html import email_html
from send_email import send_email, send_email_2
from datetime import datetime
from config import *
import time
import pymysql
import os
from kill_chrome import kill_chrome


def SabahRaporuComplete(Ithalat_Perakende, Ithalat_Filo, ToptanFatura_perakende, ToptanFatura_filo, Euro_kur, SadeceBanaGonderilsin, sessionemail):
    #email_reader()
    #kill_chrome()
    #time.sleep(15)
    firsttable_data_astuple = return_sabahraporu_firsttable_astuple()
    secondtable_data_astuple = return_sabahraporu_secondtable_astuple()

    # This func below was the RPA to read the data from Turkuaz. No longer in use - Data is retrieved from the OraDB
    #Diger_Satislar_value_ay, Diger_Satislar_value_yil, Bugun_Perakende, Bugun_Olasilik, Islem_Alti = TurkuazDataReader(turkuazusername, turkuazpassword)
    #kill_chrome()

    Islem_Alti = return_sabahraporu_islemalti()
    Bugun_Olasilik = return_sabahraporu_bugunolasilik()
    Bugun_Perakende = return_sabahraporu_bugunperakende()

    DigerSatislar_filo_ay, DigerSatislar_filo_yil = return_sabahraporu_digersatislar_filo()
    DigerSatislar_perakende_ay, DigerSatislar_perakende_yil = return_sabahraporu_digersatislar_perakende()
    Diger_Satislar_value_ay = DigerSatislar_filo_ay + DigerSatislar_perakende_ay
    Diger_Satislar_value_yil = DigerSatislar_filo_yil + DigerSatislar_perakende_yil

    #Perakende_Ay, Toptan_Ay , Perakende_Yil, Toptan_Yil, Aylik_YS_Satis_F, YSval_YSF, Aylik_DS_Satis_F, Toptan_Aylik_eksi = ExcelRead(Skoda_Satis_Stok_Raporu, "Satış Stok Durumu", Diger_Satislar_value_ay)
    Filo_Bu_Ay_Perakende, Flo_Bu_Yil_Perakende = return_sabahraporu_filo_adetler()
    Perakende_Bu_Ay_Perakende, Perakende_Bu_Yil_Perakende = return_sabahraporu_perakende_adetler()

    Perakende_Ay = Filo_Bu_Ay_Perakende + Perakende_Bu_Ay_Perakende
    Perakende_Yil = Flo_Bu_Yil_Perakende + Perakende_Bu_Yil_Perakende

    Toptan_Bu_Ay_Filo, Toptan_Bu_Yil_Filo = return_sabahraporu_toptan_filo_adetler()
    Toptan_Bu_Ay_Perakende, Toptan_Bu_Yil_Perakende = return_sabahraporu_toptan_perakende_adetler()

    Toptan_Ay = Toptan_Bu_Ay_Filo + Toptan_Bu_Ay_Perakende + Diger_Satislar_value_ay
    Toptan_Yil = Toptan_Bu_Yil_Filo + Toptan_Bu_Yil_Perakende + Diger_Satislar_value_yil

    Aylik_YS_Satis_F = Filo_Bu_Ay_Perakende
    YSval_YSF = Perakende_Bu_Ay_Perakende
    Aylik_DS_Satis_F = Toptan_Bu_Ay_Filo
    Toptan_Aylik_eksi = Toptan_Bu_Ay_Perakende

    Fatura_Baglanti = format_with_period(str(YSval_YSF + Bugun_Perakende + Bugun_Olasilik + Islem_Alti))
    YSval_YSF = format_with_period(YSval_YSF)
    
    today = datetime.today().strftime("%d-%m-%Y").replace("-",".")

    Perakende_Ay = format_with_period(str(str(Perakende_Ay + Diger_Satislar_value_ay)))
    Perakende_Yil = format_with_period(str(Perakende_Yil + Diger_Satislar_value_yil))
    Toptan_Ay = format_with_period(Toptan_Ay)
    Toptan_Yil = format_with_period(Toptan_Yil)

    filo_tuples_aslist = []
    perakende_tuples_aslist = []
    for tuple in firsttable_data_astuple:
        if tuple[3] == "Filo":
            filo_tuples_aslist.append(tuple)
        elif tuple[3] == "Perakende":
            perakende_tuples_aslist.append(tuple)

    for ea_list in filo_tuples_aslist:
        if "YSStok" in ea_list:
            Filo_YSstok = ea_list[1]
            Filo_YSstok_isimli = ea_list[2]
        if "Stok" in ea_list:
            Filo_DSstok = ea_list[1]
            Filo_DSstok_isimli = ea_list[2]
        if "Fiktif" in ea_list:
            Filo_Fiktif = ea_list[1]
            Filo_Fiktif_isimli = ea_list[2]
        if "Yolda"in ea_list:
            Filo_Yolda = ea_list[1]
            Filo_Yolda_isimli = ea_list[2]
        if "Liman" in ea_list:
            Filo_Liman = ea_list[1]
            Filo_Liman_isimli = ea_list[2]
        if "Produced & Int" in ea_list:
            Filo_ProdInt = ea_list[1]
            Filo_ProdInt_isimli = ea_list[2]

    try:
        Filo_YSstok = Filo_YSstok
    except:
        Filo_YSstok = 0
    try:
        Filo_YSstok_isimli = Filo_YSstok_isimli
    except:
        Filo_YSstok_isimli = 0
    try:
        Filo_DSstok = Filo_DSstok
    except:
        Filo_DSstok = 0
    try:
        Filo_DSstok_isimli = Filo_DSstok_isimli
    except:
        Filo_DSstok_isimli = 0
    try:
        Filo_Fiktif = Filo_Fiktif
    except:
        Filo_Fiktif = 0
    try:
        Filo_Fiktif_isimli = Filo_Fiktif_isimli
    except:
        Filo_Fiktif_isimli = 0
    try:
        Filo_Yolda = Filo_Yolda
    except:
        Filo_Yolda = 0
    try:
        Filo_Yolda_isimli = Filo_Yolda_isimli
    except:
        Filo_Yolda_isimli = 0
    try:
        Filo_Liman = Filo_Liman
    except:
        Filo_Liman = 0
    try:
        Filo_Liman_isimli = Filo_Liman_isimli
    except:
        Filo_Liman_isimli = 0
    try:
        Filo_ProdInt = Filo_ProdInt
    except:
        Filo_ProdInt = 0
    try:
        Filo_ProdInt_isimli = Filo_ProdInt_isimli
    except:
        Filo_ProdInt_isimli = 0


    for ea_list in perakende_tuples_aslist:
        if "YSStok" in ea_list:
            Perakende_YSstok = ea_list[1]
            Perakende_YSstok_isimli = ea_list[2]
        if "Stok" in ea_list:
            Perakende_DSstok = ea_list[1]
            Perakende_DSstok_isimli = ea_list[2]
        if "Fiktif" in ea_list:
            Perakende_Fiktif = ea_list[1]
            Perakende_Fiktif_isimli = ea_list[2]
        if "Yolda"in ea_list:
            Perakende_Yolda = ea_list[1]
            Perakende_Yolda_isimli = ea_list[2]
        if "Liman" in ea_list:
            Perakende_Liman = ea_list[1]
            Perakende_Liman_isimli = ea_list[2]
        if "Produced & Int" in ea_list:
            Perakende_ProdInt = ea_list[1]
            Perakende_ProdInt_isimli = ea_list[2]

    try:
        Perakende_YSstok = Perakende_YSstok
    except:
        Perakende_YSstok = 0
    try:
        Perakende_YSstok_isimli = Perakende_YSstok_isimli
    except:
        Perakende_YSstok_isimli = 0
    try:
        Perakende_DSstok = Perakende_DSstok
    except:
        Perakende_DSstok = 0
    try:
        Perakende_DSstok_isimli = Perakende_DSstok_isimli
    except:
        Perakende_DSstok_isimli = 0
    try:
        Perakende_Fiktif = Perakende_Fiktif
    except:
        Perakende_Fiktif = 0
    try:
        Perakende_Fiktif_isimli = Perakende_Fiktif_isimli
    except:
        Perakende_Fiktif_isimli = 0
    try:
        Perakende_Yolda = Perakende_Yolda
    except:
        Perakende_Yolda = 0
    try:
        Perakende_Yolda_isimli = Perakende_Yolda_isimli
    except:
        Perakende_Yolda_isimli = 0
    try:
        Perakende_Liman = Perakende_Liman
    except:
        Perakende_Liman = 0
    try:
        Perakende_Liman_isimli = Perakende_Liman_isimli
    except:
        Perakende_Liman_isimli = 0
    try:
        Perakende_ProdInt = Perakende_ProdInt
    except:
        Perakende_ProdInt = 0
    try:
        Perakende_ProdInt_isimli = Perakende_ProdInt_isimli
    except:
        Perakende_ProdInt_isimli = 0

    try:
        perc_perakende_YSstok = "%" + str(round((Perakende_YSstok_isimli / Perakende_YSstok)*100))
    except:
        perc_perakende_YSstok = "-"
    try:
        perc_perakende_DSstok = "%" + str(round((Perakende_DSstok_isimli / Perakende_DSstok)*100))
    except:
        perc_perakende_DSstok = "-"
    try:
        perc_perakende_Fiktif = "%" + str(round((Perakende_Fiktif_isimli / Perakende_Fiktif)*100))
    except:
        perc_perakende_Fiktif = "-"
    try:
        perc_perakende_Yolda = "%" + str(round((Perakende_Yolda_isimli / Perakende_Yolda)*100))
    except:
        perc_perakende_Yolda = "-"
    try:
        perc_perakende_Liman = "%" + str(round((Perakende_Liman_isimli / Perakende_Liman)*100))
    except:
        perc_perakende_Liman = "-"
    try:
        perc_perakende_ProdInt = "%" + str(round((Perakende_ProdInt_isimli / Perakende_ProdInt)*100))
    except:
        perc_perakende_ProdInt = "-"

    try:
        perc_filo_YSstok = "%" + str(round((Filo_YSstok_isimli / Filo_YSstok)*100))
    except:
        perc_filo_YSstok = "-"
    try:
        perc_filo_DSstok = "%" + str(round((Filo_DSstok_isimli / Filo_DSstok)*100))
    except:
        perc_filo_DSstok = "-"
    try:
        perc_filo_Fiktif = "%" + str(round((Filo_Fiktif_isimli / Filo_Fiktif)*100))
    except:
        perc_filo_Fiktif = "-"
    try:
        perc_filo_Yolda = "%" + str(round((Filo_Yolda_isimli / Filo_Yolda)*100))
    except:
        perc_filo_Yolda = "-"
    try:
        perc_filo_Liman = "%" + str(round((Filo_Liman_isimli / Filo_Liman)*100))
    except:
        perc_filo_Liman = "-"
    try:
        perc_filo_ProdInt = "%" + str(round((Filo_ProdInt_isimli / Filo_ProdInt)*100))
    except:
        perc_filo_ProdInt = "-"

    toplam_YSstok = Filo_YSstok + Perakende_YSstok
    toplam_DSstok = Filo_DSstok + Perakende_DSstok
    toplam_Fiktif = Filo_Fiktif + Perakende_Fiktif
    toplam_Yolda = Filo_Yolda + Perakende_Yolda
    toplam_Liman = Filo_Liman + Perakende_Liman
    toplam_ProdInt = Filo_ProdInt + Perakende_ProdInt

    toplam_YSstok_isimli = Filo_YSstok_isimli + Perakende_YSstok_isimli
    toplam_DSstok_isimli = Filo_DSstok_isimli + Perakende_DSstok_isimli
    toplam_Fiktif_isimli = Filo_Fiktif_isimli + Perakende_Fiktif_isimli
    toplam_Yolda_isimli = Filo_Yolda_isimli + Perakende_Yolda_isimli
    toplam_Liman_isimli = Filo_Liman_isimli + Perakende_Liman_isimli
    toplam_ProdInt_isimli = Filo_ProdInt_isimli + Perakende_ProdInt_isimli

    try:
        perc_toplam_YSstok = "%" + str(round((toplam_YSstok_isimli / toplam_YSstok)*100))
    except:
        perc_toplam_YSstok = "-"
    try:
        perc_toplam_DSstok = "%" + str(round((toplam_DSstok_isimli / toplam_DSstok)*100))
    except:
        perc_toplam_DSstok = "-"
    try:
        perc_toplam_Fiktif = "%" + str(round((toplam_Fiktif_isimli / toplam_Fiktif)*100))
    except:
        perc_toplam_Fiktif = "-"
    try:
        perc_toplam_Yolda = "%" + str(round((toplam_Yolda_isimli / toplam_Yolda)*100))
    except:
        perc_toplam_Yolda = "-"
    try:
        perc_toplam_Liman = "%" + str(round((toplam_Liman_isimli / toplam_Liman)*100))
    except:
        perc_toplam_Liman = "-"
    try:
        perc_toplam_ProdInt = "%" + str(round((toplam_ProdInt_isimli / toplam_ProdInt)*100))
    except:
        perc_toplam_ProdInt = "-"


    Filo_YSstok = format_with_period(Filo_YSstok)
    Filo_DSstok = format_with_period(Filo_DSstok)
    Filo_Fiktif = format_with_period(Filo_Fiktif)
    Filo_Yolda = format_with_period(Filo_Yolda)
    Filo_Liman = format_with_period(Filo_Liman)
    Filo_ProdInt = format_with_period(Filo_ProdInt)

    Filo_YSstok_isimli = format_with_period(Filo_YSstok_isimli)
    Filo_DSstok_isimli = format_with_period(Filo_DSstok_isimli)
    Filo_Fiktif_isimli = format_with_period(Filo_Fiktif_isimli)
    Filo_Yolda_isimli = format_with_period(Filo_Yolda_isimli)
    Filo_Liman_isimli = format_with_period(Filo_Liman_isimli)
    Filo_ProdInt_isimli = format_with_period(Filo_ProdInt_isimli)

    Perakende_YSstok = format_with_period(Perakende_YSstok)
    Perakende_DSstok = format_with_period(Perakende_DSstok)
    Perakende_Fiktif = format_with_period(Perakende_Fiktif)
    Perakende_Yolda = format_with_period(Perakende_Yolda)
    Perakende_Liman = format_with_period(Perakende_Liman)
    Perakende_ProdInt = format_with_period(Perakende_ProdInt)

    Perakende_YSstok_isimli = format_with_period(Perakende_YSstok_isimli)
    Perakende_DSstok_isimli = format_with_period(Perakende_DSstok_isimli)
    Perakende_Fiktif_isimli = format_with_period(Perakende_Fiktif_isimli)
    Perakende_Yolda_isimli = format_with_period(Perakende_Yolda_isimli)
    Perakende_Liman_isimli = format_with_period(Perakende_Liman_isimli)
    Perakende_ProdInt_isimli = format_with_period(Perakende_ProdInt_isimli)

    toplam_YSstok = format_with_period(toplam_YSstok)
    toplam_DSstok = format_with_period(toplam_DSstok)
    toplam_Fiktif = format_with_period(toplam_Fiktif)
    toplam_Yolda = format_with_period(toplam_Yolda)
    toplam_Liman = format_with_period(toplam_Liman)
    toplam_ProdInt = format_with_period(toplam_ProdInt)

    toplam_YSstok_isimli = format_with_period(toplam_YSstok_isimli)
    toplam_DSstok_isimli = format_with_period(toplam_DSstok_isimli)
    toplam_Fiktif_isimli = format_with_period(toplam_Fiktif_isimli)
    toplam_Yolda_isimli = format_with_period(toplam_Yolda_isimli)
    toplam_Liman_isimli = format_with_period(toplam_Liman_isimli)
    toplam_ProdInt_isimli = format_with_period(toplam_ProdInt_isimli)
    
    filo_tuples_aslist2 = []
    perakende_tuples_aslist2 = []
    for ea_list2 in secondtable_data_astuple:
        if ea_list2[3] == "Filo":
            filo_tuples_aslist2.append(ea_list2)
        if ea_list2[3] == "Perakende":
            perakende_tuples_aslist2.append(ea_list2)
    

    for perakende_tops in perakende_tuples_aslist2:
        if "Fabia" in perakende_tops:
            perakende_fabia = perakende_tops[1]
            perakende_fabia_musterili = perakende_tops[2]
        if "Scala" in perakende_tops:
            perakende_scala = perakende_tops[1]
            perakende_scala_musterili = perakende_tops[2]
        if "Octavia" in perakende_tops:
            perakende_octavia = perakende_tops[1]
            perakende_octavia_musterili = perakende_tops[2]
        if "Octavia Combi" in perakende_tops:
            perakende_octaviaCombi = perakende_tops[1]
            perakende_octaviaCombi_musterili = perakende_tops[2]
        if "Yeni Octavia" in perakende_tops:
            perakende_Yenioctavia = perakende_tops[1]
            perakende_Yenioctavia_musterili = perakende_tops[2]
        if "Yeni Octavia Combi" in perakende_tops:
            perakende_YenioctaviaCombi = perakende_tops[1]
            perakende_YenioctaviaCombi_musterili = perakende_tops[2]
        if "Superb" in perakende_tops:
            perakende_Superb = perakende_tops[1]
            perakende_Superb_musterili = perakende_tops[2]
        if "Superb Combi" in perakende_tops:
            perakende_SuperbCombi = perakende_tops[1]
            perakende_SuperbCombi_musterili = perakende_tops[2]
        if "Superb Combi" in perakende_tops:
            perakende_SuperbCombi = perakende_tops[1]
            perakende_SuperbCombi_musterili = perakende_tops[2]
        if "Kamiq" in perakende_tops:
            perakende_Kamiq = perakende_tops[1]
            perakende_Kamiq_musterili = perakende_tops[2]
        if "Karoq" in perakende_tops:
            perakende_Karoq = perakende_tops[1]
            perakende_Karoq_musterili = perakende_tops[2]
        if "Kodiaq" in perakende_tops:
            perakende_Kodiaq = perakende_tops[1]
            perakende_Kodiaq_musterili = perakende_tops[2]
        if "Yeni Superb" in perakende_tops:
            perakende_yenisuperb = perakende_tops[1]
            perakende_yenisuperb_musterili = perakende_tops[2]
        if "Yeni Superb Combi" in perakende_tops:
            perakende_yenisuperbcombi = perakende_tops[1]
            perakende_yenisuperbcombi_musterili = perakende_tops[2]
        if "Yeni Kodiaq" in perakende_tops:
            perakende_yenikodiaq = perakende_tops[1]
            perakende_yenikodiaq_musterili = perakende_tops[2]
        
    try:
        perakende_fabia = perakende_fabia
    except:
        perakende_fabia = 0
        perakende_fabia_musterili = 0
    try:
        perakende_scala = perakende_scala
    except:
        perakende_scala = 0
        perakende_scala_musterili = 0
    try:
        perakende_octavia = perakende_octavia
    except:
        perakende_octavia = 0
        perakende_octavia_musterili = 0
    try:
        perakende_octaviaCombi = perakende_octaviaCombi
    except:
        perakende_octaviaCombi = 0
        perakende_octaviaCombi_musterili = 0
    try:
        perakende_Yenioctavia = perakende_Yenioctavia
    except:
        perakende_Yenioctavia = 0
        perakende_Yenioctavia_musterili = 0
    try:
        perakende_YenioctaviaCombi = perakende_YenioctaviaCombi
    except:
        perakende_YenioctaviaCombi = 0
        perakende_YenioctaviaCombi_musterili = 0
    try:
        perakende_Superb = perakende_Superb
    except:
        perakende_Superb = 0
        perakende_Superb_musterili = 0
    try:
        perakende_SuperbCombi = perakende_SuperbCombi
    except:
        perakende_SuperbCombi = 0
        perakende_SuperbCombi_musterili = 0
    try:
        perakende_Kamiq = perakende_Kamiq
    except:
        perakende_Kamiq = 0
        perakende_Kamiq_musterili = 0
    try:
        perakende_Karoq = perakende_Karoq
    except:
        perakende_Karoq = 0
        perakende_Karoq_musterili = 0
    try:
        perakende_Kodiaq = perakende_Kodiaq
    except:
        perakende_Kodiaq = 0
        perakende_Kodiaq_musterili = 0
    try:
        perakende_yenisuperb = perakende_yenisuperb
    except:
        perakende_yenisuperb = 0
        perakende_yenisuperb_musterili = 0
    try:
        perakende_yenisuperbcombi = perakende_yenisuperbcombi
    except:
        perakende_yenisuperbcombi = 0
        perakende_yenisuperbcombi_musterili = 0
    try:
        perakende_yenikodiaq = perakende_yenikodiaq
    except:
        perakende_yenikodiaq = 0
        perakende_yenikodiaq_musterili = 0
    
    perakende_octavia = perakende_octavia + perakende_octaviaCombi + perakende_Yenioctavia + perakende_YenioctaviaCombi
    perakende_Superb = perakende_Superb + perakende_SuperbCombi
    perakende_yenisuperb = perakende_yenisuperb + perakende_yenisuperbcombi


    perakende_octavia_musterili = perakende_octavia_musterili + perakende_octaviaCombi_musterili + perakende_Yenioctavia_musterili + perakende_YenioctaviaCombi_musterili
    perakende_Superb_musterili = perakende_Superb_musterili + perakende_SuperbCombi_musterili
    perakende_yenisuperb_musterili = perakende_yenisuperb_musterili + perakende_yenisuperbcombi_musterili

    try:
        perc_fabia_perakende = "%" + str(round((perakende_fabia_musterili / perakende_fabia) * 100))
    except:
        perc_fabia_perakende = "-"
    try:
        perc_scala_perakende = "%" + str(round((perakende_scala_musterili / perakende_scala) * 100))
    except:
        perc_scala_perakende = "-"
    try:
        perc_octavia_perakende = "%" + str(round((perakende_octavia_musterili / perakende_octavia) * 100))
    except:
        perc_octavia_perakende = "-"
    try:
        perc_yenisuperb_perakende = "%" + str(round((perakende_yenisuperb_musterili / perakende_yenisuperb) * 100))
    except:
        perc_yenisuperb_perakende = "-"
    try:
        perc_kamiq_perakende = "%" + str(round((perakende_Kamiq_musterili / perakende_Kamiq) * 100))
    except:
        perc_kamiq_perakende = "-"
    try:
        perc_karoq_perakende = "%" + str(round((perakende_Karoq_musterili / perakende_Karoq) * 100))
    except:
        perc_karoq_perakende = "-"
    try:
        perc_kodiaq_perakende = "%" + str(round((perakende_Kodiaq_musterili / perakende_Kodiaq) * 100))
    except:
        perc_kodiaq_perakende = "-"
    try:
        perc_yenikodiaq_perakende = "%" + str(round((perakende_yenikodiaq_musterili / perakende_yenikodiaq) * 100))
    except:
        perc_yenikodiaq_perakende = "-"

    Perakende_Toplam = perakende_fabia + perakende_scala + perakende_octavia + perakende_Superb + perakende_Kamiq + perakende_Karoq + perakende_Kodiaq + perakende_yenisuperb
    Perakende_Toplam_musterili = perakende_fabia_musterili + perakende_scala_musterili + perakende_octavia_musterili + perakende_Superb_musterili + perakende_Kamiq_musterili + perakende_Karoq_musterili + perakende_Kodiaq_musterili +perakende_yenisuperb_musterili
    try:
        perc_Perakende_Toplam = "%" + str(round((Perakende_Toplam_musterili / Perakende_Toplam) * 100))
    except:
        perc_Perakende_Toplam = "-"

    
    for filo_tops in filo_tuples_aslist2:
        if "Fabia" in filo_tops:
            filo_fabia = filo_tops[1]
            filo_fabia_musterili = filo_tops[2]
        if "Scala" in filo_tops:
            filo_scala = filo_tops[1]
            filo_scala_musterili = filo_tops[2]
        if "Octavia" in filo_tops:
            filo_octavia = filo_tops[1]
            filo_octavia_musterili = filo_tops[2]
        if "Octavia Combi" in filo_tops:
            filo_octaviaCombi = filo_tops[1]
            filo_octaviaCombi_musterili = filo_tops[2]
        if "Yeni Octavia" in filo_tops:
            filo_YeniOctavia = filo_tops[1]
            filo_YeniOctavia_musterili = filo_tops[2]
        if "Yeni Octavia Combi" in filo_tops:
            filo_YeniOctaviaCombi = filo_tops[1]
            filo_YeniOctaviaCombi_musterili = filo_tops[2]
        if "Superb" in filo_tops:
            filo_Superb = filo_tops[1]
            filo_Superb_musterili = filo_tops[2]
        if "Superb Combi" in filo_tops:
            filo_SuperbCombi = filo_tops[1]
            filo_SuperbCombi_musterili = filo_tops[2]
        if "Superb Combi" in filo_tops:
            filo_SuperbCombi = filo_tops[1]
            filo_SuperbCombi_musterili = filo_tops[2]
        if "Kamiq" in filo_tops:
            filo_Kamiq = filo_tops[1]
            filo_Kamiq_musterili = filo_tops[2]
        if "Karoq" in filo_tops:
            filo_Karoq = filo_tops[1]
            filo_Karoq_musterili = filo_tops[2]
        if "Kodiaq" in filo_tops:
            filo_Kodiaq = filo_tops[1]
            filo_Kodiaq_musterili = filo_tops[2]
        if "Yeni Superb" in filo_tops:
            filo_yenisuperb = filo_tops[1]
            filo_yenisuperb_musterili = filo_tops[2]
        if "Yeni Superb Combi" in filo_tops:
            filo_yenisuperbcombi = filo_tops[1]
            filo_yenisuperbcombi_musterili = filo_tops[2]
        if "Yeni Kodiaq" in filo_tops:
            filo_yeniKodiaq = filo_tops[1]
            filo_yeniKodiaq_musterili = filo_tops[2]
    

    try:
        filo_fabia = filo_fabia
    except:
        filo_fabia = 0
        filo_fabia_musterili = 0
    try:
        filo_scala = filo_scala
    except:
        filo_scala = 0
        filo_scala_musterili = 0
    try:
        filo_octavia = filo_octavia
    except:
        filo_octavia = 0
        filo_octavia_musterili = 0
    try:
        filo_octaviaCombi = filo_octaviaCombi
    except:
        filo_octaviaCombi = 0
        filo_octaviaCombi_musterili = 0
    try:
        filo_YeniOctavia = filo_YeniOctavia
    except:
        filo_YeniOctavia = 0
        filo_YeniOctavia_musterili = 0
    try:
        filo_YeniOctaviaCombi = filo_YeniOctaviaCombi
    except:
        filo_YeniOctaviaCombi = 0
        filo_YeniOctaviaCombi_musterili = 0
    try:
        filo_Superb = filo_Superb
    except:
        filo_Superb = 0
        filo_Superb_musterili = 0
    try:
        filo_SuperbCombi = filo_SuperbCombi
    except:
        filo_SuperbCombi = 0
        filo_SuperbCombi_musterili = 0
    try:
        filo_Kamiq = filo_Kamiq
    except:
        filo_Kamiq = 0
        filo_Kamiq_musterili = 0
    try:
        filo_Karoq = filo_Karoq
    except:
        filo_Karoq = 0
        filo_Karoq_musterili = 0
    try:
        filo_Kodiaq = filo_Kodiaq
    except:
        filo_Kodiaq = 0
        filo_Kodiaq_musterili = 0
    try:
        filo_yenisuperb = filo_yenisuperb
    except:
        filo_yenisuperb = 0
        filo_yenisuperb_musterili = 0
    try:
        filo_yenisuperbcombi = filo_yenisuperbcombi
    except:
        filo_yenisuperbcombi = 0
        filo_yenisuperbcombi_musterili = 0
    try:
        filo_yeniKodiaq = filo_yeniKodiaq
    except:
        filo_yeniKodiaq = 0
        filo_yeniKodiaq_musterili = 0
    
    filo_octavia = filo_octavia + filo_octaviaCombi + filo_YeniOctavia + filo_YeniOctaviaCombi
    filo_Superb = filo_Superb + filo_SuperbCombi
    filo_yenisuperb = filo_yenisuperb + filo_yenisuperbcombi

    filo_octavia_musterili = filo_octavia_musterili + filo_octaviaCombi_musterili + filo_YeniOctavia_musterili + filo_YeniOctaviaCombi_musterili
    filo_Superb_musterili = filo_Superb_musterili + filo_SuperbCombi_musterili
    filo_yenisuperb_musterili = filo_yenisuperb_musterili + filo_yenisuperbcombi_musterili

    try:
        perc_fabia_filo = "%" + str(round((filo_fabia_musterili / filo_fabia) * 100))
    except:
        perc_fabia_filo = "-"
    try:
        perc_scala_filo = "%" + str(round((filo_scala_musterili / filo_scala) * 100))
    except:
        perc_scala_filo = "-"
    try:
        perc_octavia_filo = "%" + str(round((filo_octavia_musterili / filo_octavia) * 100))
    except:
        perc_octavia_filo = "-"
    try:
        perc_kamiq_filo = "%" + str(round((filo_Kamiq_musterili / filo_Kamiq) * 100))
    except:
        perc_kamiq_filo = "-"
    try:
        perc_karoq_filo = "%" + str(round((filo_Karoq_musterili / filo_Karoq) * 100))
    except:
        perc_karoq_filo = "-"
    try:
        perc_kodiaq_filo = "%" + str(round((filo_Kodiaq_musterili / filo_Kodiaq) * 100))
    except:
        perc_kodiaq_filo = "-"
    try:
        perc_yenisuperb_filo = "%" + str(round((filo_yenisuperb_musterili / filo_yenisuperb) * 100))
    except:
        perc_yenisuperb_filo = "-"
    try:
        perc_yenikodiaq_filo = "%" + str(round((filo_yeniKodiaq_musterili / filo_yeniKodiaq) * 100))
    except:
        perc_yenikodiaq_filo = "-"

    filo_Toplam = filo_fabia + filo_scala + filo_octavia + filo_Superb + filo_Kamiq + filo_Karoq + filo_Kodiaq + filo_yenisuperb + filo_yeniKodiaq
    filo_Toplam_musterili = filo_fabia_musterili + filo_scala_musterili + filo_octavia_musterili + filo_Superb_musterili + filo_Kamiq_musterili + filo_Karoq_musterili + filo_Kodiaq_musterili + filo_yenisuperb_musterili + filo_yeniKodiaq_musterili
    try:
        perc_filo_Toplam = "%" + str(round((filo_Toplam_musterili / filo_Toplam) * 100))
    except:
        perc_filo_Toplam = "-"
    toplam_fabia = perakende_fabia + filo_fabia
    toplam_fabia_musterili = perakende_fabia_musterili + filo_fabia_musterili
    toplam_scala = perakende_scala + filo_scala
    toplam_scala_musterili = perakende_scala_musterili + filo_scala_musterili
    toplam_octavia = perakende_octavia + filo_octavia
    toplam_octavia_musterili = perakende_octavia_musterili + filo_octavia_musterili
    toplam_kamiq = perakende_Kamiq + filo_Kamiq
    toplam_kamiq_musterili = perakende_Kamiq_musterili + filo_Kamiq_musterili
    toplam_karoq = perakende_Karoq + filo_Karoq
    toplam_karoq_musterili = perakende_Karoq_musterili + filo_Karoq_musterili
    toplam_kodiaq = perakende_Kodiaq + filo_Kodiaq
    toplam_kodiaq_musterili = perakende_Kodiaq_musterili + filo_Kodiaq_musterili
    toplam_yenisuperb = perakende_yenisuperb + filo_yenisuperb
    toplam_yenisuperb_musterili = perakende_yenisuperb_musterili + filo_yenisuperb_musterili
    toplam_yenikodiaq = perakende_yenikodiaq + filo_yeniKodiaq
    toplam_yenikodiaq_musterili = perakende_yenikodiaq_musterili + filo_yeniKodiaq_musterili

    try:
        perc_fabia_toplam = "%" + str(round((toplam_fabia_musterili / toplam_fabia) * 100))
    except:
        perc_fabia_toplam = "-"
    try:
        perc_scala_toplam = "%" + str(round((toplam_scala_musterili / toplam_scala) * 100))
    except:
        perc_scala_toplam = "-"
    try:
        perc_octavia_toplam = "%" + str(round((toplam_octavia_musterili / toplam_octavia) * 100))
    except:
        perc_octavia_toplam = "-"
    try:
        perc_kamiq_toplam = "%" + str(round((toplam_kamiq_musterili / toplam_kamiq) * 100))
    except:
        perc_kamiq_toplam = "-"
    try:
        perc_karoq_toplam = "%" + str(round((toplam_karoq_musterili / toplam_karoq) * 100))
    except:
        perc_karoq_toplam = "-"
    if toplam_kodiaq != 0:
        perc_kodiaq_toplam = "%" + str(round((toplam_kodiaq_musterili / toplam_kodiaq) * 100))
    else:
        perc_kodiaq_toplam = "-"
    try:
        perc_yenisuperb_toplam = "%" + str(round((toplam_yenisuperb_musterili / toplam_yenisuperb) * 100))
    except:
        perc_yenisuperb_toplam = "-"
    try:
        perc_yenikodiaq_toplam = "%" + str(round((toplam_yenikodiaq_musterili / toplam_yenikodiaq) * 100))
    except:
        perc_yenikodiaq_toplam = "-"

    toplam_Toplam = toplam_fabia + toplam_scala + toplam_octavia + toplam_kamiq + toplam_karoq + toplam_kodiaq + toplam_yenisuperb + toplam_yenikodiaq
    toplam_Toplam_musterili = toplam_fabia_musterili + toplam_scala_musterili + toplam_octavia_musterili + toplam_kamiq_musterili + toplam_karoq_musterili + toplam_kodiaq_musterili + toplam_yenisuperb_musterili + toplam_yenikodiaq_musterili
    try:
        perc_Toplam_toplam = "%" + str(round((toplam_Toplam_musterili / toplam_Toplam) * 100))
    except:
        perc_Toplam_toplam = "-"

    if Euro_kur == None:
        Euro_kur = ""
    else:
        Euro_kur = '<p style="color:#349051"><b>İthalat Kuru: {}</b></p><br>'.format(Euro_kur)

    Ithalat_Toplam = int(Ithalat_Perakende) + int(Ithalat_Filo)
    Fatura_Toplam = int(ToptanFatura_perakende) + int(ToptanFatura_filo)

    Aylik_YS_Satis_F = Aylik_YS_Satis_F + Diger_Satislar_value_ay

    mail_index = email_html.format(today, str(Perakende_Ay), str(Perakende_Yil), str(Toptan_Ay), str(Toptan_Yil), Perakende_Ay, Aylik_YS_Satis_F,
        YSval_YSF, Toptan_Ay, format_with_period(Aylik_DS_Satis_F + DigerSatislar_filo_ay), format_with_period(Toptan_Aylik_eksi), Fatura_Baglanti, Ithalat_Toplam, Ithalat_Perakende, Ithalat_Filo, Fatura_Toplam, ToptanFatura_perakende, ToptanFatura_filo, Euro_kur,
        Perakende_YSstok, Perakende_YSstok_isimli, perc_perakende_YSstok, Filo_YSstok, Filo_YSstok_isimli, perc_filo_YSstok, toplam_YSstok, toplam_YSstok_isimli, perc_toplam_YSstok,
        Perakende_DSstok, Perakende_DSstok_isimli, perc_perakende_DSstok, Filo_DSstok, Filo_DSstok_isimli, perc_filo_DSstok, toplam_DSstok, toplam_DSstok_isimli, perc_toplam_DSstok,
        Perakende_Fiktif, Perakende_Fiktif_isimli, perc_perakende_Fiktif, Filo_Fiktif, Filo_Fiktif_isimli, perc_filo_Fiktif, toplam_Fiktif, toplam_Fiktif_isimli, perc_toplam_Fiktif,
        Perakende_Yolda, Perakende_Yolda_isimli, perc_perakende_Yolda, Filo_Yolda, Filo_Yolda_isimli, perc_filo_Yolda, toplam_Yolda, toplam_Yolda_isimli, perc_toplam_Yolda,
        Perakende_Liman, Perakende_Liman_isimli, perc_perakende_Liman, Filo_Liman, Filo_Liman_isimli, perc_filo_Liman, toplam_Liman,toplam_Liman_isimli, perc_toplam_Liman,
        Perakende_ProdInt, Perakende_ProdInt_isimli, perc_perakende_ProdInt, Filo_ProdInt, Filo_ProdInt_isimli, perc_filo_ProdInt, toplam_ProdInt, toplam_ProdInt_isimli, perc_toplam_ProdInt,
        format_with_period(perakende_fabia), format_with_period(perakende_fabia_musterili), perc_fabia_perakende, format_with_period(filo_fabia), format_with_period(filo_fabia_musterili), perc_fabia_filo, format_with_period(toplam_fabia), format_with_period(toplam_fabia_musterili), perc_fabia_toplam,
        format_with_period(perakende_scala), format_with_period(perakende_scala_musterili), perc_scala_perakende, format_with_period(filo_scala), format_with_period(filo_scala_musterili), perc_scala_filo, format_with_period(toplam_scala), format_with_period(toplam_scala_musterili), perc_scala_toplam,
        format_with_period(perakende_octavia), format_with_period(perakende_octavia_musterili), perc_octavia_perakende, format_with_period(filo_octavia), format_with_period(filo_octavia_musterili), perc_octavia_filo, format_with_period(toplam_octavia), format_with_period(toplam_octavia_musterili), perc_octavia_toplam,
        format_with_period(perakende_yenisuperb), format_with_period(perakende_yenisuperb_musterili), perc_yenisuperb_perakende, format_with_period(filo_yenisuperb), format_with_period(filo_yenisuperb_musterili), perc_yenisuperb_filo, format_with_period(toplam_yenisuperb), format_with_period(toplam_yenisuperb_musterili), perc_yenisuperb_toplam,
        format_with_period(perakende_Kamiq), format_with_period(perakende_Kamiq_musterili), perc_kamiq_perakende, format_with_period(filo_Kamiq), format_with_period(filo_Kamiq_musterili), perc_kamiq_filo, format_with_period(toplam_kamiq), format_with_period(toplam_kamiq_musterili), perc_kamiq_toplam,
        format_with_period(perakende_Karoq), format_with_period(perakende_Karoq_musterili), perc_karoq_perakende, format_with_period(filo_Karoq), format_with_period(filo_Karoq_musterili), perc_karoq_filo, format_with_period(toplam_karoq), format_with_period(toplam_karoq_musterili), perc_karoq_toplam,
        #format_with_period(perakende_Kodiaq), format_with_period(perakende_Kodiaq_musterili), perc_kodiaq_perakende, format_with_period(filo_Kodiaq), format_with_period(filo_Kodiaq_musterili), perc_kodiaq_filo, format_with_period(toplam_kodiaq), format_with_period(toplam_kodiaq_musterili), perc_kodiaq_toplam,
        format_with_period(perakende_yenikodiaq), format_with_period(perakende_yenikodiaq_musterili), perc_yenikodiaq_perakende, format_with_period(filo_yeniKodiaq), format_with_period(filo_yeniKodiaq_musterili), perc_yenikodiaq_filo, format_with_period(toplam_yenikodiaq), format_with_period(toplam_yenikodiaq_musterili), perc_yenikodiaq_toplam,
        format_with_period(str(Perakende_Toplam)),format_with_period(str(Perakende_Toplam_musterili)), perc_Perakende_Toplam,format_with_period(str(filo_Toplam)),format_with_period(str(filo_Toplam_musterili)), perc_filo_Toplam, format_with_period(str(toplam_Toplam)),format_with_period(str(toplam_Toplam_musterili)),format_with_period(str(perc_Toplam_toplam))
        ).replace("em.pty", "0")

    #os.remove(Skoda_Satis_Stok_Raporu)

    mail_header = "SABAH RAPORU {}".format(today)
    mail_to = ["SkodaSatis@skoda.com.tr", "SkodaFilo@skoda.com.tr", "SkodaUrun@skoda.com.tr" ,"SkodaSSH@skoda.com.tr"]
    mail_cc = ["z.basar@skoda.com.tr", "yuceautoicrakurulu@skoda.com.tr"]
    mail_bcc = ["btyazilim@skoda.com.tr", "SkodaDashboard@skoda.com.tr", "l.yilmaz@skoda.com.tr"]

    if SadeceBanaGonderilsin == True:
        try:
            send_email_2(sabahraporu_email, sabahraporu_email_Password, mail_header, mail_index, sessionemail, None, None, None)
        except:
            send_email(mail_index, mail_header, sessionemail, cc_email=[sessionemail])
    else:
        try:
            send_email_2(sabahraporu_email, sabahraporu_email_Password, mail_header, mail_index, mail_to, mail_cc, mail_bcc, None)
        except:
            send_email(mail_index, mail_header, ["SkodaSatis@skoda.com.tr", "SkodaFilo@skoda.com.tr", "SkodaUrun@skoda.com.tr" ,"SkodaSSH@skoda.com.tr"], cc_email=["z.basar@skoda.com.tr", "yuceautoicrakurulu@skoda.com.tr"])
            send_email(mail_index, mail_header, ["c.colak@skoda.com.tr", "b.yurdasiper@skoda.com.tr"], cc_email=["dogao@skoda.com.tr", "s.ozcelik@skoda.com.tr", "b.basara@skoda.com.tr"])
            send_email(mail_index, mail_header, ["SkodaDashboard@skoda.com.tr"])
            send_email(mail_index, mail_header, ["l.yilmaz@skoda.com.tr"])
        
    

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO sabahraporu (ithalat, fatura, tarih) VALUES (%s, %s, %s)"
    values = (Ithalat_Toplam, Fatura_Toplam, today)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

