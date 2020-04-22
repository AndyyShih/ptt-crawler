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
from lxml import etree
import random

Block = input("請輸入版塊名稱:")
#開啟瀏覽器
chromedriver = "E:/ptt-crawler/chromedriver"
driver = webdriver.Chrome(chromedriver)

#設定瀏覽版塊
url_head = 'https://www.ptt.cc/bbs/'
url_block = str(Block)
url_tail = '/index.html'
url = url_head + url_block + url_tail
payload = {
    'from' : url ,
    'yes' : 'yes'
}
headers = {'user-agent' : 'my-app/0.0.1'}

rs = requests.Session()
rs.post('https://www.ptt.cc/ask/over18' , data = payload , headers = headers)
res = rs.get(url , headers = headers)

soup = BeautifulSoup(driver.page_source , 'html.parser')

#通過18歲條款頁面
driver.get(url)
driver.find_element_by_xpath("//button[@class = 'btn-big']").click()

soup = BeautifulSoup(driver.page_source , 'html.parser')
time.sleep(1)

#建立CSV並準備寫入資料
with open("./ptt.csv",'w',newline='',encoding='utf-8-sig') as csvfile:
    ptt_writer=csv.writer(csvfile)

    #指定抓取頁數的迴圈
    for pages in range(0,4):
        soup = BeautifulSoup(driver.page_source , 'html.parser')
        #點擊文章
        article_url = []
        for link in driver.find_elements_by_xpath('//div[@class = "title"]/a'):
            article_url.append(link.get_attribute('href'))
        length = len(article_url)

        for articles in range(0,length-3):
            driver.get(article_url[articles])
            time.sleep(1)
            #抓取文章內容
            soup = BeautifulSoup(driver.page_source , 'html.parser')

            #文章頭部資料(.article-metaline)
            article_data = soup.select('.article-metaline span') 
            ptt_writer.writerow(article_data[1]) #作者
            ptt_writer.writerow(article_data[3]) #標題
            ptt_writer.writerow(article_data[5]) #發文時間

            #抓取文章內文
            inner_url = []
            for i in soup.select('.f2 a'):
                inner_url.extend(i)
            html = rs.get(inner_url[0] , headers = headers).content
            selector = etree.HTML(html)
            Content = selector.xpath('//*[@id="main-content"]/text()')
            ptt_writer.writerow(Content)

            #抓取引文(.f2 .f6)
            article_quotation = soup.select('#main-content')
            for article_quotation in article_quotation:
                ptt_writer.writerow(article_quotation.select('.f2')[0])#引句
            quotation = []
            for i in soup.select('.f6'):
                quotation.extend(i)
            ptt_writer.writerow(quotation)#引文內容
            
        
            #抓取文章尾部資料(.f2)
            article_tail = soup.select('#main-content')
            for article_tail in article_tail:
                ptt_writer.writerow(article_tail.select('.f2 a')[0]) #文章網址
        
            #抓取推文及推文時間(.push)
            article_push = soup.select('.push')
            for article_push in article_push:
                ptt_writer.writerow(article_push.select('span')[1]) #推文者
                ptt_writer.writerow(article_push.select('span')[2]) #推文內容
                ptt_writer.writerow(article_push.select('span')[3]) #推文時間
        #返回文章列表
            driver.back()
            time.sleep(random.randint(1,5))
        #下一頁
        driver.find_element_by_xpath("//div[@class = 'btn-group btn-group-paging']/a[2]").click()

driver.close()