from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from collections import defaultdict
import random
import re

TIME = 3

def getID(fname):
    data = []
    with open(fname, 'r', encoding="utf-8") as fi:
        for line in fi:
            m = re.findall(r'A2.Sel\(\'[0-9]{9}', line)
            if len(m) != 0:
                data.append(str(m)[-2-9:-2])
    return data

def fillQues(driver, numPg):
    # targeted attributes: name, value 

    listElems = driver.find_elements_by_css_selector("input[type='radio']")
    print(len(listElems))
    listElems.sort(key = lambda x: (x.get_attribute('name'), x.get_attribute('value')))
    res = defaultdict(list)
    p = [0, 2]
    for i in listElems:
        name = i.get_attribute('name')
        res[name].append(i)
    for name in res:
        n = len(res[name])
        j = p[random.randint(0, 1)] if numPg != 0 else 4
        element = res[name][j]
        driver.execute_script("arguments[0].scrollIntoView(true)", element)
        ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(TIME)

def doButton(driver, name):
    try:
        element = driver.find_element_by_id(name)
        element.click()
        return 1
    except Exception:
        return -1 

def doText(driver, name, inp):
    element = driver.find_element_by_id(name)
    element.send_keys(inp)

def getSubjectsID(driver):
    data = driver.page_source
    with open('ou.ou', 'w', encoding="utf-8") as fo:
        fo.write(data)
    return getID('ou.ou')

def openNewTab(driver, url):
    driver.execute_script("window.open('%s', 'new_window')" % (url))
    time.sleep(TIME)
    driver.switch_to_window(driver.window_handles[1])
    
    for i in range(10): # num page
        fillQues(driver, i)
        x = doButton(driver, 'btnNext')
        if x == -1:
            break

    time.sleep(TIME)
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

def solve(driver, user, pwd):

    # Login Page
    doButton(driver, "btnLang_1")
    time.sleep(TIME)
    doText(driver, "user", user)
    doText(driver, "pwd", pwd)
    time.sleep(TIME)
    doButton(driver, "btnSubmit")
    time.sleep(TIME)
    element = driver.find_element_by_id("upSystemParams_upmodalSystemParams_divpopup")
    element.send_keys(Keys.ESCAPE)
    time.sleep(TIME)

    # Neptun Page
    driver.get("https://hallgato.neptun.elte.hu/main.aspx?ismenuclick=true&ctrl=1307")
    listSubject = getSubjectsID(driver)
    originalUrl = "https://unipoll.neptun.elte.hu/Survey.aspx?FillOutId=000000000&displaymode=noframe&lng=en-US"
    print("Type something when you finished preparing")
    s = input()
    for subject in listSubject:
        subjectUrl = originalUrl.replace("000000000", subject)
        print(subjectUrl)
        time.sleep(TIME)
        openNewTab(driver, subjectUrl)
        time.sleep(TIME)

    # Logout
    print("Option (1 for repeating, 2 for exit): ", end="")
    s = input()
    doButton(driver, "lbtnQuit")
    if s == '1':
        solve(driver)
    elif s == '2':
        driver.quit()

def main():
    print("User file: ")
    fname = input()
    with open(fname, 'r') as fi:
        user = fi.readline()
        pwd = fi.readline()
    user = user[:len(user) - 1]

    driver = webdriver.Firefox()
    driver.get("https://hallgato.neptun.elte.hu/login.aspx")
    solve(driver, user, pwd)

if __name__ == "__main__":
    main()
