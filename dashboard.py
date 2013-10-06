import re
from selenium import webdriver
from bs4 import BeautifulSoup

class ProductInfo():

    def __init__(self, name, price, numOwned, totalCPS):
        self.name = name
        self.price = price
        self.numOwned = numOwned
        self.totalCPS = totalCPS

    def cps(self):
        return self.totalCPS / self.numOwned

    def marginalBenefit(self):
        return self.cps() / self.price

    def __str__(self):
        return "{0} >> CPS: {1}, Owned: {2}, Price: {3}\nMarginal Benefit: {4}".format(self.name, self.cps(), self.numOwned, self.price, self.marginalBenefit())

driver = webdriver.Firefox()
driver.implicitly_wait(5)

def run():
    driver.get('http://orteil.dashnet.org/cookieclicker')

    html = driver.page_source
    #updateSave()
    insertGameStateCookie("MS4wMzc1fHwxMzgwMDczMzM0MjgxfDExMTExMXw3NTE5NTAwMTUwNDkuOTE1NDsxMjg0NTAxNjk4MjIxOS44MjY7MzU1MTk7NjI7MTU0MDcxMTI4MzcyMS43NTAyOzIzNjstMTstMTswOzA7MDswOzA7LTF8MTAwLDEwMyw4ODI1NzUyODczLDA7MTIyLDEyMyw1OTAxNTk5NDg4MSwwOzc1LDEwOSwxMzk2OTM4ODgsMDs4MCwxMDAsNTExOTM0NDc4LDA7NzAsMTAwLDE2MjA3ODM1MDksMDsxMDAsMTAwLDkxNDM1OTE3NzIsMDsxMDAsMTAwLDE5NDUyNDQ0Mjg4LDA7ODgsODgsMjQzMTI0ODk0MTI0LDA7NTAsNTAsOTY3MjI0MDU0ODQyLDA7MzUsMzUsMjY1NDk5NDUyMDMyNiwwO3w0NTAzNTk5NjI3MzQ1OTE5OzQ1MDMxODczMTA1MTAwNzk7MjI1Mjg5OTMyNTMxMTk4MzszOTQwNjUyNDkyNTMyMjIzOzU2MzUwMzQ3MzY2NjcwM3w0NTAzMDQ3ODU4MjkwNjg3OzIyNTIwOTYyOTQyNzA5NzU7MTk%3D%21END%21")

    # Refresh
    html = driver.page_source

    soup = BeautifulSoup(html)
    
    products = collectProductInfo(soup)
    for product in products:
        print(product)
    
def collectProductInfo(soup):
    products = []
    productDivs = soup.find_all('div', id=re.compile('product\d'))
    for product in productDivs:
        index = product['id'][-1:]
        title = product.find('div', class_='title').string
        price = int(re.sub(',', '', product.find('span', class_='price').string))
        numOwned = int(re.sub(',', '', product.find('div', class_='owned').string))
        
        info = soup.find('div', id='rowInfoContent{0}'.format(index))
        cps = ""
        try:
            match = re.search(r'(?<=producing) [^\s]*? (?=cookies)', str(info))
            cps = float(re.sub(',', '', match.group(0)))
        except:
            cps = 'error parsing CPS'
            
        pi = ProductInfo(title, price, numOwned, cps)
        products.append(pi)

    return products

def updateSave():
    try:
        elem = driver.find_element_by_id('prefsButton')
        elem.click()
        
        elem = driver.find_element_by_link_text('Save')
        elem.click()
    except:
        # FIX
        print("oops")

def insertGameStateCookie(cookie):
    try:
        elem = driver.find_element_by_id('prefsButton')
        elem.click()

        elem = driver.find_element_by_link_text('Import save')
        elem.click()

        alert = driver.switch_to_alert()
        alert.send_keys(cookie)
        alert.accept()

    except:
        # FIX - this can fail sometimes
        print("oops in insertCookie")

run()


