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

#構想:點擊貼文->抓完資料->點上一頁
#抓取貼文內資料

url = 'https://www.ptt.cc/bbs/Gossiping/M.1587019790.A.0D4.html'
payload = {
    'from' : url ,
    'yes' : 'yes'
}
headers = {'user-agent' : 'my-app/0.0.1'}

rs = requests.Session()
rs.post('https://www.ptt.cc/ask/over18' , data = payload , headers = headers)
res = rs.get(url , headers = headers)

soup = BeautifulSoup(res.text , 'html.parser')

with open("./article.csv",'w',newline='',encoding='utf-8-sig') as csvfile:
    article_writter = csv.writer(csvfile)

    #抓取文章資料(.article-metaline)
    article_data = soup.select('.article-metaline span') 
    article_writter.writerow(article_data[1]) #作者
    article_writter.writerow(article_data[3]) #標題
    article_writter.writerow(article_data[5]) #發文時間

    #抓取文章內文
    #article_content = soup.select('#main-content')
    #article_writter.writerow(article_content) #無法僅留存#text
    
    #抓取引文(.f2 .f6)
    article_quotation = soup.select('#main-content')
    for article_quotation in article_quotation:
        article_writter.writerow(article_quotation.select('.f2')[0])
        article_writter.writerow(article_quotation.select('.f6')) #無法過濾tag
    
    #抓取文章尾段資料(.f2)
    article_tail = soup.select('#main-content')
    for article_tail in article_tail:
        article_writter.writerow(article_tail.select('.f2 a')[0])

    #抓取推文及推文時間(.push)
    article_push = soup.select('.push')
    for article_push in article_push:
        article_writter.writerow(article_push.select('span')[1]) #推文者
        article_writter.writerow(article_push.select('span')[2]) #推文內容
        article_writter.writerow(article_push.select('span')[3]) #推文時間



