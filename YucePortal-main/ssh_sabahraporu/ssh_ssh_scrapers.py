#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import undetected_chromedriver as uc
from ssh_sabahraporu.ssh_excel_readers import *
import time
import subprocess
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from config import *
from kill_chrome import kill_chrome

def TurkuazDataReader1(id, pw, excel_startdate, excel_enddate, wait_time=None):
    # Opens driver and directs to login page
    options = Options()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get("https://turkuaz.dohas.com.tr/Admin/UILogin.aspx?ReturnUrl=%2f&__0186262C9018__=BQTQ4GMAmhTUYA%3d%3d__")
    time.sleep(1.5)
    try:
        # Login Process
        driver.find_element("xpath", '//*[@id="txtUserName"]').send_keys(id)
        driver.find_element("xpath", '//*[@id="txtPassword"]').send_keys(pw)
        driver.find_element("xpath", '//*[@id="btnEnter"]').click()
        time.sleep(0.5)
        try:
            driver.find_element("xpath", '//*[@id="btnEnter"]').click()
        except:
            pass
        time.sleep(0.8)

        driver.get("https://turkuaz.dohas.com.tr/General/Report/UIReportFrame.aspx?Menu1Selected=109&Menu2Selected=892&mPressed=1&Key=0&__018962B652BB__=CBfrtGQAAAAAmhTUYA%3d%3d__&t=1689578263241T")
        time.sleep(0.8)

        # Here it uses the popping up iframe part
        iframe1 = driver.find_element("id", "_ctl0_ContentFields_myFrame")
        driver.switch_to.frame(iframe1)

        iframe2 = driver.find_element("id", 'myopendoc')
        driver.switch_to.frame(iframe2)
        driver.find_element("xpath", '//*[@id="content"]/a[4]').click()
        time.sleep(1)
        driver.find_element("xpath", '//*[@id="content_sub"]/a[4]').click()
        time.sleep(20)
        driver.find_element("xpath", '//*[@id="documentListTable"]/tr[1]/td[2]/a').click()
        time.sleep(25)

        driver.switch_to.window(driver.window_handles[1])

        iframe_of_popup = driver.find_element("id", 'reportRunWindowFrame')
        driver.switch_to.frame(iframe_of_popup)
        time.sleep(15)

        # Fills the Start/End dates
        try:
            driver.find_element("xpath", '//*[@id="PROMPT0"]').send_keys(Keys.DELETE)
        except:
            time.sleep(20)
            try:
                driver.find_element("xpath", '//*[@id="PROMPT0"]').send_keys(Keys.DELETE)
            except:
                time.sleep(30)

        for i in range(20):
            driver.find_element("xpath", '//*[@id="PROMPT0"]').send_keys(Keys.DELETE)
        driver.find_element("xpath", '//*[@id="PROMPT0"]').send_keys(excel_startdate)

        for i in range(20):
            driver.find_element("xpath", '//*[@id="PROMPT1"]').send_keys(Keys.DELETE)
        driver.find_element("xpath", '//*[@id="PROMPT1"]').send_keys(excel_enddate)
        time.sleep(0.1)

        # Fills "Marka" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[3]/div/div/span/span[1]/span/ul/li/input').send_keys("Skoda")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[3]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[3]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        # Fills "Pdi" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[4]/div/div/span/span[1]/span/ul/li/input').send_keys("YOK")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[4]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[4]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)


        # Fills "Stok İş Emirleri Gelsin mi?" Selectbox
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[5]/div/div/span/span[1]/span').click()
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys("Evet")
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(Keys.ENTER)


        # Fills "Yetkili Satıcı :" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[6]/div/div/span/span[1]/span/ul/li/input').send_keys("TÜMÜ")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[6]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[6]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        driver.find_element("xpath", '//*[@id="titleDiv"]/button[4]').click()
        if wait_time == None:
            time.sleep(300)
        else:
            time.sleep(wait_time)
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
    kill_chrome()
    time.sleep(4)

