import os
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import csv
from bs4 import BeautifulSoup
import requests
import selenium.webdriver.support.ui as ui

#開啟瀏覽器
chromedriver = "E:/ptt-crawler/chromedriver"
driver = webdriver.Chrome(chromedriver)

#設定瀏覽網頁
url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
payload = {
    'from' : url ,
    'yes' : 'yes'
}
headers = {'user-agent' : 'my-app/0.0.1'}
'''
#讓機器人通過是否滿18歲驗證
rs = requests.Session()
rs.post('https://www.ptt.cc/ask/over18' , data = payload , headers = headers)
res = rs.get(url , headers = headers)
'''
#通過18歲條款頁面
driver.get(url)
driver.find_element_by_xpath("//button[@class = 'btn-big']").click()

soup = BeautifulSoup(driver.page_source , 'html.parser')


with open("./ptt.csv",'w',newline='',encoding='utf-8-sig') as csvfile:
    ptt_writer=csv.writer(csvfile)
    target = ['date','author','title']

    #創建所需資料各自的List
    article_date = []
    article_author = []
    article_title = []

    #將抓取的資料放入各自的List
    for i in range(0,4):
        soup = BeautifulSoup(driver.page_source , 'html.parser')
        items = soup.select('.r-ent')
        for items in items:
            article_date.extend(items.select('.date')[0])
            article_author.extend(items.select('.author')[0])
            article_title.extend(items.select('.title a')[0])
        driver.find_element_by_xpath("//div[@class = 'btn-group btn-group-paging']/a[2]").click() #點擊下頁

    #寫入抓取的資料   
    ptt_writer.writerow(article_date)
    ptt_writer.writerow(article_author)
    ptt_writer.writerow(article_title)

    driver.close()
    

