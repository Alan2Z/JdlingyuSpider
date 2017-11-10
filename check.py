# -*- coding: utf-8 -*-
import os
import shutil

class Check():

    def __init__(self):
        self.path = unicode("F:/JDLY_pics","utf-8")
        self.con = 0

    #遍历path目录下的所有文件夹，获取到文件夹对象后传递给fun2
    def fun1(self):
        con=0
        for dirs in os.listdir(self.path):
            con+=1
            dirPath = self.path+"/"+dirs
            print con,dirPath
            self.fun2(dirPath)


    #检测该文件夹对象中是否存在2.jpg文件，并做出逻辑判断，是则continue 否则删除文件夹
    def fun2(self,path):
        for dirs in os.listdir(path):
            newExist = path+"/"+"2.jpg"
            if os.path.exists(newExist):
                break
            else:
                shutil.rmtree(path)
                print "------------------------------------------DELETE"+path
                # path=""
                self.con +=1

    pass

check = Check()
check.fun1()
print check.con