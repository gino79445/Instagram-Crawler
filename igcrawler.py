from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os
import wget

import getpass
def enterIg(usern,passw):
    PATH = os.getcwd()+'\chromedriver'
    
    # driver = webdriver.Chrome(PATH)
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    driver.maximize_window()
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

    login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
    login.click()

    return driver

def search(driver,keyword):
    search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
    )
    # search = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located(By.CSS_SELECTOR, ".QY4Ed.P0xOK")
    # )
    

    # keyword = 'mybosseatshit'
    search.send_keys(keyword)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(1)
    search.send_keys(Keys.RETURN)

def scroll(driver,numscr):
    for i in range(numscr):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
   

def downloadImg(driver,keyword,numscr):
    
    scroll(driver,numscr)   

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
    f = open(path+'\\'+keyword+"likeuser"+str(count)+'.txt', 'w+')
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
        
        time.sleep(2)
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
    

def userDetails(driver,keyword,numscr,storiesnum):
    
    
    count = 0
    dictPath  = os.path.join(keyword)
    os.mkdir(dictPath)

    # for i in range(num):
    #     for j in range(3):
    #         front = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div['
    #         mid = ']/div['
    #         back = ']/a/div'
    #         p = front +str(i+1)+mid +str(j+1)+back
    #         link =driver.find_element_by_xpath(p)
    #         driver.execute_script("arguments[0].click();", link)
    
    
    global links 
    links =  WebDriverWait(driver, 10).until(
         EC.presence_of_all_elements_located((By.CLASS_NAME, "_9AhH0"))
    )
    t=0
    while(t<numscr):
   
        
        try:
            driver.execute_script("arguments[0].click();", links[t])
        except:
            scroll(driver,1)
            newlinks = WebDriverWait(driver, 10).until(
                 EC.presence_of_all_elements_located((By.CLASS_NAME, "_9AhH0"))
            )
            for element in newlinks:
                if element not in links:
                    links.append(element)

            driver.execute_script("arguments[0].click();", links[t])

      
        time.sleep(2)
    
        try:

            imgs = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eLAPa.kPFhm"))
            )
            

            img = imgs[0].find_element_by_class_name("FFVAD")
            # print(img.get_attribute("src"))
            dataPath = dictPath+'/'+keyword+str(count)
            os.mkdir(dataPath)
            save_as =os.path.join(dataPath,keyword + str(count)+'.jpg')

            wget.download(img.get_attribute("src"),save_as)
            
            comment(driver,dataPath,keyword,count)
            likeusers(driver,dataPath,keyword,count,storiesnum)
        except:
            try:
            

                imgs = WebDriverWait(driver, 1).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eLAPa.RzuR0"))
                )
                img = imgs[0].find_element_by_class_name("FFVAD")
                # print(img.get_attribute("src"))
                dataPath = dictPath+'/'+keyword+str(count)
                os.mkdir(dataPath)
                save_as =os.path.join(dataPath,keyword + str(count)+'.jpg')

                wget.download(img.get_attribute("src"),save_as)
                
                comment(driver,dataPath,keyword,count)
                likeusers(driver,dataPath,keyword,count,storiesnum)
            except:
                print("other")
                
    
        count+=1
        t+=1
        driver.back()
       
def comment(driver,path,keyword,count):
 
    f = open(path+'\\'+keyword+"comment"+str(count)+'.txt', 'w+',encoding='UTF-8')
    # users=driver.find_elements_by_css_selector('.sqdOP.yWX7d._8A5w5.ZIAjV')
    # time.sleep(2)
    
    users = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sqdOP.yWX7d._8A5w5.ZIAjV"))
    )
    
    comments = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.xLCgt.MMzan.KV-D4.se6yk.T0kll"))
    )
    # comments=driver.find_elements_by_css_selector('.Jv7Aj.mArmR.MqpiF')
    likers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.PIoXz.qyrsm._0PwGv.uL8Hv.T0kll"))
    )
  
    i=1
    er = 0
    for comment in comments: 
    
            if i==1:
                f.write(users[i].get_attribute("textContent")+':\n')
                f.write(comment.get_attribute("textContent")+'\n\n')
            else:
                f.write(users[i].get_attribute("textContent")+':\n')
                f.write("留言: "+comment.get_attribute("textContent")+'\n')
                string = likers[(i-2)*2+er].get_attribute("textContent")
                if string == "回覆":
                    er=er - 1
                    f.write("讚數: 0 \n")
                else :
                    f.write("讚數: "+string+'\n')
            f.write("\n")
            i+=1
    


    
def main():
   
    username = input("account: ")
    # password = input("password: ")
    password = getpass.getpass("password: ")
    keyword = input("search keyword: ")

    numscr = 10
    driver = enterIg(username,password)
    
    search(driver,keyword)
    
    # downloadImg(driver,keyword,numscr)

    storiesnum = storiesNum(driver)

    userDetails(driver,keyword,numscr,storiesnum)
    driver.close()

if __name__ == '__main__':
    
    main()