from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import operator
from collections import defaultdict
import random
import time

def fillQues(driver, numPg):
    # targeted attributes: name, value 

    listElems = driver.find_elements_by_css_selector("input[type='radio']")
    print(len(listElems))
    listElems.sort(key = lambda x: (x.get_attribute('name'), x.get_attribute('value')))
    # listElems = listElems[::-1]
    res = defaultdict(list)
    p = [0, 2]
    for i in listElems:
        # print(i.get_attribute('name'), i.get_attribute('value'), sep=' ')
        name = i.get_attribute('name')
        res[name].append(i)
    for name in res:
        n = len(res[name])
        j = p[random.randint(0, 1)] if numPg != 0 else 4
        element = res[name][j]
        driver.execute_script("arguments[0].scrollIntoView(true)", element)
        ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(3)

def test():
    a = defaultdict(list)
    a['abc'] = [5, 3, 3, 4, 2]
    a['bca'] = [3, 2, 1, 4, 5]
    # a['abc']+=[5]
    # a['abc'].append(3)
    # a['abc'].append(4)
    # print(a['abc'])

    for key in a:
        print(a[key])

# fillQues()
# test()
