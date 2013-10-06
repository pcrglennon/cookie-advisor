from datetime import datetime
import re
from selenium import webdriver
from bs4 import BeautifulSoup

from product_info import ProductInfo

def run():
    global driver
    global filename
    
    seed = input('Enter initial game state, or filename (w/ txt extension): ')
    
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    driver.get('http://orteil.dashnet.org/cookieclicker')

    if '.txt' in seed:
        filename = seed
        insertGameStateCookie()
    else:
        filename = 'saves.txt'
        insertGameStateCookie(seed)

    # Refresh
    html = driver.page_source
    soup = BeautifulSoup(html)
    
    products = collectProductInfo(soup)
    for product in products:
        print(product)

    prependNewSave()
    
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

def updateSave(close=True):
    try:
        openMenu()
        
        elem = driver.find_element_by_link_text('Save')
        elem.click()
    except Exception as e:
        raise Exception("Issue in updateSave --> ", e)

    finally:
        if close:
            closeMenu()

def prependNewSave():
    try:
        updateSave(False)

        cookieStr = driver.get_cookie('CookieClickerGame')['value']
        
        temp = None
        try: 
            with open(filename, 'r') as f:
                temp = f.read()
        except:
            # No existing file, will be created
            pass

        utcTS = datetime.utcnow()
        with open(filename, 'w') as f:
            f.write('{0} || {1}\n\n'.format(str(utcTS), cookieStr))
            if temp:
                f.write(temp)
        print("save success")
    except Exception as e:
        print('Issue in prependNewSave > ' + e)

    finally:
        closeMenu()
        

def insertGameStateCookie(seedCookie = None):
    try:
        if seedCookie:
            cookieStr = seedCookie
        else:
            f = open(filename, 'r')
            cookieStr = re.search('(?<= \|\| )[^\s]+', f.readline()).group(0)
            f.close()

        openMenu()

        elem = driver.find_element_by_link_text('Import save')
        elem.click()

        alert = driver.switch_to_alert()
        alert.send_keys(cookieStr)
        alert.accept()

    except Exception as e:
        # FIX - this can fail sometimes
        print("oops in insertCookie -->  ", e)

    finally:
        # Close Menu
        closeMenu()

def openMenu():
    if not isMenuOpen():
        toggleMenu()

def closeMenu():
    if isMenuOpen():
        toggleMenu()

def toggleMenu():
    elem = driver.find_element_by_id('prefsButton')
    elem.click()

def isMenuOpen():
    elem = driver.find_element_by_id('menu')
    return len(elem.text) > 0

run()


