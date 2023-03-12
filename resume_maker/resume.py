import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
def validate_data(txt):
    if(txt):
        return True
    else:
        return False
def generate_data(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.get('https://www.linkedin.com')

    username = driver.find_element('id','session_key') # logging in using dummy account
    username.send_keys("officialap1812@gmail.com")
    time.sleep(0.5)

    password = driver.find_element('id','session_password')
    password.send_keys("pratham1812")
    time.sleep(0.5)

    sign_in_button = driver.find_element('xpath','//*[@type="submit"]') #instructing selenium to find sign in button and clicking it
    sign_in_button.click()
    time.sleep(0.5)


    linkedin_url = url

    driver.get(linkedin_url)


    start = time.time()

    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000

    while True:   #code to scroll down the web page inorder to ensure that all data gets loaded on the webpage
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000

        # we will stop the script for 2 seconds so that
        # the data can load
        time.sleep(2)
       

        end = time.time()
       
        if round(end - start) > 7:
            break


    src = driver.page_source
    driver.quit()
    soup = BeautifulSoup(src,"lxml")


    about= soup.find("div",{"class":"text-body-medium"})  #finding the bio section in profile


    lst = soup.find_all("ul",{"class":"pvs-list"})

    ind = [j for j in range(len(lst)) if len(lst[j].find_all("li",{"class":"artdeco-list__item"})) != 0]  #logic to implement accurate scraping of data


    heading = soup.find_all("h2",{"class":"pvs-header__title"})
    reqd = []

    for k in heading:
        reqd.append(k.find("span",{"class":"visually-hidden"}).get_text().strip())




    if("About" in reqd):  #implementing logic to ensure data retrieved points to correct category
        reqd.remove("About")

    if("Activity" in reqd):
        reqd.remove("Activity")

    if("Featured" in reqd):
        reqd.remove("Featured")
    ind.remove(0)
    while(len(reqd) != len(ind)):
        ind.remove(ind[-1])


    s = []


    for k in ind:
        exp = lst[k].find_all("li",{"class":"artdeco-list__item"})
        
        res = []
        
        for j in exp:
            
            x = j.find_all("span",{"class":"visually-hidden"})
            ls = []
            for k in x:
                
                if(validate_data(k)):
                    ls.append(k.get_text().strip())
               

            result = "\n".join(ls)
            res.append(result)
            
        s.append(res)

    about1 = soup.find_all("span",{"class":"visually-hidden"})[3]



    final = dict(zip(reqd,s))  #creating our object which contains relevant text for relevant category
    if(validate_data(about)):
        final["Bio"] = about.get_text().strip()
    else:
        final["Bio"] = ""
    if(validate_data(about1)):
        final["About"] = about1.get_text().strip()
    else:
        final["About"] = ""

    if("Skills" in list(final.keys())):
        res = [j.split("\n")[0] for j in final["Skills"]]
        final["Skills"] = res


    return final


