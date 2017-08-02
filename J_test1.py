# -*- coding:utf8 -*-
__author__ = 'zouguangyu'
from bs4 import BeautifulSoup
import requests


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


    def getLastPageNums(self,):      #先获取首页的HTML  找到最后一页的页码
        homePage_html = se.get(self.main_url,headers = self.headers).text  #成功获取到首页的html
        homePage_soup = BeautifulSoup(homePage_html,'lxml')
        getlastPage = homePage_soup.find(title='最后页')
        self.lastPageNum = int(getlastPage.get_text())     #成功获取到最后一页的页码

        for pagenum in range(1,self.lastPageNum):
            print '正在第%s页' % pagenum
            pagenum = str(pagenum)
            self.getPage(pagenum)


    def getPage(self,pageNum):     #获取第一页中所有图集的id
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
            print picurl,picname




jd = Jdlingyu()
jd.getLastPageNums()
