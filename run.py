from customer import Customer
from admin import Admin
import json

def loadAppSettings():
    #Loads magentoversions.json
    with open("config.json", "r") as f:
        settings = json.load(f)
    return settings

def loadTestCases():
    #Loads magentoversions.json
    with open("testcases.json", "r") as f:
        testCases = json.load(f)
    return testCases['cases']

appSettings = loadAppSettings()
testCases = loadTestCases()

customer = Customer(appSettings)
admin = Admin(appSettings)

for case in testCases:
    print('------------------------------------------------------------------------------------------------')
    print(f"Payment method: {case.get('paymentMethod')}")
    print(f"Payment action: {case.get('paymentAction')}\n")
    admin.changePaymentAction(case.get('paymentAction'), case.get('paymentMethod'))

    if 'dropin' in case:
        admin.toggleDropin(case.get('dropin'))

    customer.addProductToCart()
    customer.checkoutFillShippingInfo()
    customer.selectPaymentMethod(case.get('paymentMethod'))

    input("\nFinish payment and press Enter to continue...")