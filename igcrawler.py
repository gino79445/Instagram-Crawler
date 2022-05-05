import random
from cv2 import exp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import pyautogui as pag
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains

import os
import wget

import getpass

global likergol
global commentgol
likergol=0
commentgol=0

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
    search.send_keys(keyword)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(1)
    search.send_keys(Keys.RETURN)

def scroll(driver,numscr):
    for i in range(numscr):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
   

def downloadImg(driver):
    try:
        imgs = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eLAPa.kPFhm"))
        )
    except:
        try:
            imgs = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".kPFhm.Y8U6w.Uvt28"))
            )
            
        except:
            #多張照片第一章
            # imgs = WebDriverWait(driver, 2).until(
            #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eLAPa.RzuR0"))
            # )
            pass
        

    img = imgs[0].find_element_by_class_name("FFVAD")
    # print(img.get_attribute("src"))
    
    return img
    


def storiesNum(driver):
    # 算精選限時數量
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

def likeusers(driver,path,keyword,count,storiesnum,people):
    f = open(path+'\\'+keyword+"likeuser"+str(count)+'.csv', 'w+')
    try:
     
        people.click()

        driver.implicitly_wait(0)
        
        # f.write(people.get_attribute("textContent")+"\n")
        global likeNum
        likeNum = people.get_attribute("textContent")
        f.write("id\n")
                 
        # time.sleep(5)                  
        # users=driver.find_elements_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')
        # 往下
        downnum=0
        
        global Users
        Users  = [] #buffer
        lastlen =-1
        last = []
        ero = 0 
        for i in range(5):
            lenusers = len(Users)
            # print(lenusers)
            
            if lenusers>=50:

                ero =0  
                temp = Users[-25:] 
                Users = temp
                # 寫入一半buffer的usrs
                for user in Users: 
                    f.write(user+'\n')

            try :
            #   Users 5 次都沒變break
                if ero == 5 :
                    break
            
                if lastlen == lenusers and last == Users  :
                    ero+=1
                    
                    
                
                # 以防直接進入上述if
                if lenusers!= 0:
                    lastlen =lenusers
                    last =Users
                # 找按讚者
              
                users = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll"))
                )
               

                # Users 增加未看過user
                for element in users:
                    if element.get_attribute("textContent") not in Users:
                        Users.append(element.get_attribute("textContent"))
                # scroll 
                # area =  WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, ".qF0y9.Igw0E.IwRSH.eGOV_.acqo5.vwCYk.i0EQd"))
                # )
                area =   WebDriverWait(driver, 10).until(
                     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".qF0y9.Igw0E.IwRSH.eGOV_.acqo5.vwCYk.i0EQd"))
                )
                area = area[1]
                # print(area.get_attribute("outerHTML"))
                area =  WebDriverWait(area, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "div"))
                )
                # print(area.get_attribute("outerHTML"))
                
                
                # area =   WebDriverWait(area, 10).until(
                #      EC.presence_of_all_elements_located((By.TAG_NAME, "div"))
                # )
              
                # area = area[0]
                # area.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                driver.execute_script('arguments[0].scrollTop ='+str(downnum)+';', area)
                # driver.execute_script("arguments[0].scrollTo(0,document.body.scrollHeight);", area)
                
                downnum+=1000
      
                sleep( random.uniform(0.2,1.5)) # Time in seconds
            except:
  
                print("error")
                break
        
        for user in Users: 
            f.write(user+'\n')

        # for user in Users: 
            
        #     f.write(user+'\n')
            
    
    except:
        f.write("This is a vedio")
        #     print("vedio")
                
                
    f.close()

def compute(likersnum,commentsnum,count):
    
    if "萬" in likersnum:
        string = likersnum.replace("萬", "")
        n1 = float(string)
        n1 = n1 * 10000
    else:
        n1 = float(likersnum)

    if "萬" in commentsnum:
        string = commentsnum.replace("萬", "")
        n2 = float(string)
        n2 = n2 * 10000
    else:
        n2 = float(commentsnum)
    global likergol
    global commentgol
    likergol = likergol + n1
    commentgol = commentgol + n2
    print("\ncount = " +str(count) +'\n' )
    print("totol likers = " +str(likergol) +'\n' )
    print("totol comments = " +str(commentgol) +'\n' )
    return likergol , commentgol

