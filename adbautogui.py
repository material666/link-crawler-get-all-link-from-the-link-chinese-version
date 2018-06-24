#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author qq: 412905523

try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

import re

import platform

import os

PATH = lambda p: os.path.abspath(p)
# 判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"
# 判断是否设置环境变量ANDROID_HOME
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
    else:
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
else:
    raise EnvironmentError(
        "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])
import random
import tempfile
import time
import xml.etree.cElementTree as ET
import  subprocess
import winsound
from PIL import Image
from PIL import ImageOps
import threading
import os
adbpath = "adb"
import webbrowser


class Element(object):
    """
    通过元素定位,需要Android 4.0以上
    """

    def __init__(self, id="11102", boolean=False):
        """
        初始化，获取系统临时文件存储目录，定义匹配数字模式
        """
        p = subprocess.Popen("set ANDROID_ADB_SERVER_PORT=" + id, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p = subprocess.Popen(adbpath + " kill-server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p.stdout.read())
        print(
            subprocess.call(adbpath + " start-server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for self.Devicename in self.numberd():
            print("Elment: " + self.Devicename)
            if boolean == True:
                self.echo(self.Devicename)
            else:
                pass
            print(subprocess.call(adbpath + " -s " + self.Devicename + " wait-for-device", shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        print("start:-------------------------------------------------------------:")
        self.tempFile = tempfile.gettempdir()
        self.tempFiledevice = tempfile.gettempdir()
        self.pattern = re.compile(r"\d+")

    def ShowDevice(self):
        for self.Devicename in self.numberd():
            print(self.Devicename)

    def numberd(self):
        numberlist = ','.join(os.popen(adbpath + u" devices").readlines()[1:-1]).replace("\tdevice", "").replace(
            "\n",
            "").split(
            ',')
        return numberlist

    # 一些常用操作

    def quitApp(self, packageName, device=None):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        if device == None:
            os.popen(adbpath + " shell am force-stop %s" % packageName)
        else:
            os.popen(adbpath + " -s " + device + " shell am force-stop %s" % packageName)

    def getFocusedPackageAndActivity(self, device=None):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        if device == None:
            pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
            out = os.popen(
                adbpath + " shell dumpsys window w | %s \/ | %s name=" % (find_util, find_util)).readlines()
            return pattern.findall(str(out))[0]
        else:
            pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
            out = os.popen(adbpath + " -s " + device + " shell dumpsys window w | %s \/ | %s name=" % (
                find_util, find_util)).readlines()
            return pattern.findall(str(out))[0]

    def getCurrentPackageName(self, device=None):
        """
        获取当前运行的应用的包名
        """
        if device == None:
            return self.getFocusedPackageAndActivity().split("/")[0]
        else:
            return self.getFocusedPackageAndActivity(device).split("/")[0]

    def startWebpage(self, url, device=None):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        if device == None:
            os.popen(adbpath + " shell am start -a android.intent.action.VIEW -d %s" % url)
        else:
            os.popen(adbpath + " -s " + device + " shell am start -a android.intent.action.VIEW -d " + url)

    # 设备信息！！！------------------------------------------------------------------------------------------------------------------------------------------
    def getDeviceNatework(self, device=None):
        if device == None:
            return ''.join(os.popen(adbpath + " shell cat /sys/class/net/wlan0/address").readlines()).replace(
                "\r\n", "")
        else:
            return ''.join(os.popen(
                adbpath + " -s " + device + " shell cat /sys/class/net/wlan0/address").readlines()).replace("\r\n",
                                                                                                            "")

    def getDeviceModule(self, device=None):
        if device == None:
            return ''.join(os.popen(adbpath + " shell getprop ro.product.model").readlines()).replace("\r\n", "")
        else:
            return ''.join(
                os.popen(adbpath + " -s " + device + " shell getprop ro.product.model").readlines()).replace("\r\n",
                                                                                                             "")

    def getDeviceSystemVersion(self, device=None):
        if device == None:
            return ''.join(os.popen(adbpath + " shell getprop ro.build.version.release").readlines()).replace(
                "\r\n", "")
        else:
            return ''.join(os.popen(
                adbpath + " -s " + device + " shell getprop ro.build.version.release").readlines()).replace("\r\n",
                                                                                                            "")

    def getDeviceSize(self, device=None):
        if device == None:
            return ''.join(os.popen(adbpath + " shell wm size").readlines()).replace("\r\n", "").replace(
                "Physical size: ", "")
        else:
            return ''.join(os.popen(adbpath + " -s " + device + " shell wm size").readlines()).replace("\r\n", "")

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    def echo(self, device=None):
        if device == None:
            print("设备型号:" + self.getDeviceModule())
            print("网络mac地址:" + self.getDeviceNatework())
            print("Android 系统版本:" + self.getDeviceSystemVersion())
            print("屏幕分辨率:" + self.getDeviceSize())
        else:
            print(device + "的设备型号:" + self.getDeviceModule(device))
            print(device + "的网络mac地址:" + self.getDeviceNatework(device))
            print(device + "的Android 系统版本:" + self.getDeviceSystemVersion(device))
            print(device + "的屏幕分辨率:" + self.getDeviceSize(device))
            # print("电池信息:" + )

    def __uidump(self, device=None):
        if device == None:
            os.popen(adbpath + " shell uiautomator dump /data/local/tmp/uidump.xml")
            os.popen(adbpath + " pull /data/local/tmp/uidum.xml " + self.tempFile)
        else:
            os.popen(
                adbpath + " -s " + device + r" shell uiautomator dump /data/local/tmp/uidump" + device + ".xml")
            os.popen(
                adbpath + " -s " + device + " pull /data/local/tmp/uidump" + device + ".xml " + self.tempFiledevice)

    def __element(self, attrib, name, device=None):
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
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                    return Xpoint, Ypoint

    def others(self, device=None):
        if device == None:
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                print(elem)
        else:
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                print(elem)

    def findElementByPartName(self, namelist, device=None):
        """
        同属性单个元素，返回单个坐标元组
        """
        if device == None:
            self.__uidump()
            tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if set(list("".join([x for x in namelist]))).issubset(
                        set(list(elem.attrib["text"].encode("utf-8")))):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    return Xpoint, Ypoint
        else:
            self.__uidump(device)
            tree = ET.ElementTree(file=self.tempFiledevice + "\\uidump" + device + ".xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                # print(list("".join([x for x in namelist])))
                # print(list(elem.attrib["text"].encode("utf-8")))
                # set(dic.items()).issubset(set(elem.attrib.items()))
                # set(""join.namelist.items()).issubset(set(elem.attrib["text"].encode("utf-8").split.items()))
                if set(list("".join([x for x in namelist]))).issubset(
                        set(list(elem.attrib["text"].encode("utf-8")))):
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                    return Xpoint, Ypoint

    def findElementsByPartName(self, nameji, device=None):
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

    def __elements(self, attrib, name, device=None):
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

    def findElementByOthers(self, dic, device=None):
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
                    # os.popen(adbpath + " -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
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
                    # os.popen(adbpath + " -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
                    return Xpoint, Ypoint

    def findElementsByOthers(self, dic, device=None):
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
                    # os.popen(adbpath + " -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
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
                    # os.popen(adbpath + " -s SS6TIFZT99999999 shell input tap " + str(Xpoint) + " " + str(Xpoint))
                    lister.append((Xpoint, Ypoint))
            return list(set(lister))

    def findElementByPicPath(self, picPath, device=None):
        if device == None:
            result1 = self.locateOnScreen(picPath)
            result2 = self.center(result1)
            return result2
        else:
            result1 = self.locateOnScreen(picPath, device)
            result2 = self.center(result1)
            return result2

    def findElementByPicPathAndAc(self, picPath, device=None):
        if device == None:
            t1 = ac.imread(self.screenshot())
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            coordinate = ac.find_all_template(t1, t2)[0]["result"]
            # print(coordinate)
            print('Time used:', time.time() - start)
            return coordinate
        else:
            t1 = ac.imread(self.screenshot(device))
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            coordinate = ac.find_all_template(t1, t2)[0]["result"]
            # print(coordinate)
            print('Time used:', time.time() - start)
            return coordinate

    def findElementByPicPathAndAc(self, picPath, device=None):
        if device == None:
            t1 = ac.imread(self.screenshot())
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)[0]
            print(final)
            print('Time used:', time.time() - start)
            if final:
                return final[0]
            else:
                return {'confidence': None, 'result': None, 'rectangle': None}
        else:
            t1 = ac.imread(self.screenshot(device))
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            print('Time used:', time.time() - start)
            if final:
                return final[0]
            else:
                return {'confidence': None, 'result': None, 'rectangle': None}

    def findElementByPicPathAndAcReturnCordinate(self, picPath, device=None):
        if device == None:
            t1 = ac.imread(self.screenshot())
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            try:
                coordinate = ac.find_all_template(t1, t2)[0]["result"]
                # print(coordinate)
                print('Time used:', time.time() - start)
                return coordinate
            except:
                return None

        else:
            t1 = ac.imread(self.screenshot(device))
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            try:
                coordinate = ac.find_all_template(t1, t2)[0]["result"]
                # print(coordinate)
                print('Time used:', time.time() - start)
                return coordinate
            except:
                return None

    def findElementsByPicPathAndAcReturnCordinate(self, picPath, device=None):
        coordinatelist = []
        if device == None:
            t1 = ac.imread(self.screenshot())
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            for coordinatedic in final:
                coordinate = coordinatedic["result"]
                coordinatelist.append(coordinate)
            # print(coordinate)
            print('Time used:', time.time() - start)
            return coordinatelist
        else:
            t1 = ac.imread(self.screenshot(device))
            t2 = ac.imread(picPath)
            import time
            start = time.time()
            final = ac.find_all_template(t1, t2)
            print(final)
            for coordinatedic in final:
                coordinate = coordinatedic["result"]
                coordinatelist.append(coordinate)
            # print(coordinate)
            print('Time used:', time.time() - start)
            return coordinatelist

    def findElementsByPicPath(self, picPath, device=None):
        if device == None:
            result2list = []
            result1list = self.locateAllOnScreen(picPath)
            for result1 in result1list:
                result2 = self.center(result1)
                result2list.append(result2)
        else:
            result2list = []
            result1list = self.locateAllOnScreen(picPath, device)
            for result1 in result1list:
                result2 = self.center(result1)
                result2list.append(result2)
        return result2list

    def screenshotbmp(self, device=None):
        # yige
        if device == None:
            self.mkdir(r"C:\Users\Administrator\Desktop\pic")
            os.popen(
                radbpath + " shell screencap -p /sdcard/screen.bmp && " + adbpath + " pull /sdcard/screen.bmp C:\Users\Administrator\Desktop\pic\ && " + adbpath + " shell rm /sdcard/screen.bmp")
            print(r"ok pic saved in C:\Users\Administrator\Desktop\pic")
            return r"C:\Users\Administrator\Desktop\pic\screen.bmp"
        # duoge
        else:
            self.mkdir(r"C:\Users\Administrator\Desktop\pic" + device)
            os.popen(
                radbpath + " -s " + device + r" shell screencap -p /sdcard/screen.bmp && " + adbpath + " pull /sdcard/screen.bmp C:\Users\Administrator\Desktop\pic" + device + r"\ && " + adbpath + " shell rm /sdcard/screen.bmp")
            print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)
            return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.bmp"

    def get_screenxy_from_bmp(self, son_bmp, device=None):
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

                        if datas_b[son_pos:son_pos + img_son.size[0]] != datas_a[
                                                                         main_pos:main_pos + img_son.size[0]]:
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

                        if datas_b[son_pos:son_pos + img_son.size[0]] != datas_a[
                                                                         main_pos:main_pos + img_son.size[0]]:
                            match_test = False
                            break
                    if match_test:
                        return (yx[1], yx[0], img_son.size[0], img_son.size[1])
            return False

    def findElementByName(self, name, device=None):
        """
        通过元素名称定位
        usage: findElementByName(u"设置")
        """
        if device == None:
            return self.__element("text", name)
        else:
            return self.__element("text", name, device)

    def findElementsByName(self, name, device=None):
        if device == None:
            return self.__elements("text", name)
        else:
            return self.__elements("text", name, device)

    def findElementByClass(self, className, device=None):
        """
        通过元素类名定位
        usage: findElementByClass("android.widget.TextView")
        """
        if device == None:
            return self.__element("class", className)
        else:
            return self.__element("class", className, device)

    def findElementsByClass(self, className, device=None):
        if device == None:
            return self.__elements("class", className)
        else:
            return self.__elements("class", className, device)

    def findElementById(self, id, device=None):
        """
        通过元素的resource-id定位
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        if device == None:
            return self.__element("resource-id", id)
        else:
            return self.__element("resource-id", id, device)

    def findElementsById(self, id, device=None):
        if device == None:
            return self.__elements("resource-id", id)
        else:
            return self.__elements("resource-id", id, device)

    def findElementByContent(self, content, device=None):
        if device == None:
            return self.__element("content-desc", content)
        else:
            return self.__element("content-desc", content, device)
        # return self.__element("content-desc", content)

    def findElementsByContent(self, content, device=None):
        if device == None:
            return self.__elements("content-desc", content)
        else:
            return self.__elements("content-desc", content, device)

    def findElementByPackage(self, package, device=None):
        if device == None:
            return self.__element("package", package)
        else:
            return self.__element("package", package, device)

    def findElementsByPackage(self, package, device=None):
        if device == None:
            return self.__elements("package", package)
        else:
            return self.__elements("package", package, device)

    def findElementByXpath(self, Xpath, device=None):
        self.__uidump()
        tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            print(elem.attrib)

    # def
    def screenshot(self, device=None, box=None, screenpng=None):
        # yige
        if screenpng == None:
            if box == None:
                if device == None:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic")
                    os.popen(
                        radbpath + " shell screencap -p /sdcard/screen.png && " + adbpath + " pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic\ && " + adbpath + " shell rm /sdcard/screen.png")

                    return r"C:\Users\Administrator\Desktop\pic\screen.png"
                    # duoge
                else:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic" + device)
                    os.popen(
                        adbpath + " -s " + device + " shell screencap -p /sdcard/screen.png && " + adbpath + " -s " + device + r" pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic" + device + r"\ && " + adbpath + " -s " + device + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)

                    return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png"

            else:
                if device == None:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic")
                    os.popen(
                        adbpath + " shell screencap -p /sdcard/screen.png && " + adbpath + " pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic\ && " + adbpath + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic")
                    image = PIL.Image.open(r"C:\Users\Administrator\Desktop\pic\screen.png")

                    return r"C:\Users\Administrator\Desktop\pic\screen.png"
                    # duoge
                else:
                    self.mkdir(r"C:\Users\Administrator\Desktop\pic" + device)
                    os.popen(
                        adbpath + " -s " + device + " shell screencap -p /sdcard/screen.png && " + adbpath + " -s " + device + r" pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic" + device + r"\ && " + adbpath + " -s " + device + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)
                    image = PIL.Image.open(r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png")

                    return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png"
        else:
            if box == None:
                if device == None:
                    self.mkdir(screenpng)
                    os.popen(
                        adbpath + " shell screencap -p /sdcard/screen.png && " + adbpath + " pull /sdcard/screen.png " + screenpng + "\ && " + adbpath + " shell rm /sdcard/screen.png")
                    '''if "emulator" in self.Devicename:
                        image = Image.open( screenpng+r"\screen.png")
                        image = image.rotate(270)
                    print(r"ok pic saved in "+screenpng)'''
                    return screenpng + r"\screen.png"
                    # duoge
                else:
                    self.mkdir(screenpng + r"\screen.png")
                    os.popen(
                        adbpath + " -s " + device + " shell screencap -p /sdcard/screen.png && " + adbpath + " -s " + device + r" pull /sdcard/screen.png C:\Users\Administrator\Desktop\pic" + device + r"\ && " + adbpath + " -s " + device + " shell rm /sdcard/screen.png")
                    print(r"ok pic saved in C:\Users\Administrator\Desktop\pic" + device)

                    return r"C:\Users\Administrator\Desktop\pic" + device + r"\screen.png"

            else:
                if device == None:
                    self.mkdir(screenpng)
                    os.popen(
                        adbpath + " shell screencap -p /sdcard/screen.png && " + adbpath + " pull /sdcard/screen.png " + screenpng + r"\ && " + adbpath + "b shell rm /sdcard/screen.png")
                    print(r"ok pic saved in " + screenpng)

                    return screenpng + r"/screen.png"
                    # duoge
                else:
                    self.mkdir(screenpng)
                    os.popen(
                        adbpath + " shell screencap -p /sdcard/screen.png && " + adbpath + " pull /sdcard/screen.png " + screenpng + "\ && " + adbpath + " shell rm /sdcard/screen" + device + ".png")
                    print(r"ok pic saved in " + screenpng)

                    return screenpng + r"/screen" + device + ".png"

    # 图像识别1类===================================================================================================================================
    def locateAllOnScreen(self, image, grayscale=False, limit=None, region=None, device=None):
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

    def locateOnScreen(self, image, grayscale=False, device=None):
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

    def mkdir(self, path):
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
            # print path + ' 目录已存在'
            return False

    def locate(self, needleImage, haystackImage, grayscale=False):
        # Note: The gymnastics in this function is because we want to make sure to exhaust the iterator so that the needle and haystack files are closed in locateAll.
        points = tuple(self.locateAll(needleImage, haystackImage, grayscale, 1))
        if len(points) > 0:
            return points[0]
        else:
            return None

    def locateAll(self, needleImage, haystackImage, grayscale=False, limit=None):
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
            for matchx in self._kmp(needleImageFirstRow,
                                    haystackImageData[y * haystackWidth:(y + 1) * haystackWidth]):
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

    def center(self, coords):
        return (coords[0] + int(coords[2] / 2), coords[1] + int(coords[3] / 2))

    def _kmp(self, needle,
             haystack):  # Knuth-Morris-Pratt search algorithm implementation (to be used by screen capture)
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
    def __init__(self, id="11102"):
        p = subprocess.Popen("set ANDROID_ADB_SERVER_PORT=" + id, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        subprocess.Popen(adbpath + " -p " + id + " kill-server", shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        subprocess.Popen(adbpath + "  -p " + id + " start-server", shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def touch(self, dx, dy, device=None):
        if device == None:
            print(str(dx) + ", " + str(dy))
            os.popen(adbpath + " shell input tap " + str(dx) + " " + str(dy))
            time.sleep(0.5)
        else:
            print(str(dx) + ", " + str(dy))
            os.popen(adbpath + " -s " + device + " shell input tap " + str(dx) + " " + str(dy))
            time.sleep(0.5)

    def swipe(self, x2, y2, x1, y1, device=None):
        if device == None:
            print(str((x2, y2, x1, y1)))
            os.popen(adbpath + " shell input swipe " + str(x2) + " " + str(y2) + " " + str(x1) + " " + str(y1))
            time.sleep(0.5)
        else:
            print(str((x2, y2, x1, y1)))
            os.popen(adbpath + " -s " + device + " shell input swipe " + str(x2) + " " + str(y2) + " " + str(
                x1) + " " + str(y1))
            time.sleep(0.5)

class keycode:
    def __init__(self):
        self.POWER = 26
        self.BACK = 4
        self.HOME = 3
        self.MENU = 82
        self.VOLUME_UP = 24
        self.VOLUME_DOWN = 25
        self.SPACE = 62
        self.BACKSPACE = 67
        self.ENTER = 66
        self.MOVE_HOME = 122
        self.MOVE_END = 123
class ADB(object):
    """
    单个设备，可不传入参数device_id
    """

    def __init__(self, device_id=""):
        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s %s" % device_id

    # adb命令
    def adb(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # adb shell命令
    def shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def getDeviceState(self):
        """
        获取设备状态： offline | bootloader | device
        """
        return self.adb("get-state").stdout.read().strip()

    def getDeviceID(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip()

    def getAndroidVersion(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        return self.shell("getprop ro.build.version.release").stdout.read().strip()

    def getSdkVersion(self):
        """
        获取设备SDK版本号
        """
        return self.shell("getprop ro.build.version.sdk").stdout.read().strip()

    def getDeviceModel(self):
        """
        获取设备型号
        """
        return self.shell("getprop ro.product.model").stdout.read().strip()

    def getPid(self, packageName):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        if system is "Windows":
            pidinfo = self.shell("ps | findstr %s$" % packageName).stdout.read()
        else:
            pidinfo = self.shell("ps | grep -w %s" % packageName).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return pattern.findall(" ".join(result))[0]

    def killProcess(self, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if self.shell("kill %s" % str(pid)).stdout.read().split(": ")[-1] == "":
            return "kill success"
        else:
            return self.shell("kill %s" % str(pid)).stdout.read().split(": ")[-1]

    def quitApp(self, packageName):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        self.shell("am force-stop %s" % packageName)

    def getFocusedPackageAndActivity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.shell("dumpsys window w | %s \/ | %s name=" % (find_util, find_util)).stdout.read()

        return pattern.findall(out)[0]

    def getCurrentPackageName(self):
        """
        获取当前运行的应用的包名
        """
        return self.getFocusedPackageAndActivity().split("/")[0]

    def getCurrentActivity(self):
        """
        获取当前运行应用的activity
        """
        return self.getFocusedPackageAndActivity().split("/")[-1]

    def getBatteryLevel(self):
        """
        获取电池电量
        """
        level = self.shell("dumpsys battery | %s level" % find_util).stdout.read().split(": ")[-1]

        return int(level)

    def getBatteryStatus(self):
        """
        获取电池充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        """
        statusDict = {1: "BATTERY_STATUS_UNKNOWN",
                      2: "BATTERY_STATUS_CHARGING",
                      3: "BATTERY_STATUS_DISCHARGING",
                      4: "BATTERY_STATUS_NOT_CHARGING",
                      5: "BATTERY_STATUS_FULL"}
        status = self.shell("dumpsys battery | %s status" % find_util).stdout.read().split(": ")[-1]

        return statusDict[int(status)]

    def getBatteryTemp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" % find_util).stdout.read().split(": ")[-1]

        return int(temp) / 10.0

    def getScreenResolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        pattern = re.compile(r"\d+")
        out = self.shell("dumpsys display | %s PhysicalDisplayInfo" % find_util).stdout.read()
        display = pattern.findall(out)

        return (int(display[0]), int(display[1]))

    def reboot(self):
        """
        重启设备
        """
        self.adb("reboot")

    def fastboot(self):
        """
        进入fastboot模式
        """
        self.adb("reboot bootloader")

    def getSystemAppList(self):
        """
        获取设备中安装的系统应用包名列表
        """
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.split(":")[-1].splitlines()[0])

        return sysApp

    def getThirdAppList(self):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.split(":")[-1].splitlines()[0])

        return thirdApp

    def getMatchingAppList(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.shell("pm list packages %s" % keyword).stdout.readlines():
            matApp.append(packages.split(":")[-1].splitlines()[0])

        return matApp

    def getAppStartTotalTime(self, component):
        """
        获取启动应用所花时间
        usage: getAppStartTotalTime("com.android.settings/.Settings")
        """
        time = self.shell("am start -W %s | %s TotalTime" % (component, find_util)) \
            .stdout.read().split(": ")[-1]
        return int(time)

    def installApp(self, appFile):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("d:\\apps\\Weico.apk")
        """
        self.adb("install %s" % appFile)

    def isInstall(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        if self.getMatchingAppList(packageName):
            return True
        else:
            return False

    def removeApp(self, packageName):
        """
        卸载应用
        args:
        - packageName -:应用包名，非apk名
        """
        self.adb("uninstall %s" % packageName)

    def clearAppData(self, packageName):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.shell("pm clear %s" % packageName).stdout.read().splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def resetCurrentApp(self):
        """
        重置当前应用
        """
        packageName = self.getCurrentPackageName()
        component = self.getFocusedPackageAndActivity()
        self.clearAppData(packageName)
        self.startActivity(component)

    def startActivity(self, component):
        """
        启动一个Activity
        usage: startActivity(component = "com.android.settinrs/.Settings")
        """
        self.shell("am start -n %s" % component)

    def startWebpage(self, url):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        self.shell("am start -a android.intent.action.VIEW -d %s" % url)

    def callPhone(self, number):
        """
        启动拨号器拨打电话
        usage: callPhone(10086)
        """
        self.shell("am start -a android.intent.action.CALL -d tel:%s" % str(number))

    def sendKeyEvent(self, keycode):
        """
        发送一个按键事件
        args:
        - keycode -:
        http://developer.android.com/reference/android/view/KeyEvent.html
        usage: sendKeyEvent(keycode.HOME)
        """
        self.shell("input keyevent %s" % str(keycode))
        sleep(0.5)

    def longPressKey(self, keycode):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(keycode.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(keycode))
        sleep(0.5)

    def touch(self, e=None, x=None, y=None):
        """
        触摸事件
        usage: touch(e), touch(x=0.5,y=0.5)
        """
        if (e != None):
            x = e[0]
            y = e[1]
        if (0 < x < 1):
            x = x * self.width
        if (0 < y < 1):
            y = y * self.high

        self.shell("input tap %s %s" % (str(x), str(y)))
        sleep(0.5)

    def touchByElement(self, element):
        """
        点击元素
        usage: touchByElement(Element().findElementByName(u"计算器"))
        """
        self.shell("input tap %s %s" % (str(element[0]), str(element[1])))
        sleep(0.5)

    def touchByRatio(self, ratioWidth, ratioHigh):
        """
        通过比例发送触摸事件
        args:
        - ratioWidth -:width占比, 0<ratioWidth<1
        - ratioHigh -: high占比, 0<ratioHigh<1
        usage: touchByRatio(0.5, 0.5) 点击屏幕中心位置
        """
        self.shell("input tap %s %s" % (
        str(ratioWidth * self.getScreenResolution()[0]), str(ratioHigh * self.getScreenResolution()[1])))
        sleep(0.5)

    def swipeByCoord(self, start_x, start_y, end_x, end_y, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(800, 500, 200, 500)
        """
        self.shell("input swipe %s %s %s %s %s" % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))
        sleep(0.5)

    def swipe(self, e1=None, e2=None, start_x=None, start_y=None, end_x=None, end_y=None, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(e1, e2)
               swipe(e1, end_x=200, end_y=500)
               swipe(start_x=0.5, start_y=0.5, e2)
        """
        if (e1 != None):
            start_x = e1[0]
            start_y = e1[1]
        if (e2 != None):
            end_x = e2[0]
            end_y = e2[1]
        if (0 < start_x < 1):
            start_x = start_x * self.width
        if (0 < start_y < 1):
            start_y = start_y * self.high
        if (0 < end_x < 1):
            end_x = end_x * self.width
        if (0 < end_y < 1):
            end_y = end_y * self.high

        self.shell("input swipe %s %s %s %s %s" % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))
        sleep(0.5)

    def swipeByRatio(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, duration=" "):
        """
        通过比例发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipeByRatio(0.9, 0.5, 0.1, 0.5) 左滑
        """
        self.shell("input swipe %s %s %s %s %s" % (
        str(start_ratioWidth * self.getScreenResolution()[0]), str(start_ratioHigh * self.getScreenResolution()[1]), \
        str(end_ratioWidth * self.getScreenResolution()[0]), str(end_ratioHigh * self.getScreenResolution()[1]),
        str(duration)))
        sleep(0.5)

    def swipeToLeft(self):
        """
        左滑屏幕
        """
        self.swipeByRatio(0.8, 0.5, 0.2, 0.5)

    def swipeToRight(self):
        """
        右滑屏幕
        """
        self.swipeByRatio(0.2, 0.5, 0.8, 0.5)

    def swipeToUp(self):
        """
        上滑屏幕
        """
        self.swipeByRatio(0.5, 0.8, 0.5, 0.2)

    def swipeToDown(self):
        """
        下滑屏幕
        """
        self.swipeByRatio(0.5, 0.2, 0.5, 0.8)

    def longPress(self, e=None, x=None, y=None):
        """
        长按屏幕的某个坐标位置, Android 4.4
        usage: longPress(e)
               longPress(x=0.5, y=0.5)
        """
        self.swipe(e1=e, e2=e, start_x=x, start_y=y, end_x=x, end_y=y, duration=2000)

    def longPressElement(self, e):
        """
       长按元素, Android 4.4
        """
        self.shell("input swipe %s %s %s %s %s" % (str(e[0]), str(e[1]), str(e[0]), str(e[1]), str(2000)))
        sleep(0.5)

    def longPressByRatio(self, ratioWidth, ratioHigh):
        """
        通过比例长按屏幕某个位置, Android.4.4
        usage: longPressByRatio(0.5, 0.5) 长按屏幕中心位置
        """
        self.swipeByRatio(ratioWidth, ratioHigh, ratioWidth, ratioHigh, duration=2000)

    def sendText(self, string):
        """
        发送一段文本，只能包含英文字符和空格，多个空格视为一个空格
        usage: sendText("i am unique")
        """
        text = str(string).split(" ")
        out = []
        for i in text:
            if i != "":
                out.append(i)
        length = len(out)
        for i in xrange(length):
            self.shell("input text %s" % out[i])
            if i != length - 1:
                self.sendKeyEvent(keycode.SPACE)
        sleep(0.5)

class ElementA(object):
    """
    通过元素定位
    """

    def __init__(self, device_id=""):
        """
        初始化，获取系统临时文件存储目录，定义匹配数字模式
        """
        self.utils = ADB(device_id)

        self.tempFile = tempfile.gettempdir()
        self.pattern = re.compile(r"\d+")

    def __uidump(self):
        """
        获取当前Activity的控件树
        """
        if int(self.utils.getSdkVersion()) >= 19:
            self.utils.shell("uiautomator dump --compressed /data/local/tmp/uidump.xml").wait()
        else:
            self.utils.shell("uiautomator dump /data/local/tmp/uidump.xml").wait()
        self.utils.adb("pull data/local/tmp/uidump.xml %s" % self.tempFile).wait()
        self.utils.shell("rm /data/local/tmp/uidump.xml").wait()

    def __element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组，(x, y)
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        """
        Xpoint = None
        Ypoint = None

        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                # 获取元素所占区域坐标[x, y][x, y]
                bounds = elem.attrib["bounds"]

                # 通过正则获取坐标列表
                coord = self.pattern.findall(bounds)

                # 求取元素区域中心点坐标
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                break

        if Xpoint is None or Ypoint is None:
            raise Exception("Not found this element(%s) in current activity" % name)

        return (Xpoint, Ypoint)

    def __elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表，[(x1, y1), (x2, y2)]
        """
        pointList = []
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                # 将匹配的元素区域的中心点添加进pointList中
                pointList.append((Xpoint, Ypoint))

        return pointList

    def __bound(self, attrib, name):
        """
        同属性单个元素，返回单个坐标区域元组,(x1, y1, x2, y2)
        """
        coord = []

        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)

        if not coord:
            raise Exception("Not found this element(%s) in current activity" % name)

        return (int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))

    def __bounds(self, attrib, name):
        """
        同属性多个元素，返回坐标区域列表，[(x1, y1, x2, y2), (x3, y3, x4, y4)]
        """

        pointList = []
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                pointList.append((int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])))

        return pointList

    def __checked(self, attrib, name):
        """
        返回布尔值列表
        """
        boolList = []
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                checked = elem.attrib["checked"]
                if checked == "true":
                    boolList.append(True)
                else:
                    boolList.append(False)

        return boolList

    def findElementByName(self, name):
        """
        通过元素名称定位单个元素
        usage: findElementByName(u"设置")
        """
        return self.__element("text", name)

    def findElementsByName(self, name):
        """
        通过元素名称定位多个相同text的元素
        """
        return self.__elements("text", name)

    def findElementByClass(self, className):
        """
        通过元素类名定位单个元素
        usage: findElementByClass("android.widget.TextView")
        """
        return self.__element("class", className)

    def findElementsByClass(self, className):
        """
        通过元素类名定位多个相同class的元素
        """
        return self.__elements("class", className)

    def findElementById(self, id):
        """
        通过元素的resource-id定位单个元素
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        return self.__element("resource-id", id)

    def findElementsById(self, id):
        """
        通过元素的resource-id定位多个相同id的元素
        """
        return self.__elements("resource-id", id)

    def findElementByContentDesc(self, contentDesc):
        """
        通过元素的content-desc定位单个元素
        """
        return self.__element("content-desc", contentDesc)

    def findElementsByContentDesc(self, contentDesc):
        """
        通过元素的content-desc定位多个相同的元素
        """
        return self.__elements("content-desc", contentDesc)

    def getElementBoundByName(self, name):
        """
        通过元素名称获取单个元素的区域
        """
        return self.__bound("text", name)

    def getElementBoundsByName(self, name):
        """
        通过元素名称获取多个相同text元素的区域
        """
        return self.__bounds("text", name)

    def getElementBoundByClass(self, className):
        """
        通过元素类名获取单个元素的区域
        """
        return self.__bound("class", className)

    def getElementBoundsByClass(self, className):
        """
        通过元素类名获取多个相同class元素的区域
        """
        return self.__bounds("class", className)

    def getElementBoundByContentDesc(self, contentDesc):
        """
        通过元素content-desc获取单个元素的区域
        """
        return self.__bound("content-desc", contentDesc)

    def getElementBoundsByContentDesc(self, contentDesc):
        """
        通过元素content-desc获取多个相同元素的区域
        """
        return self.__bounds("content-desc", contentDesc)

    def getElementBoundById(self, id):
        """
        通过元素id获取单个元素的区域
        """
        return self.__bound("resource-id", id)

    def getElementBoundsById(self, id):
        """
        通过元素id获取多个相同resource-id元素的区域
        """
        return self.__bounds("resource-id", id)

    def isElementsCheckedByName(self, name):
        """
        通过元素名称判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("text", name)

    def isElementsCheckedById(self, id):
        """
        通过元素id判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("resource-id", id)

    def isElementsCheckedByClass(self, className):
        """
        通过元素类名判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("class", className)

class ImageUtils(object):

    def __init__(self, device_id=""):
        """
        初始化，获取系统临时文件存放目录
        """
        self.utils = ADB(device_id)
        self.tempFile = tempfile.gettempdir()

    def screenShot(self):
        """
        截取设备屏幕
        """
        self.utils.shell("screencap -p /data/local/tmp/temp.png").wait()
        self.utils.adb("pull /data/local/tmp/iuniTemp.png %s" %self.tempFile).wait()

        return self

    def writeToFile(self, dirPath, imageName, form = "png"):
        """
        将截屏文件写到本地
        usage: screenShot().writeToFile("d:\\screen", "image")
        """
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(PATH("%s/temp.png" %self.tempFile), PATH("%s/%s.%s" %(dirPath, imageName, form)))
        self.utils.shell("rm /data/local/tmp/temp.png")

    def loadImage(self, imageName):
        """
        加载本地图片
        usage: lodImage("d:\\screen\\image.png")
        """
        if os.path.isfile(imageName):
            load = Image.open(imageName)
            return load
        else:
            print "image is not exist"

    def subImage(self, box):
        """
        截取指定像素区域的图片
        usage: box = (100, 100, 600, 600)
              screenShot().subImage(box)
        """
        image = Image.open(PATH("%s/temp.png" %self.tempFile))
        newImage = image.crop(box)
        newImage.save(PATH("%s/temp.png" %self.tempFile))

        return self

    #http://testerhome.com/topics/202
    def sameAs(self,loadImage):
        """
        比较两张截图的相似度，完全相似返回True
        usage： load = loadImage("d:\\screen\\image.png")
                screen().subImage(100, 100, 400, 400).sameAs(load)
        """
        import math
        import operator

        image1 = Image.open(PATH("%s/temp.png" %self.tempFile))
        image2 = loadImage


        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        if differ == 0:
            return True
        else:
            return False

class Log(object):

    def __init__(self, logPath, fileName):
        self.path = logPath
        self.fileName = fileName

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        self.logFile = file(PATH("%s/%s" %(self.pathself.fileName)), "a")

    def info(self, info):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logFile.write("INFO : %s %s\n" %(timestamp, str(info)))
        self.logFile.flush()

    def debug(self,debugInfo):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logFile.write("DEBUG: %s %s\n" %(timestamp, str(debugInfo)))
        self.logFile.flush()

    def error(self, errorInfo):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.logFile.write("ERROR: %s %s\n" %(timestamp, str(errorInfo)))
        self.logFile.flush()

    def close(self):
        self.logFile.close()