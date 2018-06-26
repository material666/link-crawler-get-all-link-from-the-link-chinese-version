# -*- coding: utf-8 -*-
import re
import requests
from qqbot import QQBotSlot as qqbotslot, RunBot, qqbotsched
import os, time, random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : 'c2be5eebb7e84e848c8e47cb44aabb08',
        'info'   : msg,
        #'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return "你好哇"

def kickUser(bot, contact, member, content):
    gl = bot.List('group', contact.name)
    if gl:
        group = gl[0]
        membs = bot.List(group, member.name)
        if membs:
            bot.GroupKick(group, membs)
            bot.SendTo(contact,'用户@' + member.name + '你敢发广告，信不信管理员T了你')

#禁言用户
def shutUser(bot, contact, member, content):
    gl = bot.List('group', contact.name)
    if gl:
        group = gl[0]
        membs = bot.List(group, member.name)
        if membs:
            bot.GroupShut(group, membs, 86400)
            bot.SendTo(contact,'用户@' + member.name + '你敢发广告，信不信管理禁言你啊！！')

def insertChatAdContent(bot, contact, member, content, keyword):
    now = datetime.datetime.now()
    print('time:' +str(now) +'\n'
          +'name:' + str(contact.name) +'\n'
          + 'qq:' + str(contact.qq) +'\n'
          + 'content:' + content +'\n'
          + 'keyword:' + keyword +'\n')

def getkey(text):
    import hashlib
    md5_object = hashlib.md5()
    md5_object.update(text.encode())
    print(md5_object.hexdigest())
    return md5_object.hexdigest()
