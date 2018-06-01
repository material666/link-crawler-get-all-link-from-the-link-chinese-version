#!/usr/bin/env python
#-*- coding:utf-8 -*-

#作者:material
#qq412905523
#邮箱:412905523@qq.com

#author:material
#qq412905523
#mail:    412905523@qq.com

#次自动化最大优势在于可以多设备操作  想做一个安静的python版安卓sikuli。。(至于为啥不说按键精灵) (python应该可以打败按键) 不过现在这个还是比按键垃圾的
#源码有人想改下木有关系
#重点是大图识小图(现在是包含关系)(不是包含的我还没开源。)
#还有就是对接高级的图像算法 比如找怪物 不管怪物图像咋变 就是把怪物给找出来 这种图像识别算法才叫高级啦。这样的肯定秒杀按键精灵

import multiprocessing
import platform
import os, sys
import threading
import webbrowser
import subprocess
import random
import tempfile
import os
import re
import threading
import time
import xml.etree.cElementTree as ET
#import appium
from multiprocessing import Process
import subprocess
import sys

import PIL
from PIL import Image
#from PIL import ImageOps
import aircv as ac
import platform
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"
import pyperclip
import os, sys

#作者qq:412905523
#python版按键精灵
#还不想开源....不要问为啥、

class Element(object):
    """
    通过元素定位,需要Android 4.0以上
    """
    def __init__(self,boolean=False):
        """
        初始化，获取系统临时文件存储目录，定义匹配数字模式
        """
        #self.echo()
        os.popen("adb kill-server")
        os.popen("adb start-server")
        for self.Devicename in self.numberd():
            print("Elment: "+ self.Devicename)
            if boolean == True:
                self.echo(self.Devicename)
            else:
                pass
            os.popen("adb -s "+ self.Devicename +" wait-for-device")
        print("start:-------------------------------------------------------------:")
        self.tempFile = tempfile.gettempdir()
        self.tempFiledevice = tempfile.gettempdir()
        self.pattern = re.compile(r"\d+")
        #self.numberd()

    def ShowDevice(self):
        for self.Devicename in self.numberd():
            print("Elment: " + self.Devicename)

    def numberd(self):
        numberlist = ','.join(os.popen(u"adb devices").readlines()[1:-1]).replace("\tdevice", "").replace("\n",
                                                                                                          "").split(
            ',')
        return numberlist

