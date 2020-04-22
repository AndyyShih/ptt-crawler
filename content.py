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

#抓取貼文內資料
url = 'https://www.ptt.cc/bbs/Gossiping/M.1587455293.A.F83.html'
payload = {
    'from' : url ,
    'yes' : 'yes'
}
headers = {'user-agent' : 'my-app/0.0.1'}

rs = requests.Session()
rs.post('https://www.ptt.cc/ask/over18' , data = payload , headers = headers)
res = rs.get(url , headers = headers)
html = rs.get(url , headers = headers).content

soup = BeautifulSoup(res.text , 'html.parser')

with open("./article.csv",'w',newline='',encoding='utf-8-sig') as csvfile:
    article_writter = csv.writer(csvfile)

    #抓取文章資料(.article-metaline)
    article_data = soup.select('.article-metaline span') 
    article_writter.writerow(article_data[1]) #作者
    article_writter.writerow(article_data[3]) #標題
    article_writter.writerow(article_data[5]) #發文時間

    #抓取文章內文
    selector = etree.HTML(html)
    Content = selector.xpath('//*[@id="main-content"]/text()')
    article_writter.writerow(Content)
    
    #抓取引文(.f2 .f6)
    article_quotation = soup.select('#main-content')
    for article_quotation in article_quotation:
        article_writter.writerow(article_quotation.select('.f2')[0])#引句
    quotation = []
    for i in soup.select('.f6'):
        quotation.extend(i)
    article_writter.writerow(quotation)#引文內容
    
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