#优先级一
'''!-------识别是否是自己的话-------!'''
@qqbotslot
def onQQMessage(bot, contact, member, content):
    # 优先级一
    '''!-------识别是否是自己的话-------!'''
    if bot.isMe(contact, member):
        print('自己的命令')
    else:
        if contact.ctype == 'buddy':
            if "购买" in content or "注册码" in content or "软件" in content or "价格" in content:
                bot.SendTo(contact, '''miracle软件官网:
http://58.87.73.164/
拥有以下软件的演示和下载地址
客户数据系统三件套软件
兴趣部落营销软件都在官网
微博自动发帖软件
软件价格:
单款软件 
50元每月
90元每季度(一个季度90天)                
                ''')
            elif content == "购买注册码":
                bot.SendTo(contact, '请回复:注册id,邮箱号,付款方式\n(付款方式请填写微信或者支付宝,注册id和邮箱号一定要填对,您付款后注册码是发送到您邮箱中的,其中","是英文的)')
            elif "," in content and "@" in content and ".com" in content:
                if content.split(",")[2] == "支付宝" or content.split(",")[2] == "微信":
                    bot.SendTo(contact, "对不起第三方支付接口出现问题！！！！！")
                    '''if content.split(",")[2] == "支付宝":
                        istype = "1"
                    else:
                        istype = "2"
                    try:
                        goodsname = content.split(",")[0]
                        orderid = content.split(",")[0]

                        uid = "498161464611a5eccfc8c43c"
                        token = "d4460a95efb9098552780b789960caf4"

                        return_url = 'http://140.143.242.39/pay'
                        notify_url = 'http://140.143.242.39/'
                        price = "50"
                        key = getkey(goodsname + istype + notify_url + orderid + price + return_url + token + uid)
                        params = {'goodsname': goodsname, 'uid': uid, 'token': token, 'key': key, 'price': price,
                                  'istype': istype, 'return_url': return_url, 'notify_url': notify_url,
                                  'orderid': orderid, }
                        try:
                            r = requests.post("https://pay.bbbapi.com/?format=json", data=params)
                        except:
                            bot.SendTo(contact, "对不起第三方支付接口出现问题！！！！！")
                            return
                        print(r.content)
                        link = "https://www.kuaizhan.com/common/encode-png?large=true&data=" + \
                               eval(r.content.decode())['data']["qrcode"]
                        bot.SendTo(contact,
                                   r'您的id为:' + content.split(",")[0] + '\n您的邮箱为:' + content.split(",")[1] + '\n付款方式:' +
                                   content.split(",")[2] + "\n请用" + content.split(",")[2] + "下面链接中的二维码付款，注册码将发送到" +
                                   content.split(",")[1] + "\n链接: " + link)
                    except:
                        bot.SendTo(contact,"对不起第三方支付接口出现问题！！！！！")
                        return'''
                else:
                    bot.SendTo(contact, "对不起没有这种付款方式")

            elif content == "用法":
                bot.SendTo(contact, '''miracle软件官网:
http://58.87.73.164/
邮件营销三件套软件下载地址
兴趣部落营销软件下载地址都在官网！
qq提供在线注册码购买业务:
1:
私聊我时:
请回复: 购买注册码+id
群聊我时:           
请回复: @我+购买注册码+id
2:
我发送二维码链接
3:
扫码付款后，发送注册码给你
其他:
回复:随机生成身份证号
回复:计算器
(群聊时请@我和我尬聊)
(私聊直接陪我聊天)''')
            else:
                bot.SendTo(contact, get_response(content))

        if contact.ctype == 'group':
            if "购买" in content or "注册码" in content or "软件" in content or "价格" in content:
                bot.SendTo(contact, '''miracle软件官网:
http://58.87.73.164/
拥有以下软件的演示和下载地址
客户数据系统三件套软件
兴趣部落营销软件都在官网
微博自动发帖软件
软件价格:
单款软件 
50元每月
90元每季度(一个季度90天)                
                            ''')
            elif "," in content and "@" in content and ".com" in content:
                if content.split(",")[2] == "支付宝" or content.split(",")[2] == "微信":
                    bot.SendTo(contact, "对不起第三方支付接口出现问题！！！！！")
                    '''if content.split(",")[2] == "支付宝":
                        istype = "1"
                    else:
                        istype = "2"
                    try:
                        goodsname = content.split(",")[0]
                        orderid = content.split(",")[0]

                        uid = "498161464611a5eccfc8c43c"
                        token = "d4460a95efb9098552780b789960caf4"

                        return_url = 'http://140.143.242.39/pay'
                        notify_url = 'http://140.143.242.39/'
                        price = "50"
                        key = getkey(goodsname + istype + notify_url + orderid + price + return_url + token + uid)
                        params = {'goodsname': goodsname, 'uid': uid, 'token': token, 'key': key, 'price': price,
                                  'istype': istype, 'return_url': return_url, 'notify_url': notify_url,
                                  'orderid': orderid, }
                        try:
                            r = requests.post("https://pay.bbbapi.com/?format=json", data=params)
                        except:
                            bot.SendTo(contact, "对不起第三方支付接口出现问题！！！！！")
                            return
                        print(r.content)
                        link = "https://www.kuaizhan.com/common/encode-png?large=true&data=" + \
                               eval(r.content.decode())['data']["qrcode"]
                        bot.SendTo(contact,
                                   r'您的id为:' + content.split(",")[0] + '\n您的邮箱为:' + content.split(",")[1] + '\n付款方式:' +
                                   content.split(",")[2] + "\n请用" + content.split(",")[2] + "下面链接中的二维码付款，注册码将发送到" +
                                   content.split(",")[1] + "\n链接: " + link)
                    except:
                        bot.SendTo(contact,"对不起第三方支付接口出现问题！！！！！")
                        return
                else:
                    bot.SendTo(contact, "对不起没有这种付款方式")'''
            if content == "用法":
                bot.SendTo(contact, '''miracle软件官网:
http://58.87.73.164/
邮件营销三件套软件下载地址
兴趣部落营销软件下载地址都在官网！
qq提供在线注册码购买业务:
1:
私聊我时:
请回复: 购买注册码+id
群聊我时:           
请回复: @我+购买注册码+id
2:
我发送二维码链接
3:
扫码付款后，发送注册码给你
其他:
回复:随机生成身份证号
回复:计算器
(群聊时请@我和我尬聊)
(私聊直接陪我聊天)''')
            else:
                if '@ME' in content:
                    if content == '@ME':
                        bot.SendTo(contact, r'@' + member.name + r'，艾特我干嘛呢？我就一机器人，你觉得我欠揍你找开发者qq412905523修理修理我\伤心')
                    else:
                        bot.SendTo(contact, get_response(content.replace("@ME", "")))


            #群聊计算模块
            if content == "计算器":
                bot.SendTo(contact, r'@' + member.name + '''，material超级计算器
其中num1为第一个参数,num2为第二个参数,英文逗号隔开
有什么新点子可以找开发者412905523开发！！qq机器人找推广中介！！
(回复:f1,num1,num2)加法
(回复:f2,num1,num2)减法
(回复:f3,num1,num2)乘法
(回复:f4,num1,num2)除法
(回复:f5,num1,num2)乘方
(回复:f6,num1,num2)开方
(回复:f7,num1,num2)最最最简单的哈希算法
其中num1为第一个参数,num2为第二个参数,英文逗号隔开
有什么新点子可以找开发者412905523开发！！qq机器人找推广中介！！
不知道如何使用时回复:(用法)''')
                return

            if 'f1,' in content:
                ts = datetime.datetime.now()
                res = float(str(content).split(',')[1]) + float(str(content).split(',')[2])
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，加法结果为:' + str(res) + "，用时:" + str(ta))
            if 'f2,' in content:
                ts = datetime.datetime.now()
                res = float(str(content).split(',')[1]) - float(str(content).split(',')[2])
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，减法结果为:' + str(res) + "，用时:" + str(ta))
            if 'f3,' in content:
                ts = datetime.datetime.now()
                res = int(str(content).split(',')[1]) * int(str(content).split(',')[2])
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，乘法结果为:' + str(res) + "，用时:" + str(ta))
            if 'f4,' in content:
                ts = datetime.datetime.now()
                res = int(str(content).split(',')[1]) / int(str(content).split(',')[2])
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，除法结果为:' + str(res) + "，用时:" + str(ta))
            if 'f5,' in content:
                ts = datetime.datetime.now()
                res = int(str(content).split(',')[1]) ** int(str(content).split(',')[2])
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，乘方结果为:' + str(res) + "，用时:" + str(ta))
            if 'f6,' in content:
                ts = datetime.datetime.now()
                res = int(str(content).split(',')[1]) ** (1 / int(str(content).split(',')[2]))
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，开方结果为:' + str(res) + "，用时:" + str(ta))
            if 'f7,' in content:
                ts = datetime.datetime.now()
                res = random.randint(int(str(content).split(',')[1]), int(str(content).split(',')[2]))
                ta = datetime.datetime.now() - ts
                bot.SendTo(contact, r'@' + member.name + '，哈希算法结果为:' + str(res) + "，用时:" + str(ta))
            #群聊计算模块


            #身份证模块:
            if '随机生成身份证号' in content or content == "e":
                p = os.popen(r'python sfzgenerator.py')
                x = p.read()
                bot.SendTo(contact, x)

@qqbotsched(hour='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', minute='10,20,30,40,50')
def mytask(bot):
    for g in {'名侦探柯南', '机器人定制试用群', '求租_淘宝店铺', '汇编语言', '软件反汇编逆向破解群','网站、软件开发接单','material机器人定制群','举报骗子诈骗qq'}:
        if g is not None:
            timegogao = bot.List('group', g)
            if timegogao is not None:
                for group in timegogao:
                    bot.SendTo(group, '''
material机器人(请回复数字)
具体情况请找开发者！qq:412905523
不知道机器人回复规则请回复：命令
@我(艾特我)可以和我尬聊

1:qq微信智能机器人定制，开发(私聊，群聊)
2:zip/excel/rar/压缩包文件类密码找回破解
3:非文件类密码找回破解(包括验证码)
4:程序软件开发(java,python,批处理,html(css))
5:破解，逆向编程apk,exe,pyc等
6:外挂插件开发
7:网站/服务器建设开发,漏洞维修

material机器人(请回复数字)
具体情况请找开发者！qq:412905523
不知道机器人回复规则请回复：命令
@我(艾特我)可以和我尬聊
官方总群:664808953
                                ''')

if __name__ == '__main__':
    RunBot(['-q', '2758678389'])