#一些常用操作
#这些还没尝试过 看看有没bug 有的化联系作者qq412905523 我修复一下
    def quitApp(self, packageName,device= None):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        if device ==None:
            os.popen("adb shell am force-stop %s" % packageName)
        else:
            os.popen("adb -s " + device + " shell am force-stop %s" % packageName)

    def getFocusedPackageAndActivity(self,device = None):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        if device  == None:
            pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
            out = os.popen("adb shell dumpsys window w | %s \/ | %s name=" % (find_util, find_util)).readlines()
            return pattern.findall(str(out))[0]
        else:
            pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
            out = os.popen("adb -s "+device+" shell dumpsys window w | %s \/ | %s name=" % (find_util, find_util)).readlines()
            return pattern.findall(str(out))[0]

    def getCurrentPackageName(self,device = None):
        """
        获取当前运行的应用的包名
        """
        if device ==None:
            return self.getFocusedPackageAndActivity().split("/")[0]
        else:
            return self.getFocusedPackageAndActivity(device).split("/")[0]

    def startWebpage(self, url,device = None):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        if device == None:
            os.popen("adb shell am start -a android.intent.action.VIEW -d %s" % url)
        else:
            os.popen("adb -s " +device + " shell am start -a android.intent.action.VIEW -d " + url)

    #设备信息！！！------------------------------------------------------------------------------------------------------------------------------------------
    def getDeviceNatework(self,device=None):
        if device ==None:
            return ''.join(os.popen("adb shell cat /sys/class/net/wlan0/address").readlines()).replace("\r\n", "")
        else:
            return ''.join(os.popen("adb -s "+ device +" shell cat /sys/class/net/wlan0/address").readlines()).replace("\r\n", "")
    def getDeviceModule(self,device=None):
        if device ==None:
            return ''.join(os.popen("adb shell getprop ro.product.model").readlines()).replace("\r\n", "")
        else:
            return ''.join(os.popen("adb -s "+ device +" shell getprop ro.product.model").readlines()).replace("\r\n", "")
    def getDeviceSystemVersion(self,device=None):
        if device ==None:
            return ''.join(os.popen("adb shell getprop ro.build.version.release").readlines()).replace("\r\n", "")
        else:
            return ''.join(os.popen("adb -s "+ device +" shell getprop ro.build.version.release").readlines()).replace("\r\n", "")
    def getDeviceSize(self,device=None):
        if device ==None:
            return ''.join(os.popen("adb shell wm size").readlines()).replace("\r\n", "").replace("Physical size: ", "")
        else:
            return ''.join(os.popen("adb -s "+ device +" shell wm size").readlines()).replace("\r\n", "")


 #---------------------------------------------------------------------------------------------------------------------------------------------------------
    def echo(self,device=None):
        if device==None:
            print("设备型号:" + self.getDeviceModule())
            print("网络mac地址:" + self.getDeviceNatework())
            print("Android 系统版本:" + self.getDeviceSystemVersion())
            print("屏幕分辨率:" + self.getDeviceSize())
        else:
            print(device+"的设备型号:" + self.getDeviceModule(device))
            print(device+"的网络mac地址:" + self.getDeviceNatework(device))
            print(device+"的Android 系统版本:" + self.getDeviceSystemVersion(device))
            print(device+"的屏幕分辨率:" + self.getDeviceSize(device))
            #print("电池信息:" + )

    def __uidump(self,device=None):
        if device == None:
            os.popen("adb shell uiautomator dump /data/local/tmp/uidump.xml")
            os.popen("adb pull /data/local/tmp/uidump.xml " + self.tempFile)
        else:
            os.popen("adb -s "+device +r" shell uiautomator dump /data/local/tmp/uidump"+device+".xml")
            os.popen("adb -s "+device +" pull /data/local/tmp/uidump"+device+".xml " + self.tempFiledevice)

    def __element(self, attrib, name,device=None):
        """
        同属性单个元素，返回单个坐标元组
        """
        if device == None:
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                    return Xpoint, Ypoint
        else:
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump"+device+".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                    return Xpoint, Ypoint


    def findElementByPartName(self, namelist,device=None):
        """
        同属性单个元素，返回单个坐标元组
        """
        if device == None:
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(list("".join([x for x in namelist]))).issubset(set(list(elem.attrib["text"].encode("utf-8")))):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    return Xpoint, Ypoint
        else:
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump"+device+".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                #print(list("".join([x for x in namelist])))
                #print(list(elem.attrib["text"].encode("utf-8")))
                #set(dic.items()).issubset(set(elem.attrib.items()))
                #set(""join.namelist.items()).issubset(set(elem.attrib["text"].encode("utf-8").split.items()))
                if set(list("".join([x for x in namelist]))).issubset(set(list(elem.attrib["text"].encode("utf-8")))):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                    return Xpoint, Ypoint

    def findElementsByPartName(self, nameji,device = None):
        """
        同属性多个元素，返回坐标元组列表
        """
        if device == None:
            lister = []
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(list("".join([x for x in nameji]))).issubset(set(list(elem.attrib["text"].encode("utf-8")))):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    lister.append((Xpoint, Ypoint))
            return list(set(lister))
        else:
            lister = []
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(list("".join([x for x in nameji]))).issubset(set(list(elem.attrib["text"].encode("utf-8")))):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    lister.append((Xpoint, Ypoint))
            return list(set(lister))

    def __elements(self, attrib, name,device = None):
        """
        同属性多个元素，返回坐标元组列表
        """
        if device == None:
            list = []
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    list.append((Xpoint, Ypoint))
            return list
        else:
            list = []
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    list.append((Xpoint, Ypoint))
            return list

    def findElementByOthers(self,dic,device = None):
        if device == None:
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(dic.items()).issubset(set(elem.attrib.items())):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    # os.popen("adb -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
                    return Xpoint, Ypoint
        else:
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(dic.items()).issubset(set(elem.attrib.items())):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    # os.popen("adb -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
                    return Xpoint, Ypoint

    def findElementsByOthers(self, dic,device = None):
        """
        同属性多个元素，返回坐标元组列表
        """
        if device == None:
            lister = []
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(dic.items()).issubset(set(elem.attrib.items())):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    # os.popen("adb -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
                    lister.append((Xpoint, Ypoint))
            return list(set(lister))
        else:
            lister = []
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(dic.items()).issubset(set(elem.attrib.items())):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    # os.popen("adb -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
                    lister.append((Xpoint, Ypoint))
            return list(set(lister))



    def findElementByPicPath(self,picPath,device = None):
        if device == None:
            result1 = self.locateOnScreen(picPath)
            result2 = self.center(result1)
            return result2
        else:
            result1 = self.locateOnScreen(picPath,device)
            result2 = self.center(result1)
            return result2

    def findElementsByPicPath(self,picPath,device = None):
        if device == None:
            result2list = []
            result1list = self.locateAllOnScreen(picPath)
            for result1 in result1list:
                result2 = self.center(result1)
                result2list.append(result2)
        else:
            result2list = []
            result1list = self.locateAllOnScreen(picPath,device)
            for result1 in result1list:
                result2 = self.center(result1)
                result2list.append(result2)
        return result2list

    def screenshotbmp(self,device=None):
        #yige
        if device == None:
            self.mkdir(r"C:\Users\Administrator\Desktop\pic")
            os.popen(
                r"adb shell screencap -p /sdcard/screen.bmp && adb pull /sdcard/screen.bmp C:\Users\Administrator\Desktop\pic\ && adb shell rm /sdcard/screen.bmp")
            print(r"ok pic saved in C:\Users\Administrator\Desktop\pic")
            return r"C:\Users\Administrator\Desktop\pic\screen.bmp"
        #duoge
        else:
            self.mkdir(r"C:\Users\Administrator\Desktop\pic" + device)
            os.popen(r"adb -s "+device+ " shell screencap -p /sdcard/screen.bmp && adb pull /sdcard/screen.bmp C:\Users\Administrator\Desktop\pic" + device + r"\ && adb shell rm /sdcard/screen.bmp")
            print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)
            return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.bmp"

    def get_screenxy_from_bmp(self,son_bmp,device = None):
        # 获取屏幕上匹配指定截图的坐标->(x,y,width,height)
        from PIL import Image
        if device == None:
            img_main = Image.open(self.screenshotbmp())
            img_son = Image.open(son_bmp)
            datas_a = list(img_main.getdata())
            datas_b = list(img_son.getdata())
            for i, item in enumerate(datas_a):
                if datas_b[0] == item and datas_a[i + 1] == datas_b[1]:
                    yx = divmod(i, img_main.size[0])
                    main_start_pos = yx[1] + yx[0] * img_main.size[0]

                    match_test = True
                    for n in range(img_son.size[1]):
                        main_pos = main_start_pos + n * img_main.size[0]
                        son_pos = n * img_son.size[0]

                        if datas_b[son_pos:son_pos + img_son.size[0]] != datas_a[main_pos:main_pos + img_son.size[0]]:
                            match_test = False
                            break
                    if match_test:
                        return (yx[1], yx[0], img_son.size[0], img_son.size[1])
            return False
        else:
            img_main = Image.open(self.screenshotbmp(device))
            img_son = Image.open(son_bmp)
            datas_a = list(img_main.getdata())
            datas_b = list(img_son.getdata())
            for i, item in enumerate(datas_a):
                if datas_b[0] == item and datas_a[i + 1] == datas_b[1]:
                    yx = divmod(i, img_main.size[0])
                    main_start_pos = yx[1] + yx[0] * img_main.size[0]

                    match_test = True
                    for n in range(img_son.size[1]):
                        main_pos = main_start_pos + n * img_main.size[0]
                        son_pos = n * img_son.size[0]

                        if datas_b[son_pos:son_pos + img_son.size[0]] != datas_a[main_pos:main_pos + img_son.size[0]]:
                            match_test = False
                            break
                    if match_test:
                        return (yx[1], yx[0], img_son.size[0], img_son.size[1])
            return False

    def findElementByName(self, name,device = None):
        """
        通过元素名称定位
        usage: findElementByName(u"设置")
        """
        if device == None:
            return self.__element("text", name)
        else:
            return self.__element("text", name,device)

    def findElementsByName(self, name,device = None):
        if device == None:
            return self.__elements("text", name)
        else:
            return self.__elements("text", name,device)

    def findElementByClass(self, className,device = None):
        """
        通过元素类名定位
        usage: findElementByClass("android.widget.TextView")
        """
        if device == None:
            return self.__element("class", className)
        else:
            return self.__element("class", className,device)

    def findElementsByClass(self, className,device = None):
        if device == None:
            return self.__elements("class", className)
        else:
            return self.__elements("class", className,device)

    def findElementById(self, id,device = None):
        """
        通过元素的resource-id定位
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        if device == None:
            return self.__element("resource-id", id)
        else:
            return self.__element("resource-id", id,device)

    def findElementsById(self, id,device = None):
        if device == None:
            return self.__elements("resource-id", id)
        else:
            return self.__elements("resource-id", id,device)

    def findElementByContent(self, content,device = None):
        if device == None:
            return self.__element("content-desc", content)
        else:
            return self.__element("content-desc", content,device)
        #return self.__element("content-desc", content)

    def findElementsByContent(self, content,device = None):
        if device == None:
            return self.__elements("content-desc", content)
        else:
            return self.__elements("content-desc", content,device)

    def findElementByPackage(self, package,device = None):
        if device == None:
            return self.__element("package", package)
        else:
            return self.__element("package", package,device)

    def findElementsByPackage(self, package,device = None):
        if device == None:
            return self.__elements("package", package)
        else:
            return self.__elements("package", package,device)

    def findElementByXpath(self,Xpath,device = None):
        self.__uidump()
        tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            print(elem.attrib)
    #def
    def screenshot(self,device=None,box = None,screenpng =None):
        #yige
        if screenpng ==None:
            if box == None:
                if device == None:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic")
                    os.popen(
                        r"adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic\ && adb shell rm /sdcard/screen.png")
                    '''if "emulator" in self.Devicename:
                        im = PIL.Image.open(r"C:\Users\Administrator\Desktop\pic\screen.png")
                        im = im.rotate(270)
                        im.save( r"C:\Users\Administrator\Desktop\pic\screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic")'''
                    return r"C:\Users\Administrator\Desktop\pic\screen.png"
                    # duoge
                else:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic" + device)
                    os.popen(
                        r"adb -s " + device + " shell screencap -p /sdcard/screen.png && adb -s " + device + r" pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic" + device + r"\ && adb -s " + device + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)
                    '''if "emulator" in device:
                        im = PIL.Image.open(r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")
                        im = im.rotate(270)
                        im.save( r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")'''
                    return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png"

            else:
                if device == None:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic")
                    os.popen(
                        r"adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic\ && adb shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic")
                    image =  PIL.Image.open(r"C:\Users\Administrator\Desktop\pic\screen.png")
                    '''if "emulator" in self.Devicename:
                        image = image.rotate(270)
                        image.save(r"C:\Users\Administrator\Desktop\pic\screen.png")
                    newImage = image.crop(box)
                    newImage.save(r"C:\Users\Administrator\Desktop\pic\screen.png")'''
                    return r"C:\Users\Administrator\Desktop\pic\screen.png"
                    # duoge
                else:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic" + device)
                    os.popen(
                        r"adb -s " + device + " shell screencap -p /sdcard/screen.png && adb -s " + device + r" pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic" + device + r"\ && adb -s " + device + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)
                    image =  PIL.Image.open(r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")
                    '''if "emulator" in device:
                        image = image.rotate(270)
                        image.save(r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")
                    newImage = image.crop(box)
                    newImage.save("C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")'''
                    return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png"
        else:
            if box == None:
                if device == None:
                    self.mkdir(screenpng)
                    os.popen(r"adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png " +screenpng+"\ && adb shell rm /sdcard/screen.png")
                    '''if "emulator" in self.Devicename:
                        image = Image.open( screenpng+r"\screen.png")
                        image = image.rotate(270)
                    print(r"ok pic saved in "+screenpng)'''
                    return screenpng+r"\screen.png"
                    # duoge
                else:
                    self.mkdir(screenpng+r"\screen.png")
                    os.popen(
                        r"adb -s " + device + " shell screencap -p /sdcard/screen.png && adb -s " + device + r" pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic" + device + r"\ && adb -s " + device + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)
                    '''if "emulator" in device:
                        image = Image.open(r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")
                        image = image.rotate(270)'''
                    return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png"

            else:
                if device == None:
                    self.mkdir(screenpng)
                    os.popen(
                        r"adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png " +screenpng+r"\ && adb shell rm /sdcard/screen.png")
                    print(r"ok pic saved in "+screenpng)
                    '''image = Image.open(screenpng+r"/screen.png")
                    if "emulator" in self.Devicename:
                        image = image.rotate(270)
                    newImage = image.crop(box)
                    newImage.save(screenpng+r"/screen.png")'''
                    return screenpng+r"/screen.png"
                    # duoge
                else:
                    self.mkdir(screenpng)
                    os.popen(
                        r"adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png " +screenpng+"\ && adb shell rm /sdcard/screen"+device+".png")
                    print(r"ok pic saved in "+screenpng)
                    '''image = Image.open(screenpng+r"/screen"+device+".png")
                    if "emulator" in self.Devicename:
                        image = image.rotate(270)
                    newImage = image.crop(box)
                    newImage.save(screenpng+r"/screen"+device+".png")'''
                    return screenpng+r"/screen"+device+".png"

    #图像识别1类===================================================================================================================================
    def locateAllOnScreen(self,image, grayscale=False, limit=None, region=None,device=None):
        if device == None:
            screenshotIm = self.screenshot()
            retVal = self.locateAll(image, screenshotIm, grayscale, limit)
            if 'fp' in dir(screenshotIm) and screenshotIm.fp is not None:
                screenshotIm.fp.close()  # Screenshots on Windows won't have an fp since they came from ImageGrab, not a file.
            return retVal
        else:
            screenshotIm = self.screenshot(device)
            retVal = self.locateAll(image, screenshotIm, grayscale, limit)
            if 'fp' in dir(screenshotIm) and screenshotIm.fp is not None:
                screenshotIm.fp.close()  # Screenshots on Windows won't have an fp since they came from ImageGrab, not a file.
            return retVal

    def locateOnScreen(self,image, grayscale=False,device=None):
        if device == None:
            screenshotIm = self.screenshot()
            retVal = self.locate(image, screenshotIm, grayscale)
            if 'fp' in dir(screenshotIm) and screenshotIm.fp is not None:
                screenshotIm.fp.close()  # Screenshots on Windows won't have an fp since they came from ImageGrab, not a file.
            return retVal
        else:
            screenshotIm = self.screenshot(device)
            retVal = self.locate(image, screenshotIm, grayscale)
            if 'fp' in dir(screenshotIm) and screenshotIm.fp is not None:
                screenshotIm.fp.close()  # Screenshots on Windows won't have an fp since they came from ImageGrab, not a file.
            return retVal

    def mkdir(self,path):
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            os.makedirs(path)

            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            #print path + ' 目录已存在'
            return False

    def locate(self,needleImage, haystackImage, grayscale=False):
        # Note: The gymnastics in this function is because we want to make sure to exhaust the iterator so that the needle and haystack files are closed in locateAll.
        points = tuple(self.locateAll(needleImage, haystackImage, grayscale, 1))
        if len(points) > 0:
            return points[0]
        else:
            return None

    def locateAll(self,needleImage, haystackImage, grayscale=False, limit=None):
        needleFileObj = None
        haystackFileObj = None
        if isinstance(needleImage, str):
            # 'image' is a filename, load the Image object
            needleFileObj = open(needleImage, 'rb')
            needleImage = Image.open(needleFileObj)
        if isinstance(haystackImage, str):
            # 'image' is a filename, load the Image object
            haystackFileObj = open(haystackImage, 'rb')
            haystackImage = Image.open(haystackFileObj)

        if grayscale:
            needleImage = ImageOps.grayscale(needleImage)
            haystackImage = ImageOps.grayscale(haystackImage)

        needleWidth, needleHeight = needleImage.size
        haystackWidth, haystackHeight = haystackImage.size

        needleImageData = tuple(needleImage.getdata())  # TODO - rename to needleImageData??
        haystackImageData = tuple(haystackImage.getdata())

        needleImageRows = [needleImageData[y * needleWidth:(y + 1) * needleWidth] for y in
                           range(needleHeight)]  # LEFT OFF - check this
        needleImageFirstRow = needleImageRows[0]

        assert len(needleImageFirstRow) == needleWidth
        assert [len(row) for row in needleImageRows] == [needleWidth] * needleHeight

        numMatchesFound = 0

        for y in range(haystackHeight):
            for matchx in self._kmp(needleImageFirstRow, haystackImageData[y * haystackWidth:(y + 1) * haystackWidth]):
                foundMatch = True
                for searchy in range(1, needleHeight):
                    haystackStart = (searchy + y) * haystackWidth + matchx
                    if needleImageData[searchy * needleWidth:(searchy + 1) * needleWidth] != haystackImageData[
                                                                                             haystackStart:haystackStart + needleWidth]:
                        foundMatch = False
                        break
                if foundMatch:
                    # Match found, report the x, y, width, height of where the matching region is in haystack.
                    numMatchesFound += 1
                    yield (matchx, y, needleWidth, needleHeight)
                    if limit is not None and numMatchesFound >= limit:
                        # Limit has been reached. Close file handles.
                        if needleFileObj is not None:
                            needleFileObj.close()
                        if haystackFileObj is not None:
                            haystackFileObj.close()

        # There was no limit or the limit wasn't reached, but close the file handles anyway.
        if needleFileObj is not None:
            needleFileObj.close()
        if haystackFileObj is not None:
            haystackFileObj.close()

    def center(self,coords):
        return (coords[0] + int(coords[2] / 2), coords[1] + int(coords[3] / 2))

    def _kmp(self,needle, haystack):  # Knuth-Morris-Pratt search algorithm implementation (to be used by screen capture)
        # build table of shift amounts
        shifts = [1] * (len(needle) + 1)
        shift = 1
        for pos in range(len(needle)):
            while shift <= pos and needle[pos] != needle[pos - shift]:
                shift += shifts[pos - shift]
            shifts[pos + 1] = shift

        # do the actual search
        startPos = 0
        matchLen = 0
        for c in haystack:
            while matchLen == len(needle) or \
                    matchLen >= 0 and needle[matchLen] != c:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == len(needle):
                yield startPos


class Event(object):
    def __init__(self):
        #self.numberd()
        os.popen("adb kill-server")
        os.popen("adb start-server")
        for Devicename in self.numberd():
            print("Event: "+ Devicename)
            os.popen("adb -s "+ Devicename +" wait-for-device")

    def numberd(self):
        numberlist = ','.join(os.popen(u"adb devices").readlines()[1:-1]).replace("\tdevice","").replace("\n","").split(',')
        #print(numberlist)
        return numberlist

    def touch(self, dx, dy,device=None):
        if device == None:
            print(str(dx) + ", " + str(dy))
            os.popen("adb shell input tap " + str(dx) + " " + str(dy))
            time.sleep(0.5)
        else:
            print(str(dx) + ", " + str(dy))
            os.popen("adb -s " + device + " shell input tap " + str(dx) + " " + str(dy))
            time.sleep(0.5)

    def swipe(self,x2,y2,x1,y1,device=None):
        if device == None:
            print(str((x2,y2,x1,y1)))
            os.popen("adb shell input swipe " + str(x2) + " " + str(y2)+ " " + str(x1)+ " " + str(y1))
            time.sleep(0.5)
        else:
            print(str((x2,y2,x1,y1)))
            os.popen("adb -s " + device + " shell input swipe " + str(x2) + " " + str(y2)+ " " + str(x1)+ " " + str(y1))
            time.sleep(0.5)



