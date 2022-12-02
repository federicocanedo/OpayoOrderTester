from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class Admin:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    def __init__(self, appSettings):
        #general settings
        self.generalSettings = appSettings.get('general')

        self.baseurl = self.generalSettings.get('baseUrl')

        #admin settings
        self.adminSettings = appSettings.get('admin')

        self.adminUrl = self.adminSettings.get('url')
        self.adminUser = self.adminSettings.get('user')
        self.adminPassword = self.adminSettings.get('password')

        self.sagePayUrl = f"{self.baseurl}{self.adminUrl}admin/system_config/edit/section/payment/"

        #removeNgrok
        self.driver.get(f"{self.baseurl}{self.adminUrl}")
        self.checkNgrok()

    def checkNgrok(self):
        time.sleep(3)
        if "NGROK" in self.driver.title:
            ngrokButton = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/main/div/div/section[1]/div/footer/button")))
            ngrokButton.click()

    def checkLogin(self):
        self.driver.get(f"{self.baseurl}{self.adminUrl}")
        if len(self.driver.find_elements("id", "login-form")) > 0:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(self.adminUser)
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'login'))).send_keys(self.adminPassword)
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'login-form'))).submit()
            time.sleep(3)

    def changePaymentAction(self, paymentAction, paymentMethod):
        print('Changing payment action')
        self.checkLogin()
        self.driver.get(self.sagePayUrl)
        time.sleep(3)
        self.driver.find_elements("xpath", f"//*[contains(@id, 'sagepaysuite_sagepaysuite{paymentMethod}-head')]")[0].click()

        self.driver.find_elements("xpath", f"//*[contains(@id, 'sagepaysuite{paymentMethod}_payment_action')]")[1].send_keys(paymentAction)
        self.saveConfig()

    def toggleDropin(self, dropStatus):
        self.checkLogin()
        self.driver.get(self.sagePayUrl)
        time.sleep(3)
        self.driver.find_elements("xpath", f"//*[contains(@id, 'sagepaysuite_sagepaysuitepi-head')]")[0].click()

        if dropStatus:
            print('Enabling dropin')
            self.driver.find_elements("xpath", f"//*[contains(@id, 'sagepaysuitepi_use_dropin')]")[1].send_keys('Yes')
        else:
            print('Disabling dropin')
            self.driver.find_elements("xpath", f"//*[contains(@id, 'sagepaysuitepi_use_dropin')]")[1].send_keys('No')
            time.sleep(3)
            try:
                dropInConfirmationButton = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="html-body"]/div[4]/aside[2]/div[2]/footer/button[2]')))
                dropInConfirmationButton.click()
            except:
                print('Dropin already disabled')

        self.saveConfig()

    def saveConfig(self):
        saveConfigButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'save')))
        saveConfigButton.click()
        time.sleep(3)
        self.clearCache()

    def clearCache(self):
        self.checkLogin()
        self.driver.get(f"{self.baseurl}{self.adminUrl}admin/cache/")
        refreshCacheButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'flush_magento')))
        refreshCacheButton.click()

