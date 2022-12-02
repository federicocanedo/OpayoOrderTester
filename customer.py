from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class Customer:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    def __init__(self, appSettings):
        #general settings
        self.generalSettings = appSettings.get('general')

        self.baseUrl = self.generalSettings.get('baseUrl')

        #customer settings
        self.customerSettings = appSettings.get('customer')

        self.customerProduct = self.customerSettings.get('productName')
    
        #checkout shipping
        self.checkoutShipping = self.customerSettings.get('checkoutShipping')

        #checkout payment
        self.checkoutPayment = self.customerSettings.get('checkoutPayment')

        #removeNgrok
        self.driver.get(self.baseUrl)
        self.checkNgrok()


    def checkNgrok(self):
        time.sleep(3)
        if "NGROK" in self.driver.title:
            ngrokButton = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/main/div/div/section[1]/div/footer/button")))
            ngrokButton.click()

    def addProductToCart(self):
        print(f'Adding {self.customerProduct} to cart')
        self.driver.get(f"{self.baseUrl}{self.customerProduct}.html")
        addToCartButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'product-addtocart-button')))
        addToCartButton.click()
        time.sleep(2)

    def checkoutFillShippingInfo(self):
        print('Filling shipping info')
        self.driver.get(f"{self.baseUrl}checkout")

        for field in self.checkoutShipping:
            if "id" in self.checkoutShipping[field]:
                shippingInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, self.checkoutShipping[field].get('id'))))
            if "xpath" in self.checkoutShipping[field]:
                shippingInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.checkoutShipping[field].get('xpath'))))

            shippingInput.send_keys(self.checkoutShipping[field]['value'])

        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'co-shipping-method-form'))).submit()

    def selectPaymentMethod(self, paymentMethod):
        print(f'Selecting payment method {paymentMethod}')
        time.sleep(4)
        paymentMethodCheckbox = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, f'sagepaysuite{paymentMethod}')))
        paymentMethodCheckbox.click()