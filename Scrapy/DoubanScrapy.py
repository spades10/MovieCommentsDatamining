from selenium import webdriver
import time 
import pandas as pd
import argparse

def douban_short(user_name , passwd , querys = "流浪地球" , start = 0 , pages = 10):
    driver = webdriver.Chrome()  
    url = "https://www.douban.com/"
    driver.get(url)
    time.sleep(2)
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])    #  切换到子框架
    logins = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    logins.click()
    time.sleep(2)

    user = driver.find_element_by_css_selector('#username')
    user.send_keys(user_name)
    time.sleep(2)

    passwds = driver.find_element_by_css_selector("#password")
    passwds.send_keys(passwd)

    ms = driver.find_element_by_css_selector("body > div.account-body.login-wrap.login-start.account-anonymous > div.account-tabcon-start > div.account-form > div.account-form-field-submit > a")
    ms.click()
    time.sleep(2)   
    driver.refresh()
    time.sleep(2)   
    ms = driver.find_element_by_css_selector("#db-global-nav > div > div.global-nav-items > ul > li:nth-child(3) > a")
    ms.click()
    time.sleep(2)

    # driver.close()

    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    query = driver.find_element_by_css_selector("#inp-query")
    query.send_keys(querys)
    time.sleep(2)
    ms = driver.find_element_by_css_selector("#db-nav-movie > div.nav-wrap > div > div.nav-search > form > fieldset > div.inp-btn > input[type=submit]")
    ms.click()
    time.sleep(2)
    ms = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/a")
    ms.click()
    time.sleep(2)

    ms = driver.find_element_by_xpath("//*[@id=\"comments-section\"]/div[1]/h2/span/a")
    ms.click()
    time.sleep(2)

    #    查找
    start = start
    iters = pages
    text_to_save = []
    if start != 0:
        url_cur = driver.current_url
        url = url_cur + "&start=" + str(20*(start+1)) + "&limit=20&sort=new_score"
        driver.get(url)
        time.sleep(2)

    for i in range(0, iters):
        text = driver.find_elements_by_css_selector("#comments > div > div.comment > p")
        print("Current watch on page " + str(start + i))
        for texts in text:
            text_to_save.append(texts.text)
        if i == 0:
            ms = driver.find_element_by_xpath("//*[@id=\"paginator\"]/a")
        else:
            try:
                ms = driver.find_element_by_xpath("//*[@id=\"paginator\"]/a[3]")
            except:
                break
        ms.click()
        time.sleep(5)
    driver.quit()
    testx = pd.DataFrame(columns=["text"],data=text_to_save)
    testx.to_csv('db_shortcomments.csv',encoding='utf_8_sig')

def douban_long(user_name , passwd , querys = "流浪地球" , start = 0 , pages = 10):
    driver = webdriver.Chrome()  
    url = "https://www.douban.com/"
    driver.get(url)
    time.sleep(2)
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])    #  切换到子框架
    logins = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    logins.click()
    time.sleep(2)

    user = driver.find_element_by_css_selector('#username')
    user.send_keys(user_name)
    time.sleep(2)

    passwds = driver.find_element_by_css_selector("#password")
    passwds.send_keys(passwd)

    ms = driver.find_element_by_css_selector("body > div.account-body.login-wrap.login-start.account-anonymous > div.account-tabcon-start > div.account-form > div.account-form-field-submit > a")
    ms.click()
    time.sleep(2)   
    driver.refresh()
    time.sleep(2)   
    ms = driver.find_element_by_css_selector("#db-global-nav > div > div.global-nav-items > ul > li:nth-child(3) > a")
    ms.click()
    time.sleep(2)

    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    query = driver.find_element_by_css_selector("#inp-query")
    query.send_keys(querys)
    time.sleep(2)
    ms = driver.find_element_by_css_selector("#db-nav-movie > div.nav-wrap > div > div.nav-search > form > fieldset > div.inp-btn > input[type=submit]")
    ms.click()
    time.sleep(2)
    ms = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/a")
    ms.click()
    time.sleep(2)

    ms = driver.find_element_by_xpath("//*[@id=\"reviews-wrapper\"]/header/h2/span/a")
    ms.click()
    time.sleep(2)
    start = start
    # iters = 1048
    iters = pages
    title_to_save = []
    text_to_save = []
    if start != 0:
        url_cur = driver.current_url
        url = url_cur + "?&start=" + str(20*(start+1))
        driver.get(url)
        time.sleep(2)
    for i in range(0, iters):
        # mss = driver.find_elements_by_xpath("//*[@class=\"unfold\"]")
        # for ms in mss:
        #     ms.click()
        # a= input()
        titles = driver.find_elements_by_css_selector("div > h2 > a")
        shortcs = driver.find_elements_by_xpath("//*[@class=\"short-content\"]")
        for title in titles:
            title_to_save.append(title.text)
        for shortc in shortcs:
            a = shortc.text.replace("这篇影评可能有剧透","").replace("(展开)","").replace("\n","")
            text_to_save.append(a)
        print("Current watch on page " + str(start + i))
        try:
            ms = driver.find_element_by_xpath("//*[@id=\"content\"]/div/div[1]/div[2]/span[4]/a")
        
        except:
            try:
                ms = driver.find_element_by_xpath("//*[@id=\"content\"]/div/div[1]/div[2]/span[5]/a")
            except:
                break
        ms.click()
        time.sleep(5)
    driver.quit()
    testx = pd.DataFrame({"title":title_to_save,"text":text_to_save})
    testx.to_csv('db_longcomments.csv',encoding='utf_8_sig')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawling film comments on douban')

    parser.add_argument('--type', type=str, default='long',help='choose the type of comment (long or short)')
    parser.add_argument('--user', type=str, default=None, required = True , help='username')
    parser.add_argument('--passwd', type=str, default=None, required = True , help='password')
    parser.add_argument('--start', type=int, default=0, help='start page')     
    parser.add_argument('--pages', type=int, default=10,help='page number')         
    parser.add_argument('--query', type=str, default="流浪地球" ,help='film name')           
    args = parser.parse_args()
    if args.type == 'short':
        douban_short(user_name = args.user , passwd = args.passwd , querys=args.query , start = args.start , pages = args.pages)
    else:
        douban_long(user_name = args.user , passwd = args.passwd , querys=args.query , start = args.start , pages = args.pages)