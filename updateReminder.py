#-*- codeing = utf-8 -*-
#@Time : 2021/8/26 9:33
#@Author : robin
#@File : remind.py
#@Software : PyCharm

'''
    从高三结束一直在追《万古神帝》一书，奈何作者飞天鱼更新实在太慢，时间还不定，
    （我都研一了还在更新）就导致每天都要时不时的去浏览器查看是否更新了，搞得我很焦灼，正好最近在学爬虫，
    就让爬虫替我去查看吧，如果更新了就发邮件提醒我。
    由于还没钱买服务器，就暂且让他运行在本地吧！
    用pyinstaller -F -W xx.py打包成可执行文件，放到win10的自启动文件夹下（shell:startup）
'''
import time

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

UPDATE_URL = "https://www.ranwen8.com/modules/article/search.php?searchkey=%CD%F2%B9%C5%C9%F1%B5%DB&submit=%CB%D1%CB%F7"
ARTICLE_URL = "https://www.ranwen8.com/book/14677/48952092.html"
#48952092
#48949456

def main():
    global ARTICLE_URL
    while(True):
        html = askUrl(UPDATE_URL)
        link = getLink(html)
        if link != ARTICLE_URL:
            print("更新了，发送邮件提醒我")
            ret = sendMail(link)
            if ret:
                print("发送邮件成功")
            else:
                print("发送邮件失败")
        else:
            print("还在偷懒，没更新呢！")
        ARTICLE_URL = link
        time.sleep(14400)

def askUrl(url):
    '''
        功能
        askUrl(url): 获取网页源码
        参数
        url：目标网页地址
        返回值
        html: 目标网页源码
    '''
    html = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    session = requests.Session()
    response = session.get(url=url,headers=headers,verify=True)
    html = response.content.decode('gbk')
    #print(html)
    return html

def getLink(html):
    '''
        功能
        getLink(html): 获取更新网页中的最新更新链接
        参数
        html: 章节更新链接所在的网页源码
        返回值
        link: 最新更新链接
    '''
    link = ""
    bs = BeautifulSoup(html,"html.parser")
    #print(html)
    table = bs.select(".grid")[0]
    alink = table.find_all('a')[1]
    link = alink['href']
    return link

def sendMail(link):
    '''
        功能
        sendMain():发送更新邮件通知更新
        参数
        link: 最新章节链接
        返回值
        ret: 布尔值，发送成功返回True，发送失败返回False
    '''
    ret = True
    myAccount = ''#发送者邮箱
    myKey = ''#发送者授权码，qq邮箱先设置然后获取
    toAccount = ''#目标邮箱

    try:
        msgStr = "万古神帝已经更新，<a href="+str(link)+">点击链接查看最新章节</a>"
        print(msgStr)
        #封装发送头部
        msg = MIMEText(msgStr,"html","utf-8")#因为有链接，所以发送html格式，纯文本用plain
        msg['From'] = formataddr(['凌寒',myAccount])
        msg['To'] = formataddr(['小熊',toAccount])
        msg['Subject'] = '万古神帝更新'

        server = smtplib.SMTP_SSL('smtp.qq.com',465)#填写发送服务器以及端口
        server.login(myAccount,myKey)#用账户和口令登录邮箱
        server.sendmail(myAccount,[toAccount],msg.as_string())#发送邮箱
        server.quit()
    except Exception as e:
        print(e)
        ret = False

    return ret

if __name__ == '__main__':
    main()
