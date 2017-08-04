# -*- coding:utf8 -*-
__author__ = 'zouguangyu'
from bs4 import BeautifulSoup
import requests
import re
import time
import random


se = requests.session()

class Jdlingyu:

    #首先从main_url获取总共的页数
    #然后把每一页上的图集的id="pin-\d.+?"去重后保存在一个set中
    #每次下载一个图集时先从idSet中检查是否存在  不存在则下载并添加进去
    #

    def __init__(self):
        self.headers = {
            'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        }
        self.main_url = 'http://www.jdlingyu.wang/'
        self.load_path = ''
        self.pin_id = ''
        self.lastPageNum = 0
        self.Pics_Url = []

    def getLastPageNums(self):      #先获取首页的HTML  找到最后一页的页码
        homePage_html = se.get(self.main_url,headers = self.headers).text  #成功获取到首页的html
        homePage_soup = BeautifulSoup(homePage_html,'lxml')
        getlastPage = homePage_soup.find(title='最后页')
        self.lastPageNum = int(getlastPage.get_text())     #成功获取到最后一页的页码
        # pagenum = str(self.lastPageNum)

        return self.lastPageNum


    def getPage(self,pageNum):     #获取第一页中所有图集的id
        pageNum = str(pageNum)
        if pageNum == 1:
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
            # print self.Pics_Url[x]
            # self.getPic(picurl)
            time.sleep(random.randint(range(1,5)))

    def getPic(self,pageUrl):   #传入图集的URL  解析出HTML
        picPageHtml = se.get(pageUrl,headers = self.headers).text
        # picPageSoup = BeautifulSoup(picPageHtml,'lxml')
        # pList = picPageSoup.find_all('a',class_="phzoom")
        # for p in pList:
        #     print p.get('href')
        # print picPageHtml
        # print picPageSoup
        r = 'a href="http:\/\/wx2\.sinaimg\.cn\/large/.+?\.jpg"'
        piclink = re.compile(r)
        piclink.findall(picPageHtml)
        print piclink



    # <img title alt src="http://wx3.sinaimg.cn/large/d030806aly1fi6x5j1hdrj20xc1dxn2v.jpg" width="1200" height="1797" class="lazy">
    # <a href="http://wx3.sinaimg.cn/large/d030806aly1fi6x5j1hdrj20xc1dxn2v.jpg" class="phzoom">



    def work(self):
        # pagenum = int(self.getLastPageNums())
        # for page in range(1,pagenum):
        #     print '正在第%d页' % page
        #     self.getPage(page)

        self.getPage(1)
        time.sleep(random.randint(range(1,5)))

        print self.getPic(self.Pics_Url[0])

        # for purl in self.Pics_Url:
        #     print purl
        #     self.getPic(purl)







jd = Jdlingyu()
jd.work()


