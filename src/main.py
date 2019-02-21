from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import getID
import fillQues

TIME = 3

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
    return getID.getID('ou.ou')

def openNewTab(driver, url):
    driver.execute_script("window.open('%s', 'new_window')" % (url))
    time.sleep(TIME)
    driver.switch_to_window(driver.window_handles[1])
    
    # OK: We need to find a better way for finding element
    for i in range(10): # num page
        fillQues.fillQues(driver, i)
        x = doButton(driver, 'btnNext')
        if x == -1:
            break

    time.sleep(TIME)
    # driver.execute_script("window.close()")
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

def solve(driver, user, pwd):

    ######## Login Page
    # DONE: Handle the case when previous session still active
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

    ######## Neptun Page
    driver.get("https://hallgato.neptun.elte.hu/main.aspx?ismenuclick=true&ctrl=1307")
    # Now we have a list to fill, 
    # each has this type of url https://unipoll.neptun.elte.hu/Survey.aspx?FillOutId=375042069&displaymode=noframe&lng=en-US
    # every subject has similar url except for "375042069", we call this ID of subject
    # now we need to find all of them
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

    ######## Logout
    print("Option (1 for repeating, 2 for exit): ", end="")
    s = input()
    doButton(driver, "lbtnQuit")
    if s == '1':
        solve(driver)
    elif s == '2':
        driver.quit()

def main():
    print("User file: ") # Get user and pwd from file
    fname = input()
    with open(fname, 'r') as fi:
        user = fi.readline()
        pwd = fi.readline()
    user = user[:len(user) - 1]

    driver = webdriver.Firefox()
    driver.get("https://hallgato.neptun.elte.hu/login.aspx")
    solve(driver)

if __name__ == "__main__":
    main()
