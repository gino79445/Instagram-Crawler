from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os
import wget

def enterIg(usern,passw):
    PATH = r"C:\Users\user\Documents\crawler-selenium\chromedriver"
    # driver = webdriver.Chrome(PATH)
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    driver.get("https://www.instagram.com/")
    

    # 等10秒
    username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
    )
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
    )
    password = driver.find_element_by_name("password")

    username.clear()
    password.clear()
    username.send_keys(usern)
    password.send_keys(passw)
    print("d")
    login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
    login.click()

    return driver

def search(driver,keyword):
    search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
    )

    # keyword = 'mybosseatshit'
    search.send_keys(keyword)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    

def downloadImg(driver,keyword,numscr):
    
    for i in range(numscr):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)

    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'FFVAD'))
    )

    # 創資料夾
    path  = os.path.join(keyword)
    os.mkdir(path)

    imgs =driver.find_elements_by_class_name("FFVAD")
    count = 0
    for img in imgs:
    
        save_as =os.path.join(path,keyword + str(count)+'.jpg')
        wget.download(img.get_attribute("src"),save_as)
        count+=1

def storiesNum(driver):
    # time.sleep(3)
    # stories = driver.find_elements_by_class_name('mpzUq')
    # try:
    stories = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mpzUq"))
    )
    storiesNum = 0
    for storie in stories:
     storiesNum+=1
    # except:
    #     storiesNum=-1
    return storiesNum

def likeusers(driver,path,keyword,count,storiesnum):
    f = open(path+'\\'+keyword+str(count)+'.txt', 'w+')
    try:
        # time.sleep(5)
        # people=driver.find_elements_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll')
        people = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll"))
        )
        people = people[storiesnum]

        # people=driver.find_element_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
        # print(people.get_attribute("textContent")) 
     
        people.click()
        f.write(people.get_attribute("textContent")+"\n")
        
                 
        # time.sleep(5)                  
        # users=driver.find_elements_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')
        
        time.sleep(3)
        users = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll"))
        )
        
        for user in users: 
            f.write(user.get_attribute("textContent")+'\n')
            # print(user.get_attribute("title"))
    
    except:
        f.write("This is a vedio")
        #     print("vedio")
                
                
    f.close()
    

            
    driver.back()


def userDetails(driver,keyword,numscr,storiesnum):
    likeUsersPath  = os.path.join(keyword+"likeUsers")
    os.mkdir(likeUsersPath)
    commentUsersPath  = os.path.join(keyword+"commentUsers")
    os.mkdir(commentUsersPath)

    num = numscr*4 
    count = 0
    for i in range(num):
        for j in range(3):
                front = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div['
                mid = ']/div['
                back = ']/a/div'
                p = front +str(i+1)+mid +str(j+1)+back
                link =driver.find_element_by_xpath(p)
                link.click()

                comment(driver,commentUsersPath,keyword,count)
                likeusers(driver,likeUsersPath,keyword,count,storiesnum)
                count+=1
            
                
    
def comment(driver,path,keyword,count):

    f = open(path+'\\'+keyword+str(count)+'.txt', 'w+',encoding='UTF-8')
    # users=driver.find_elements_by_css_selector('.sqdOP.yWX7d._8A5w5.ZIAjV')
    users = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sqdOP.yWX7d._8A5w5.ZIAjV"))
    )
    comments=driver.find_elements_by_class_name("C4VMK")
    # comments=driver.find_elements_by_css_selector('.Jv7Aj.mArmR.MqpiF')
    for user in comments: 
            f.write(user.get_attribute("textContent")+'\n')
    f.write("\n")
    for user in users: 
            f.write(user.get_attribute("textContent")+'\n')
    # for num in range(len(users)): 
    #         f.write(users[num].get_attribute("textContent")+comments[num].get_attribute("textContent")+ '\n')

    
def main():
    username = input("username: ")
    password = input("password: ")
    keyword = input("keyword: ")

    numscr = 1
    driver = enterIg(username,password)
    search(driver,keyword)
    
    downloadImg(driver,keyword,numscr)
    # print(storiesNum(driver))
    storiesnum = storiesNum(driver)
    # loveNum(driver)
    userDetails(driver,keyword,numscr,storiesnum)
    
    driver.close()

if __name__ == '__main__':
    main()