def ParcaSatis_excel_downloader(id, pw, start_date, end_date):
    # Opens driver and directs to login page
    options = Options()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get("https://turkuaz.dohas.com.tr/Admin/UILogin.aspx?ReturnUrl=%2f&__0186262C9018__=BQTQ4GMAmhTUYA%3d%3d__")
    time.sleep(1.5)

    try:

        # Login Process
        driver.find_element("xpath", '//*[@id="txtUserName"]').send_keys(id)
        driver.find_element("xpath", '//*[@id="txtPassword"]').send_keys(pw)
        driver.find_element("xpath", '//*[@id="btnEnter"]').click()
        time.sleep(0.5)
        try:
            driver.find_element("xpath", '//*[@id="btnEnter"]').click()
        except:
            pass
        time.sleep(0.8)

        driver.get("https://turkuaz.dohas.com.tr/General/Report/UIReportFrame.aspx?Menu1Selected=43&Menu2Selected=891&mPressed=1&Key=0&__01870EB23C86__=B5ZWHGQAAADkPD0u__")
        time.sleep(1.5)

        # Here it uses the popping up iframe part
        iframe1 = driver.find_element("name", 'window')
        driver.switch_to.frame(iframe1)

        iframe2 = driver.find_element("id", "myopendoc")
        driver.switch_to.frame(iframe2)

        driver.find_element("xpath", '//*[@id="content"]/a[4]').click()
        time.sleep(1)
        driver.find_element("xpath", '//*[@id="content_sub"]/a[3]').click()
        time.sleep(10)

        a_tags = driver.find_elements("tag name", 'a')

        for a_tag in a_tags:
            if a_tag.text == 'PRC-YSA-GBU-007 SSH Parça Satış':
                a_tag.click()
        time.sleep(10)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)

        iframe_of_popup = driver.find_element("id", 'reportRunWindowFrame')
        driver.switch_to.frame(iframe_of_popup)
        time.sleep(75)

        # Fills the Start/End dates
        for i in range(20):
            driver.find_element("xpath", '//*[@id="PROMPT0"]').send_keys(Keys.DELETE)
        driver.find_element("xpath", '//*[@id="PROMPT0"]').send_keys(start_date)

        for i in range(20):
            driver.find_element("xpath", '//*[@id="PROMPT1"]').send_keys(Keys.DELETE)
        driver.find_element("xpath", '//*[@id="PROMPT1"]').send_keys(end_date)
        time.sleep(0.1)

        # Fills "Detay gerekli mi?" Selectbox
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[3]/div/div/span/span[1]/span').click()
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys("Evet")
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(Keys.ENTER)

        # Fills "Hangisi Gerekli?" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[4]/div/div/span/span[1]/span/ul/li/input').send_keys("TÜMÜ")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[4]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[4]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        # Fills "Hangisi Gerekli?" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[5]/div/div/span/span[1]/span/ul/li/input').send_keys("Skoda")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[5]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[5]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        # Fills "Parça Kodu" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[6]/div/div/div/input').send_keys("*TÜMÜ")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[6]/div/div/div/input').send_keys(Keys.ENTER)

        # Fills "Sipariş Parça Tipi:" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[7]/div/div/span/span[1]/span/ul/li/input').send_keys("TÜMÜ")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[7]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[7]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        # Fills "Yetkili Satıcı:" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[8]/div/div/span/span[1]/span/ul/li/input').send_keys("TÜMÜ")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[8]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[8]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        # Fills "İşemri / Banko" Selectbox
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[9]/div/div/span/span[1]/span').click()
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys("Banko")
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(Keys.ENTER)

        # Fills "Ortak Parça Grubu:" Input
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[10]/div/div/span/span[1]/span/ul/li/input').send_keys("TÜMÜ")
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[10]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ARROW_DOWN)
        driver.find_element("xpath", '//*[@id="promptsContainerDivId"]/div[10]/div/div/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

        time.sleep(0.2)

        driver.find_element("xpath", '//*[@id="titleDiv"]/button[4]').click()
        time.sleep(860)

        driver.quit()
    except:
        driver.quit()
        
    time.sleep(3)
    kill_chrome()
    time.sleep(3)