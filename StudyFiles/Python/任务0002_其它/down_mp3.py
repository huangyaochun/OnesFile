#!/usr/bin/env python
#coding:utf-8
#--下载数据

import random
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

def getUA():
    uaList = [ 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.7.0.16013',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
    ]
    ua = random.choice(uaList)
    return ua
    
def UrlGetData(url): #get请求
    resg = "GET请求失败"
    HEADERS = {'ua': '%s' % getUA()}
    try:
        res = requests.get(url,headers=HEADERS,timeout=(3,60))
        res.encoding = 'gb2312'
        resg = res.text
    except:
        print "Get is fail!"
    return resg
    
def Url_Conn_down(url,title):
    j = 1
    while j<6:  #下载 请求错误时 重试5次
        try:
            HEADERS = {'ua': '%s' % getUA()}
            res = requests.get(url,headers=HEADERS,timeout=10) 
            music = res.content 
            wfile = r'temp/%s' % (title + '.mp3')
            with open(wfile, 'ab') as file: #保存到本地的文件名 
                file.write(res.content) 
                file.flush()
                file.close()
            resg = "下载成功 " + str(j)
            break
        except:
            resg = "下载失败 " + str(j)
            j += 1
            print "Down is fail!"
    return resg
    
def main_hmmsghls():
    #好妈妈胜过好老师的下载
    file = open('temp/好妈妈胜过好老师Readme.txt','w')
    for i in range(56): #56
        url = 'http://dt.baobao88.com/au_play.php?id=' + str(151669 - i)
        print url
        req = UrlGetData(url)
        urlmp3s = re.findall('http://play.baobao88.com/vbaobao88/.*?.mp3', req)
        urlmp3 = urlmp3s[0]
        title = str(i+1).zfill(2)+ urlmp3.split('/')[-2]
        #开始下载 
        res = Url_Conn_down(urlmp3,title)
        text = 'http://www.baobao88.com/youshen/yuer/09/28' + str(151669 - i)+'\t'+urlmp3+'\t'+title +'\t'+ res
        print text
        file.write(text + '\n')
    file.close()

if __name__=='__main__':
    main_hmmsghls()

