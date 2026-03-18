from datetime import datetime, timedelta, date
import calendar
import pymysql
import base64
import time
import os
from ssh_sabahraporu.ssh_ssh_scrapers import TurkuazDataReader1, ParcaSatis_excel_downloader
from remove_empty_files import remove_empty_files
from format_with_period import format_with_period
from ssh_sabahraporu.ssh_email_html import email_html
from send_email import send_email, send_email_2
from ssh_sabahraporu.ssh_excel_readers import *
from ssh_sabahraporu.ssh_graphs import *
from ssh_sabahraporu.ssh_datefuncs import *
from ssh_sabahraporu.ssh_ora import *
from kill_chrome import kill_chrome
from ssh_sabahraporu.ssh_mssql import *
from config import *

def SSH_sabahraporu_complete(Turkuaz_username, Turkuaz_password, first_day_check):
    remove_empty_files(r"C:\Users\yuceappadmin\Downloads")

    today = date.today()
    start_day_last_year = datetime(today.year - 1, today.month, 1).strftime('%d.%m.%Y')
    start_day_thismonth_thisyear = datetime(today.year, today.month, 1).strftime('%d.%m.%Y')

    last_day_worked = last_work_day()

    formatted_last_day_worked = convert_date_Turkish_num(last_day_worked)

    first_space_index = formatted_last_day_worked.find(" ")

    second_space_index = formatted_last_day_worked.find(" ", first_space_index + 1)

    if first_space_index != -1 and second_space_index != -1:
        ay_turkce = formatted_last_day_worked[first_space_index + 1:second_space_index]
    if ay_turkce == "Şubat":
        gecen_ay = "Ocak"
    elif ay_turkce == "Mart":
        gecen_ay = "Şubat"
    elif ay_turkce == "Nisan":
        gecen_ay = "Mart"
    elif ay_turkce == "Mayıs":
        gecen_ay = "Nisan"
    elif ay_turkce == "Haziran":
        gecen_ay = "Mayıs"
    elif ay_turkce == "Temmuz":
        gecen_ay = "Haziran"
    elif ay_turkce == "Ağustos":
        gecen_ay = "Temmuz"
    elif ay_turkce == "Eylül":
        gecen_ay = "Ağustos" 
    elif ay_turkce == "Ekim":
        gecen_ay = "Eylül"
    elif ay_turkce == "Kasım":
        gecen_ay = "Ekim"
    elif ay_turkce == "Aralık":
        gecen_ay = "Kasım"
    sene = datetime.now().year
    month = datetime.now().month
    gecen_sene = sene - 1

    last_year_end_date, amount_ofdays_worked = Return_lastyear_enddate()
    howmanydaysleft_ = howmanydaysleft()
    year_of_last_day_worked = sene

    last_day_worked_PLUSONE = (datetime.strptime(last_day_worked, "%d.%m.%Y") + timedelta(days=1)).strftime("%d.%m.%Y")
    last_year_end_date_PLUSONE = (datetime.strptime(last_year_end_date, "%d.%m.%Y") + timedelta(days=1)).strftime("%d.%m.%Y")

    if first_day_check == True:
        month = month - 1
        start_day_last_year = datetime(today.year - 1, today.month - 1, 1).strftime('%d.%m.%Y')

        current_date = datetime.now()
        first_day_of_current_month = current_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        
        last_day_worked = last_work_day(first_day_check)

        start_day_thismonth_thisyear = last_day_of_previous_month.replace(day=1).strftime('%d.%m.%Y')

        last_year_end_date = last_day_of_previous_month.replace(year=last_day_of_previous_month.year - 1).strftime('%d.%m.%Y')
        start_day_last_year = (last_day_of_previous_month.replace(year=last_day_of_previous_month.year - 1).replace(day=1)).strftime('%d.%m.%Y')

        conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
        cursor = conn.cursor()
        query = f"SELECT DISTINCT * from `sshparca_data2` WHERE month={month} and year={sene};"

        amount_ofdays_worked = cursor.execute(query)
        howmanydaysleft_ = 0
    
    Parca_Satis_Hedef, İs_Emri_Hedef, Aksesuar_Satis_Hedef = Read_Hedefler_from_Excel('Copy of Tatil Günleri ve Hedef.xlsx', 'Hedef', month)

    Aksesuar_days_list_banko, Aksesuar_tl_list_banko = ssh_aksesuar_banko_fromOraDB(month, year_of_last_day_worked)
    Aksesuar_days_list_isemri, Aksesuar_tl_list_isemri = ssh_aksesuar_isemri_fromOraDB(month, year_of_last_day_worked)
    

    Aksesuar_tl_geliri_lastyear = ssh_aksesuar_total_fromGivenDates_fromOraDB(start_day_last_year, last_year_end_date)

    ssh_aksesuar_stok = ssh_aksesuar_stok_fromOraDB()
    ssh_aksesuar_stok_AsString = format_with_period(str(ssh_aksesuar_stok)) + " ₺"
    ssh_parca_stok = ssh_parca_stok_fromOraDB()
    ssh_parca_stok_AsString = format_with_period(str(ssh_parca_stok)) + " ₺"
    
    servis_giris_tumyil, randevulu_servis_giris_tumyil = ssh_servis_girisi_fromGivenDates_fromOraDB(f"01.01.{sene}", last_day_worked)
    last_day_worked_gecensene = last_day_worked.replace(str(sene), str(gecen_sene))
    servis_giris_tumyil_gecensene, randevulu_servis_giris_tumyil_gecensene = ssh_servis_girisi_fromGivenDates_fromOraDB(f"01.01.{gecen_sene}",last_day_worked_gecensene)

    
    perc_randevulu_servisgiris_tumyil = str(round((randevulu_servis_giris_tumyil/servis_giris_tumyil)*100)) + " %"
    perc_randevulu_servisgiris_gecensene = str(round((randevulu_servis_giris_tumyil_gecensene/servis_giris_tumyil_gecensene)*100)) + " %"
    
    buyil_divided_lastyear_servisgiris = str(round(((servis_giris_tumyil/servis_giris_tumyil_gecensene)*100),2)) + " %"
    buyil_divided_lastyear_randevuluservisgiris = str(round(((randevulu_servis_giris_tumyil/randevulu_servis_giris_tumyil_gecensene)*100),2)) + " %"

    servis_giris_tumyil = format_with_period(servis_giris_tumyil)
    randevulu_servis_giris_tumyil = format_with_period(randevulu_servis_giris_tumyil)
    servis_giris_tumyil_gecensene = format_with_period(servis_giris_tumyil_gecensene)
    randevulu_servis_giris_tumyil_gecensene = format_with_period(randevulu_servis_giris_tumyil_gecensene)

    tumyil_aksesuar_satisi = ssh_aksesuar_total_fromGivenDates_fromOraDB(f"01.01.{sene}", last_day_worked)
    tumyil_aksesuar_satisi_gecensene = ssh_aksesuar_total_fromGivenDates_fromOraDB(f"01.01.{gecen_sene}",last_day_worked_gecensene)
    tumyil_aksesuar_satisi_gecensene = str(round(((tumyil_aksesuar_satisi/tumyil_aksesuar_satisi_gecensene)*100),2)) + " %"
    tumyil_aksesuar_satisi = format_with_period(tumyil_aksesuar_satisi) + " ₺"
    #tumyil_aksesuar_satisi_gecensene = format_with_period(tumyil_aksesuar_satisi_gecensene) + " ₺"

    workOrder_count_kumule_busene, contact_count_kumule_busene = ssh_musteri_sikayet_fromGivenDates_fromOraDB(f"01.01.{sene}", last_day_worked, sene)
    workOrder_count_kumule_gecensene, contact_count_kumule_gecensene = ssh_musteri_sikayet_fromGivenDates_fromOraDB(f"01.01.{gecen_sene}",last_day_worked_gecensene, gecen_sene)
    

    musteri_sikayetOrani_kumule_busene = contact_count_kumule_busene #/ workOrder_count_kumule_busene
    musteri_sikyaterOrani_kumule_gecensene = str(round(((contact_count_kumule_busene/contact_count_kumule_gecensene)*100),2)) + " %" #/ workOrder_count_kumule_gecensene

    #musteri_sikayetOrani_kumule_busene = str(round(musteri_sikayetOrani_kumule_busene, 3)) + " %"
    #musteri_sikyaterOrani_kumule_gecensene = str(round(musteri_sikyaterOrani_kumule_gecensene, 3)) + " %"
    
    try:
        Aksesuar_lastdayworked_bankosatis = Aksesuar_tl_list_banko[-1]
    except:
        Aksesuar_lastdayworked_bankosatis=0
    try:
        Aksesuar_lastdayworked_isemri = Aksesuar_tl_list_isemri[-1]
    except:
        Aksesuar_lastdayworked_isemri=0
    Aksesuar_Satisi_lastdayworked = Aksesuar_lastdayworked_bankosatis + Aksesuar_lastdayworked_isemri
    Aksesuar_Satisi_Total = sum(Aksesuar_tl_list_banko) + sum(Aksesuar_tl_list_isemri)

    today = datetime.today().strftime("%d.%m.%Y")
    
    try:
        isEmri_kumule_gecensene, Garanti_kumule_gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenseneKumule.xls", 'Marka Bazlı Fatura Detayları')
    except:
        try:
            TurkuazDataReader1(Turkuaz_username, Turkuaz_password, f"01.01.{gecen_sene}", last_day_worked_gecensene, wait_time=480)
        except:
            kill_chrome()
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_GecenseneKumule.xls")
        isEmri_kumule_gecensene, Garanti_kumule_gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenseneKumule.xls", 'Marka Bazlı Fatura Detayları')
        time.sleep(1)
        kill_chrome()

    
    try:
        isEmri_kumule_busene, Garanti_kumule_busene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuseneKumule.xls", 'Marka Bazlı Fatura Detayları')
    except:
        try:
            TurkuazDataReader1(Turkuaz_username, Turkuaz_password, f"01.01.{sene}", last_day_worked, wait_time=580)
        except:
            kill_chrome()
            try:
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, f"01.01.{sene}", last_day_worked)
            except:
                kill_chrome()
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, f"01.01.{sene}", last_day_worked)
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_BuseneKumule.xls")
        isEmri_kumule_busene, Garanti_kumule_busene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuseneKumule.xls", 'Marka Bazlı Fatura Detayları')
        time.sleep(1)
        kill_chrome()
    


    try:
        İsemri_Adedi, ServisGiris = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls", 'Marka Bazlı Fatura Detayları')
        isEmri_Gun, Garanti_Gun = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls", 'Marka Bazlı Fatura Detayları')
    except:
        try:
            TurkuazDataReader1(Turkuaz_username, Turkuaz_password, last_day_worked, last_day_worked, wait_time=400)
        except:
            kill_chrome()
            try:
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, last_day_worked, last_day_worked, wait_time=180)
            except:
                kill_chrome()
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, last_day_worked, last_day_worked,  wait_time=280)
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_SonCalisilanGun_Raporu.xls")
        İsemri_Adedi, ServisGiris = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls", 'Marka Bazlı Fatura Detayları')
        isEmri_Gun, Garanti_Gun = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls", 'Marka Bazlı Fatura Detayları')
        time.sleep(1)
        kill_chrome()

    try:
        İsemri_Adedi_Gecensene, ServisGiris_Gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls", 'Marka Bazlı Fatura Detayları')
        isEmri_Gecensene, Garanti_Gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls", 'Marka Bazlı Fatura Detayları')
    except:
        try:
            TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_last_year, last_year_end_date, wait_time=250)
        except:
            kill_chrome()
            try:
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_last_year, last_year_end_date, wait_time=140)
            except:
                kill_chrome()
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_last_year, last_year_end_date, wait_time=160)
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_GecenSeneAylik_Rapor.xls")
        İsemri_Adedi_Gecensene, ServisGiris_Gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls", 'Marka Bazlı Fatura Detayları')
        isEmri_Gecensene, Garanti_Gecensene = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls", 'Marka Bazlı Fatura Detayları')
        time.sleep(1)
        kill_chrome()

    
    try:
        İsemri_Adedi_Ay, ServisGiris_Ay = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls", 'Marka Bazlı Fatura Detayları')
        isEmri_Ay, Garanti_Ay = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls", 'Marka Bazlı Fatura Detayları')
    except:
        try:
            TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_thismonth_thisyear, last_day_worked, wait_time=200)
        except:
            kill_chrome()
            try:
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_thismonth_thisyear, last_day_worked, wait_time=120)
            except:
                kill_chrome()
                TurkuazDataReader1(Turkuaz_username, Turkuaz_password, start_day_thismonth_thisyear, last_day_worked, wait_time=160)
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\SSH-IPI-DPU-008+İşçilik+ve+Parça+Gelirleri.xls", "Iscilik_Parca_BuAyKumule_Rapor.xls")
        İsemri_Adedi_Ay, ServisGiris_Ay = Read_SSH_Iscilik_ParcaGelirleri_Excel(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls", 'Marka Bazlı Fatura Detayları')
        isEmri_Ay, Garanti_Ay = Read_SSH_Iscilik_ParcaGelirleri_Excel2(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls", 'Marka Bazlı Fatura Detayları')
        time.sleep(1)
        kill_chrome()


    """
    start2 = datetime.strptime(last_day_worked, "%d.%m.%Y").strftime("%Y-%m-%d")
    end2 = (datetime.strptime(last_day_worked_PLUSONE, "%d.%m.%Y")).strftime("%Y-%m-%d")
    Banko_son_gun = round(return_banko_fromGivenDates(start2, end2))

    r"""
    try:
        Banko_son_gun = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_SonCalisilanGun_Raporu.xls", "BANKO")
    except:
        ParcaSatis_excel_downloader(Turkuaz_username, Turkuaz_password, last_day_worked, last_day_worked) # Downloads The excel starting date : lastwork_day, ending date: lastwork_day
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls", "ParcaSatis_SonCalisilanGun_Raporu.xls")
        Banko_son_gun = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_SonCalisilanGun_Raporu.xls", "BANKO")
        kill_chrome()
    #"""

    """
    start0 = datetime.strptime(start_day_last_year, "%d.%m.%Y").strftime("%Y-%m-%d")
    end0 = (datetime.strptime(last_year_end_date, "%d.%m.%Y")).strftime("%Y-%m-%d")
    Banko_kumule_gecensene = round(return_banko_fromGivenDates(start0, end0))

    r"""
    try:
        Banko_kumule_gecensene = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_GecenSeneAylik_Rapor.xls", "BANKO")
    except:
        ParcaSatis_excel_downloader(Turkuaz_username, Turkuaz_password, start_day_last_year, last_year_end_date) # Downloads The excel starting date : first day of this month last year, ending date: Chosen with func
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls", "ParcaSatis_GecenSeneAylik_Rapor.xls")
        Banko_kumule_gecensene = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_GecenSeneAylik_Rapor.xls", "BANKO")
        kill_chrome()

    """
    start1 = datetime.strptime(start_day_thismonth_thisyear, "%d.%m.%Y").strftime("%Y-%m-%d")
    end1 = (datetime.strptime(f"{last_day_worked}", "%d.%m.%Y")).strftime("%Y-%m-%d")
    Banko_kumule_busene = round(return_banko_fromGivenDates(start1, end1))

    r"""
    try:
        Banko_kumule_busene = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_BuAyKumule_Rapor.xls", "BANKO")
    except:
        ParcaSatis_excel_downloader(Turkuaz_username, Turkuaz_password, start_day_thismonth_thisyear, last_day_worked)
        RenameFile_in_a_path(r"C:\Users\yuceappadmin\Downloads\PRC-YSA-GBU-007+SSH+Parça+Satış.xls", "ParcaSatis_BuAyKumule_Rapor.xls")
        Banko_kumule_busene = Read_SSH_ParcaSatis_Excel(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_BuAyKumule_Rapor.xls", "BANKO")
        kill_chrome()
    #"""

    
    start_thisyear = datetime.strptime(f"01.01.{sene}", "%d.%m.%Y")
    start_thisyear_otherly_format = start_thisyear.strftime("%Y-%m-%d")
    enddate_thisyear_otherly_format = (datetime.strptime(f"{last_day_worked}", "%d.%m.%Y")).strftime("%Y-%m-%d")
    bu_yil_kumule_banko = round(return_banko_fromGivenDates(start_thisyear_otherly_format, enddate_thisyear_otherly_format))

    start_lastyear = datetime.strptime(f"01.01.{gecen_sene}", "%d.%m.%Y")
    start_lastyear_otherly_format = start_lastyear.strftime("%Y-%m-%d")
    enddate_lastyear_otherly_format = (datetime.strptime(f"{last_day_worked.replace(str(sene), str(gecen_sene))}", "%d.%m.%Y")).strftime("%Y-%m-%d")
    gecen_yil_kumule_banko = round(return_banko_fromGivenDates(start_lastyear_otherly_format, enddate_lastyear_otherly_format))


    bu_yil_div_gecensene_banko = str(round(((bu_yil_kumule_banko / gecen_yil_kumule_banko)*100),2)) + " %"
    bu_yil_kumule_banko_str = format_with_period(str(bu_yil_kumule_banko)) + " ₺"
    

    servisRandevuSayisi_SonGun = ssh_randevulu_servis_girisi_fromGivenDates_fromOraDB(last_day_worked, last_day_worked_PLUSONE)
    servisRandevuSayisi_BuAyKumule = ssh_randevulu_servis_girisi_fromGivenDates_fromOraDB(start_day_thismonth_thisyear, last_day_worked_PLUSONE)
    try:
        a = int(servisRandevuSayisi_SonGun)
    except:
        servisRandevuSayisi_SonGun = 0
    try:
        a = int(servisRandevuSayisi_BuAyKumule)
    except:
        servisRandevuSayisi_BuAyKumule = 0
    #servisRandevuSayisi_GecenSene = ssh_randevulu_servis_girisi_fromGivenDates_fromOraDB(start_day_last_year, last_year_end_date)


    Toplam_day = isEmri_Gun + Garanti_Gun + Banko_son_gun # + ServisGiris
    Toplam_gecensene = isEmri_Gecensene + Garanti_Gecensene + Banko_kumule_gecensene # + ServisGiris_Gecensene
    Toplam_kumule = isEmri_Ay + Garanti_Ay + Banko_kumule_busene # + ServisGiris_Ay
    orijinal_parca_satisi_gun = isEmri_Gun + Garanti_Gun + Banko_son_gun
    orijinal_parca_satisi_kumule = isEmri_Ay + Garanti_Ay + Banko_kumule_busene
    orijinal_parca_satisi_gecensene = isEmri_Gecensene + Garanti_Gecensene + Banko_kumule_gecensene

    bu_sene_kumule_toplam = round(isEmri_kumule_busene + Garanti_kumule_busene + Banko_kumule_busene)
    gecensene_kumule_toplam = round(isEmri_kumule_gecensene + Garanti_kumule_gecensene + Banko_kumule_gecensene)

    bu_sene_kumule_toplam_str = format_with_period(str(bu_sene_kumule_toplam))

    busene_div_gecensene_kumule_toplam = str(round(((bu_sene_kumule_toplam/gecensene_kumule_toplam)*100),2)) + " %"

    isEmri_kumule_busene_str = format_with_period(str(round(isEmri_kumule_busene)))
    Garanti_kumule_busene_str = format_with_period(str(round(Garanti_kumule_busene)))

    isEmri_kumule_gecensene_str = str(round(((isEmri_kumule_busene / isEmri_kumule_gecensene)*100),2)) + " %"
    Garanti_kumule_gecensene_str = str(round(((Garanti_kumule_busene / Garanti_kumule_gecensene)*100),2)) + " %"

    is_emri_graph = int(round(ServisGiris_Ay / İs_Emri_Hedef, 2) * 100)
    parca_graph = int(round(orijinal_parca_satisi_kumule / Parca_Satis_Hedef, 2) * 100)
    aksesuar_pasta_graph = int(round(Aksesuar_Satisi_Total / Aksesuar_Satis_Hedef, 2) * 100)

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    dateob = datetime.strptime(last_day_worked, "%d.%m.%Y")
    gun = dateob.strftime("%A")
    if gun == "Monday":
        gun = "Pzt"
    elif gun == "Tuesday":
        gun = "Sal"
    elif gun == "Wednesday":
        gun = "Çrş"
    elif gun == "Thursday":
        gun = "Prş"
    elif gun == "Friday":
        gun = "Cum"
    elif gun == "Saturday":
        gun = "Cmt"
    elif gun == "Sunday":
        gun = "Pzr"

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO sshparca_data (Tarih, Day, Month, Year, OrijinalParcaSatisAdet, gun) VALUES ('{}', {}, {}, {}, {},'{}');"
    Month_tobe_inserted = month
    query = query.format(last_day_worked, last_day_worked[:2], Month_tobe_inserted, last_day_worked[-4:], round(orijinal_parca_satisi_gun/1000), gun, last_day_worked)

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

    conn = pymysql.connect(host='localhost', user='root', db='ya_rpa')
    cursor = conn.cursor()
    query = "INSERT INTO sshparca_data2 (Tarih, day, month, year, servisgirisi, gun) VALUES ('{}', {}, {}, {}, {}, '{}');"
    Month_tobe_inserted = month
    query = query.format(last_day_worked, last_day_worked[:2], Month_tobe_inserted, last_day_worked[-4:], ServisGiris, gun)

    cursor.execute(query)
    conn.commit()

    if month != 1:
        query = "Select * from sshparca_data2 where month = '{}' AND year = '{}'".format(month - 1, sene)
        result = cursor.execute(query)
        datas = cursor.fetchall()

        servis_giris_list = []
        gun_list = []
        for data in datas:
            servis_giris_list.append(data[5])
            gun_list.append(data[6])

        toplam_giris = 0
        pzt_giris = 0
        pzt_count = 0
        sali_giris = 0
        sali_count = 0
        cars_giris = 0
        cars_count = 0
        pers_giris = 0
        pers_count = 0
        cuma_giris= 0
        cuma_count = 0
        ctesi_giris= 0
        ctesi_coumt = 0
        for i in range(len(servis_giris_list)):
            toplam_giris = toplam_giris + servis_giris_list[i]
            if "Pzt" == gun_list[i]:
                pzt_giris = pzt_giris +servis_giris_list[i]
                pzt_count += 1
            elif "Sal" == gun_list[i]:
                sali_giris = sali_giris + servis_giris_list[i]
                sali_count += 1
            elif "Çrş" == gun_list[i]:
                cars_giris = cars_giris + servis_giris_list[i]
                cars_count += 1
            elif "Prş" == gun_list[i]:
                pers_giris = pers_giris + servis_giris_list[i]
                pers_count += 1
            elif "Cum" == gun_list[i]:
                cuma_giris = cuma_giris + servis_giris_list[i]
                cuma_count += 1
            elif "Cmt" == gun_list[i]:
                ctesi_giris = ctesi_giris + servis_giris_list[i]
                ctesi_coumt += 1

        genel_ort = toplam_giris / len(servis_giris_list)
        genel_ort = round(genel_ort)

        pzt_ort = 1#round(pzt_giris/pzt_count)
        sal_ort = 1#round(sali_giris/sali_count)
        cars_ort = 1#round(cars_giris/cars_count)
        pers_ort = 1#round(pers_giris/pers_count)
        cuma_ort = 1#round(cuma_giris/cuma_count)
        ctesi_ort = 1#round(ctesi_giris/ctesi_coumt)
    
        last_month_servis_table_html = f"""
        <br>
        <table>
            <tr>
                <td style="background-color:#78FAAE; color:#0E3A2F; text-align:center;" colspan="7"><b>{gecen_ay} Ayı Servis Giriş Dağılımı (Ortalama)</b></td>
            </tr>
            <tr>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:160px; border:none;"><b>Çalışılan gün adedi: {len(servis_giris_list)}</b></td>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:135px; border:none;"><b>Ptesi ({pzt_count} gün)</b></td>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:135px; border:none;"><b>Salı ({sali_count} gün)</b></td>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:135px; border:none;"><b>Çarş ({cars_count} gün)</b></td>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:135px; border:none;"><b>Perş ({pers_count} gün)</b></td>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:135px; border:none;"><b>Cuma ({cuma_count} gün)</b></td>
                <td style="background-color:#0E3A2F; color:#78FAAE; text-align:center; width:135px; border:none;"><b>Ctesi ({ctesi_coumt} gün)</b></td>
            </tr>
            <tr>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{genel_ort}</b></td>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{pzt_ort}</b></td>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{sal_ort}</b></td>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{cars_ort}</b></td>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{pers_ort}</b></td>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{cuma_ort}</b></td>
                <td style="text-align:center; background-color:#F7B046; color:#0E3A2F; border:none;"><b>{ctesi_ort}</b></td>
            </tr>
        </table>
        <small>*Parantez içindeki değerler geçmiş aydaki gün adedini verir.</small>
        """
    else:
        last_month_servis_table_html = ""
    cursor.close()
    conn.close()

    plot_circlu_(is_emri_graph, 100-is_emri_graph, 'Servis Girişi (kümüle)', 'Hedef Kalan', '      İş Emri Aylık Hedef Gerçekleştirme      ', 'isemri_figure')
    plot_circlu_(parca_graph, 100-parca_graph, 'Parça Satışı (kümüle)', 'Hedef Kalan', '   Parça Satış Aylık Hedef Gerçekleştirme   ', 'parca_figure')
    plot_circlu_(aksesuar_pasta_graph, 100-aksesuar_pasta_graph, "Aksesuar Satışı (Kümüle)", "Hedef Kalan","Aksesuar Satış Aylık Hedef Gerçekleştirme", "aksesuar_pastaGrafik")
    plot_aksesuar_graph(month, year_of_last_day_worked)
    plot_columnu_(isEmri_Gecensene, isEmri_Ay, orijinal_parca_satisi_gecensene, orijinal_parca_satisi_kumule, Aksesuar_tl_geliri_lastyear, Aksesuar_Satisi_Total, 'bargraph', sene, gecen_sene)
    plot_line_('Parça Satışı (BİN ₺)', 'ParcaSatis_graph', first_day_check)
    plot_line_2('Servis Girişi', 'ServisGiris_graph', first_day_check)

    image_paths = []
    encoded_images = []

    isemri_figure = os.path.join(os.getcwd(), "isemri_figure.png")
    resize_image("isemri_figure.png", 300)
    parca_figure = os.path.join(os.getcwd(), "parca_figure.png")
    resize_image("parca_figure.png", 300)
    aksesuar_figure = os.path.join(os.getcwd(), "aksesuar_pastaGrafik.png")
    resize_image("aksesuar_pastaGrafik.png", 300)
    bargraph_figure = os.path.join(os.getcwd(), "bargraph.png")
    resize_image("bargraph.png", 500)
    parca_satis_line_figure = os.path.join(os.getcwd(), "ParcaSatis_graph.png")
    resize_image("ParcaSatis_graph.png", 957)
    aksesuar_satis_line_figure = os.path.join(os.getcwd(), "aksesuar_satis_grafik.png")
    resize_image("aksesuar_satis_grafik.png", 957)
    servis_giris_line_figure = os.path.join(os.getcwd(), "ServisGiris_graph.png")
    resize_image("ServisGiris_graph.png", 957)


    #image_paths.append(bargraph_figure)
    image_paths.append(isemri_figure)
    image_paths.append(parca_figure)
    image_paths.append(aksesuar_figure)
    image_paths.append(servis_giris_line_figure)
    image_paths.append(parca_satis_line_figure)
    image_paths.append(aksesuar_satis_line_figure)

    for image_path in image_paths:
            with open(image_path, "rb") as f:
                image_data = f.read()
                encoded_images.append(base64.b64encode(image_data).decode("utf-8"))

    Aksesuar_Satisi_lastdayworked = format_with_period(Aksesuar_Satisi_lastdayworked)
    Aksesuar_Satisi_Total = format_with_period(Aksesuar_Satisi_Total)

    try:
        servisOran_Gun = round((servisRandevuSayisi_SonGun / ServisGiris) * 100)
    except:
        servisOran_Gun = 0
    
    try:
        servisOran_Ay = round((servisRandevuSayisi_BuAyKumule / ServisGiris_Ay) * 100)
    except:
        servisOran_Ay = 0
    
    servisOran_Gun_str = str(servisOran_Gun) + " %"
    servisOran_Ay_str = str(servisOran_Ay) + " %"

    workOrder_count_lastdayworked, contact_count_lastdayworked = ssh_musteri_sikayet_fromGivenDates_fromOraDB(last_day_worked, last_day_worked_PLUSONE, sene)
    workOrder_count_kumule, contact_count_kumule = ssh_musteri_sikayet_fromGivenDates_fromOraDB(start_day_thismonth_thisyear, last_day_worked_PLUSONE, sene)

    musteri_sikayetOrani_sonGun_str = str(contact_count_lastdayworked) #/ workOrder_count_lastdayworked
    musteri_sikyaterOrani_kumule_str = str(contact_count_kumule) #/ workOrder_count_kumule


    content = email_html.format(formatted_last_day_worked, get_day_of_week(last_day_worked),
                                amount_ofdays_worked, howmanydaysleft_,
                                sene, gecen_sene,
                                format_with_period(ServisGiris), format_with_period(ServisGiris_Ay), format_with_period(İs_Emri_Hedef), servis_giris_tumyil, buyil_divided_lastyear_servisgiris,
                                format_with_period(servisRandevuSayisi_SonGun), servisOran_Gun_str, format_with_period(servisRandevuSayisi_BuAyKumule), servisOran_Ay_str, randevulu_servis_giris_tumyil, perc_randevulu_servisgiris_tumyil, buyil_divided_lastyear_randevuluservisgiris,
                                musteri_sikayetOrani_sonGun_str, musteri_sikyaterOrani_kumule_str, musteri_sikayetOrani_kumule_busene, musteri_sikyaterOrani_kumule_gecensene,
                                
                                format_with_period(isEmri_Gun) + " ₺", format_with_period(isEmri_Ay) + " ₺", isEmri_kumule_busene_str + " ₺", isEmri_kumule_gecensene_str, 
                                format_with_period(Garanti_Gun) + " ₺", format_with_period(Garanti_Ay) + " ₺", Garanti_kumule_busene_str + " ₺", Garanti_kumule_gecensene_str, 
                                format_with_period(Banko_son_gun) + " ₺", format_with_period(Banko_kumule_busene) + " ₺", bu_yil_kumule_banko_str, bu_yil_div_gecensene_banko,
                                format_with_period(orijinal_parca_satisi_gun) + " ₺", format_with_period(orijinal_parca_satisi_kumule) + " ₺", format_with_period(Parca_Satis_Hedef) + " ₺", bu_sene_kumule_toplam_str + " ₺", busene_div_gecensene_kumule_toplam,
                                
                                Aksesuar_Satisi_lastdayworked  + " ₺", Aksesuar_Satisi_Total + " ₺", format_with_period(Aksesuar_Satis_Hedef) + " ₺", tumyil_aksesuar_satisi, tumyil_aksesuar_satisi_gecensene,
                                
                                ssh_parca_stok_AsString, ssh_aksesuar_stok_AsString, 
                                encoded_images[0], encoded_images[1], encoded_images[2], 
                                encoded_images[3],
                                encoded_images[4],
                                encoded_images[5], 
                                #encoded_images[6],
                                )

    sender_email = 'sshraporu@skoda.com.tr'
    sender_password = 'Skoda.2023'
    subject = 'Günlük SSH Raporu'
    mail_to = ["SkodaSSH@skoda.com.tr", "SkodaSatis@skoda.com.tr", "SkodaFilo@skoda.com.tr"]
    mail_cc = ["z.basar@skoda.com.tr", "yuceautoicrakurulu@skoda.com.tr"]
    mail_bcc = ["btyazilim@skoda.com.tr", "SkodaDashboard@skoda.com.tr", "l.yilmaz@skoda.com.tr"]

    try:
        send_email_2(sender_email, sender_password, subject, content, mail_to, mail_cc, mail_bcc, None)
    except:
        #send_email(content, 'Günlük SSH Raporu', ["d.ozkutuk@skoda.com.tr"], cc_email=["afizeo@skoda.com.tr"], sender_email='sshraporu@skoda.com.tr')
        send_email(content, 'Günlük SSH Raporu', ["c.colak@skoda.com.tr", "b.yurdasiper@skoda.com.tr"], cc_email=["d.ozkutuk@skoda.com.tr", "s.ozcelik@skoda.com.tr"], sender_email='sshraporu@skoda.com.tr')
        send_email(content, 'Günlük SSH Raporu', ["SkodaDashboard@skoda.com.tr"], sender_email='sshraporu@skoda.com.tr')
        send_email(content, 'Günlük SSH Raporu', ["SkodaSSH@skoda.com.tr", "SkodaSatis@skoda.com.tr", "SkodaFilo@skoda.com.tr"], cc_email=["z.basar@skoda.com.tr", "yuceautoicrakurulu@skoda.com.tr"], sender_email='sshraporu@skoda.com.tr')
        send_email(content, 'Günlük SSH Raporu', ["l.yilmaz@skoda.com.tr"], sender_email='sshraporu@skoda.com.tr')


    os.remove("isemri_figure.png")
    os.remove("parca_figure.png")
    os.remove("bargraph.png")
    os.remove("ParcaSatis_graph.png")
    os.remove("aksesuar_pastaGrafik.png")
    os.remove("ServisGiris_graph.png")
    os.remove("aksesuar_satis_grafik.png")

    os.remove(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_SonCalisilanGun_Raporu.xls")
    os.remove(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenSeneAylik_Rapor.xls")
    os.remove(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuAyKumule_Rapor.xls")

    os.remove(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_BuseneKumule.xls")
    os.remove(r"C:\Users\yuceappadmin\Downloads\Iscilik_Parca_GecenseneKumule.xls")

    try:os.remove(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_SonCalisilanGun_Raporu.xls")
    except:pass
    try:os.remove(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_GecenSeneAylik_Rapor.xls")
    except:pass
    try:os.remove(r"C:\Users\yuceappadmin\Downloads\ParcaSatis_BuAyKumule_Rapor.xls")
    except:pass
