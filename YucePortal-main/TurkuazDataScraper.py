from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from datetime import datetime
import warnings
import time
warnings.filterwarnings("ignore", category=DeprecationWarning)
from config import *


def TurkuazDataReader(Turkuaz_username, Turkuaz_password):
    # Opens driver and directs to login page
    options = Options()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.get("https://turkuaz.dohas.com.tr/Admin/UILogin.aspx?ReturnUrl=%2f&__0186262C9018__=BQTQ4GMAmhTUYA%3d%3d__")
    time.sleep(1.5)

    try:
        # Login Process
        driver.find_element("xpath", '//*[@id="txtUserName"]').send_keys(Turkuaz_username)
        driver.find_element("xpath", '//*[@id="txtPassword"]').send_keys(Turkuaz_password)
        driver.find_element("xpath", '//*[@id="btnEnter"]').click()
        time.sleep(0.5)
        try:
            driver.find_element("xpath", '//*[@id="btnEnter"]').click()
        except:
            pass
        time.sleep(0.5)

        # Araç->Satış->Faturalanacak Araç İşlemleri->Distribütör Aylık Toplam Satışları
        driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=345&mPressed=1&Key=9&__01862656D11D__=BtXa4GMAAJoU1GA%3d__")
        driver.find_element("xpath", '//*[@id="_ctl0_TaskContent_rptTaskLink_lnkDistributorMonthlySales"]').click()
        time.sleep(1.5)

        # Rapordaki field'ları doldurma : day_start
        today = datetime.today().strftime("%d-%m-%Y")
        day_start = "01" + today[2:].replace("-", ".")
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys(day_start)

        # Rapordaki field'ları doldurma : day_end  ! IF DAY EQUALS 01, THINK OF A SOL ################################################
        today = datetime.today()
        try:
            yesterday = today.replace(day=today.day - 1)
        except:
            yesterday = today
        yesterday = yesterday.strftime("%d-%m-%Y").replace("-", ".")
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').clear()
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(yesterday)

        # Clicks to calculate button
        driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
        time.sleep(1.5)
        Diger_Satislar_value_ay = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[3]/td[14]').text

        # Yıllık data Turkuaz
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').clear()
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrStartingDate_TurkuazTextBox1"]').send_keys("01.01.2024")  ####################################
        driver.find_element("xpath", '//*[@id="_ctl0_ContentFields_ctrEndingDate_TurkuazTextBox1"]').send_keys(yesterday)
        driver.find_element("xpath", '//*[@id="_ctl0_ContentButtonsRight_btnList"]').click()
        time.sleep(3.5)
        Diger_Satislar_value_yil = driver.find_element("xpath", '//*[@id="_ctl0_DataGrid_grdQuota"]/tbody/tr[3]/td[14]').text

        driver.get("https://turkuaz.dohas.com.tr/UIGeneralTask.aspx?Menu1Selected=16&Menu2Selected=730&mPressed=1&Key=354&__01863A013AFE__=BaTj5WMA0e3nYA%3d%3d__")
        driver.find_element("xpath", '//*[@id="_ctl0_TaskContent_rptTaskLink_lnkVehicleConnectionRecordViewForMorningReport"]').click()
        
        fatura_table = driver.find_element("id", '_ctl0_DataGrid_grdDealerData')
        tr_tags_in_fatura_table = fatura_table.find_elements("tag name",'tr')
        
        Bugun_Perakende_str =  tr_tags_in_fatura_table[-3].text
        Bugun_Perakende = int(Bugun_Perakende_str.replace("Toplam(", "").replace(")", ""))

        Bugun_Olasilik_str = tr_tags_in_fatura_table[-2].text
        Bugun_Olasilik = int(Bugun_Olasilik_str.replace("Toplam(", "").replace(")", ""))

        Islem_Alti_str = tr_tags_in_fatura_table[-1].text
        Islem_Alti = int(Islem_Alti_str.replace("Toplam(", "").replace(")", ""))
    except:
        pass
    driver.quit()

    return Diger_Satislar_value_ay, Diger_Satislar_value_yil, Bugun_Perakende, Bugun_Olasilik, Islem_Alti
