#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import warnings
import time
warnings.filterwarnings("ignore", category=DeprecationWarning)
from config import *


def email_reader():
    options = Options()
    options.headless = False
    driver = uc.Chrome(options=options)
    try:
        driver.get("https://mail.yuceauto.com.tr/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.yuceauto.com.tr%2fowa")
        time.sleep(3)
        driver.find_element('xpath', '//*[@id="username"]').send_keys(sabahraporu_email)
        driver.find_element('xpath', '//*[@id="password"]').send_keys(sabahraporu_email_Password)
        driver.find_element('xpath', '//*[@id="lgnDiv"]/div[9]/div').click()
        time.sleep(3)
        mail_element = driver.find_element('xpath', '//*[@id="_ariaId_27"]/div[2]')
        mail_text = mail_element.text
        element = mail_text.split('\n')

        if element[0] == 'turkuaz@dogusotomotiv.com.tr':
            if 'Skoda Satış Stok Raporu' in element[1]:
                mail_element.click()
                time.sleep(4)

        try:
            driver.find_element("xpath", '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div/div[3]/div[2]/div[2]/div[6]/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[8]/div/div[1]/div[2]/div/div/table/tbody/tr/td/div/div/div[2]/a').click()
            time.sleep(5)
        except:
            time.sleep(4)
            driver.find_element("xpath", '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div/div[3]/div[2]/div[2]/div[6]/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[8]/div/div[1]/div[2]/div/div/table/tbody/tr/td/div/div/div[2]/a').click()
    except:
        pass
    driver.quit()