def userDetails(driver,keyword,numscr,storiesnum):
    
    global people
    count = 1
    dictPath  = os.path.join(keyword)
    os.mkdir(dictPath)
    # fq = open(dictPath+'\\'+'data5'+'.txt', 'w+',encoding='utf-8-sig')
    # 找每篇貼文連結
    global links 
    links =  WebDriverWait(driver, 10).until(
         EC.presence_of_all_elements_located((By.CLASS_NAME, "_9AhH0"))
    )
    t=0
    # numscr為貼文篇數
    while(count<=numscr):
   
        
        try:
            
            # 抓按讚、留言數
            action = ActionChains(driver)
            action.move_to_element(links[t]).perform()
            # n_like_elem = driver.find_elements_by_class_name('-V_eO')
            # 防止隱藏讚數、留言
            try:
                n_like_elem = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "-V_eO"))
                )
                likersnum = n_like_elem[0].text
                commentsnum = n_like_elem[1].text
            except:
                t=t+1
                continue
            
            # 點擊文章
            
            
            driver.execute_script("arguments[0].click();", links[t])
        except:
            # 如果發生錯誤，往下滑
            scroll(driver,1)
            newlinks = WebDriverWait(driver, 10).until(
                 EC.presence_of_all_elements_located((By.CLASS_NAME, "_9AhH0"))
            )
            # 添加至links
            for element in newlinks:
                if element not in links:
                    links.append(element)
            
            # 抓按讚、留言數
            
            action = ActionChains(driver)
            action.move_to_element(links[t]).perform()
            
            
            
            # n_like_elem = driver.find_elements_by_class_name('-V_eO')
            # 防止隱藏讚數、留言
            try:
                n_like_elem = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "-V_eO"))
                )
                likersnum = n_like_elem[0].text
                commentsnum = n_like_elem[1].text
            except:
                t=t+1
                continue
        
           
          
            
            # 點擊文章
            driver.execute_script("arguments[0].click();", links[t])

      
     
        # driver.implicitly_wait(0)
       
        try:
            
            # 下載圖片
            imgPath = downloadImg(driver)
            dataPath = dictPath+'/'+keyword+str(count)
            if not os.path.isdir(dataPath):
                a,b = compute(likersnum,commentsnum,count)
                # fq.write(str(b/a)+'\n')
                os.mkdir(dataPath)
                
            save_as =os.path.join(dataPath,keyword + str(count)+'.jpg')
            wget.download(imgPath.get_attribute("src"),save_as)
            
            # 抓按讚人
            people = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll"))
            )
            people = people[storiesnum+1]
            try:
                comment(driver,dataPath,keyword,count,likersnum,commentsnum)
            except:
                print("NO COMMENTS")
            likeusers(driver,dataPath,keyword,count,storiesnum,people)
            count+=1
            
        except:
            print("other")
    
        
        t+=1
        
        driver.back()
       
def comment(driver,path,keyword,count,likesnum,commentsnum):
 
    
    # users=driver.find_elements_by_css_selector('.sqdOP.yWX7d._8A5w5.ZIAjV')
    # time.sleep(2)

    for i in range(10):
        try :
            # 下滑留言
            
            next =  WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".qF0y9.Igw0E.IwRSH.YBx95._4EzTm.NUiEW"))
            )
            sleep(random.uniform(1,2))
            # driver.implicitly_wait(0)
            # driver.execute_script("arguments[0].click();", next)
            next.click()
            next.click()
            # print(str(i)+'\n')
            
          
        except:
            break
                   
    try:
        # 抓取 user,comment,likers,times
        users = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sqdOP.yWX7d._8A5w5.ZIAjV"))
        )
        
        comments = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.xLCgt.MMzan.KV-D4.se6yk.T0kll"))
        )
        # comments=driver.find_elements_by_css_selector('.Jv7Aj.mArmR.MqpiF')
        likers = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._7UhW9.PIoXz.qyrsm._0PwGv.uL8Hv.T0kll"))
        )
        
        times = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".FH9sR.RhOlS"))
        )
    except:
        print("comment error")

    i=1
    er = 0
    f = open(path+'\\'+keyword+"comment"+str(count)+'.csv', 'w+',encoding='utf-8-sig')
    for comment in comments: 
            # 發文者,文章資訊
            if i==1:
                
                f1 = open(path+'\\'+keyword+str(count)+'.csv', 'w+',encoding='utf-8-sig')
                f1.write("author,content,like,comment,timestamp,url\n")
                f1.write(users[i].get_attribute("textContent")+',')
                f1.write(comment.get_attribute("textContent")+',')
                # string = people.get_attribute("textContent")
                # if "," in string:
                #     string = string.replace(",", "")
                # if "個讚" in string:
                #     string = string.replace("個讚", "")
                f1.write(likesnum+',')
                f1.write(commentsnum+',')
                f1.write(times[i-1].get_attribute("datetime")+',')               
                f1.write(driver.current_url+'\n')
                f1.close()

            else:
                # 留言者
                if i==2:
                    f.write("id,comment,like,timestamp\n")

                f.write(users[i].get_attribute("textContent")+',')
                f.write(comment.get_attribute("textContent")+',')
                string = likers[(i-2)*2+er].get_attribute("textContent")
                if string == "回覆":
                    er=er - 1
                    f.write("0,")
                else :
                    if "," in string:
                        string = string.replace(",", "")
                    if "個讚" in string:
                        string = string.replace("個讚", "")
                    f.write(string+',')
                f.write(times[i-1].get_attribute("datetime")+'\n')
           
            i+=1
    


    
def main():
   
    username = input("account: ")
    # password = input("password: ")
    password = getpass.getpass("password: ")
    keyword = input("search keyword: ")

    numscr  = input("The number of posts : ")
    numscr = int(numscr)
    driver = enterIg(username,password)
    
    search(driver,keyword)
    
    # downloadImg(driver,keyword,numscr)

    storiesnum = storiesNum(driver)

    userDetails(driver,keyword,numscr,storiesnum)
    driver.close()

if __name__ == '__main__':
    
    main()