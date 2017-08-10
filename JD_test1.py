# -*- coding:utf8 -*-
__author__ = 'zouguangyu'
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import random

se = requests.session()

class Jdlingyu:

    def __init__(self):
        self.headers = {
            'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        }
        self.main_url = 'http://www.jdlingyu.wang/'
        self.load_path = 'F:\JDLY_pics\\'
        self.pin_id = ''
        self.lastPageNum = 0
        self.Pics_Url = []
        self.Pics_List = []
        self.Pics_Name = ''


    def getLastPageNums(self):      #先获取首页的HTML  找到最后一页的页码
        homePage_html = se.get(self.main_url,headers = self.headers).text  #成功获取到首页的html
        homePage_soup = BeautifulSoup(homePage_html,'lxml')
        getlastPage = homePage_soup.find(title='最后页')
        self.lastPageNum = int(getlastPage.get_text())     #成功获取到最后一页的页码
        return self.lastPageNum

    def getPage(self,pageNum):     #获取第一页中所有图集的id
        pageNum = str(pageNum)
        if pageNum == '1':
            url = self.main_url
        else:
            url = self.main_url+'/page'+pageNum+'/'

        pageHtml = se.get(url,headers=self.headers).text
        pageSoup = BeautifulSoup(pageHtml,'lxml')
        picsUrls = pageSoup.find_all('a',class_="imageLink image loading")
        picsNames = pageSoup.find_all('img',height="150")
        #打印出这一页的十个图集信息
        for x in range(0,10):
            picurl = picsUrls[x].get('href')
            picname = picsNames[x].get('alt')
            # print picurl,picname   #打印出图集的URL和图集名称
            self.Pics_Url.append(picurl)



    def getPic(self,pageUrl):   #传入图集的URL  解析出HTML
        picPageHtml = se.get(pageUrl,headers = self.headers).text
        picPageSoup = BeautifulSoup(picPageHtml,'lxml')
        hrefs = picPageSoup.find('p').find_all('a')
        self.Pics_Name = picPageSoup.find('h2', class_='main-title').get_text()
        self.Pics_Name.encode('utf-8')
        print self.Pics_Name
        x = 0
        for h in hrefs:
            url = h.get('href')
            self.Pics_List.append(url)
            x+=1
        print '共有%d张' % x

    def downPics(self,Pics_name):
        # print Pics_name.decode
        Pics_name.encode('utf-8')
        Pics_name = Pics_name.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_').replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
        Pics_List = self.Pics_List
        x = 0
        for p_l in Pics_List:
            num = str(x+1)
            io_fileExists = os.path.exists(self.load_path+Pics_name)
            if not io_fileExists:
                os.makedirs(self.load_path+Pics_name)
            bytes = se.get(p_l,headers=self.headers).content
            f = open(self.load_path+Pics_name+'\\'+num+'.jpg','wb')
            f.write(bytes)
            f.flush()
            f.close()
            x+=1
            print '第%s张图片写入成功' % x
        self.Pics_List = []


    def work(self):
        pagenum = int(self.getLastPageNums())
        for page in range(1,pagenum):
            print '--------------------------------------正在第%d页' % page
            self.getPage(page)
            time.sleep(random.randint(1,5))
            for x in range(0,10):
                self.getPic(self.Pics_Url[x])
                time.sleep(random.randint(1,5))
                io_fileExists = os.path.exists(self.load_path+self.Pics_Name+'\\')
                if io_fileExists:
                    print '文件夹存在，已跳过'
                    self.Pics_List = []
                    continue
                self.downPics(self.Pics_Name)
            self.Pics_Url = []

jd = Jdlingyu()
jd.work()