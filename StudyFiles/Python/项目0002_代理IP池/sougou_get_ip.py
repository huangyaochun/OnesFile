#!/usr/bin/env python
#coding:utf-8 
#nohup python -u sogou_get_ip.py > nohup2.log 2>&1 &
'''
*****获取有效ip代理
'''

import sys
import os
import time
import datetime
import urllib
import urllib2
import requests
import random
import json
import commands
import threading
import re
import gzip
from StringIO import StringIO
reload(sys)
sys.setdefaultencoding("utf-8")
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
    
def getConn():
    connList=[
    ['http://v2ex.com','>登录</a>'],
    ['http://www.baidu.com/','>登录</a>'],
    ['http://pic.sogou.com/','图说新闻'],
    ['http://e.baidu.com/','>登录</a>'],
    ['http://e.baidu.com/product/','图说新闻']
    ]
    connapi = random.choice(connList)
    return connapi

class Conn:
    def port_conn(self,url):
        self.url = url
        fails = 0 
        while fails < 3:
            try:
                user_agent = '%s' % getUA()
                header = { 'User-Agent' : user_agent }
                req = urllib2.Request(self.url,headers=header)
                req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
                req.add_header("Connection", "keep-alive")
                rd = urllib2.urlopen(req, timeout=10)    #设置超时时间
                data = rd.read()
                break
            except: 
                fails += 1
                data = '网络连接出现问题'
                print '网络连接出现问题, 正在尝试再次请求: ', fails 
        return data
        
    def check_proxies(self,url): #检测代理存活率
        self.url = url
        proxies={'https': ''+ self.url +''}
        proxie={'http': ''+ self.url +''}
        fails = 0
        while fails < 2:
            try:
                connapi = getConn()
                r0 = requests.get(url=connapi[0], proxies=proxies,timeout=30,verify=False)
                r1 = requests.get(url=connapi[0], proxies=proxies,timeout=30,verify=False)
                if (r0.status_code == requests.codes.ok and connapi[1] in r0.content) or (r1.status_code == requests.codes.ok and connapi[1] in r1.content):
                    return True
                    break
                else:
                    return False
            except Exception, e:
                fails += 1
                pass
                return False
    def check_proxies2(self,url):
        return True
                
class MyThread(threading.Thread):#自定义线程类
    def __init__(self,ip,post ):
        threading.Thread.__init__(self) #在init中要先初始化Thread，然后在给参数赋值，不能少这个，不然会报thread.__init__() not called
        self.ip = ip
        self.post = post
        self.conn = Conn()
        self.exitcode = 0 #线程正常退出时该值为0，非正常退出时该值为1
        self.sumcode = 0  #统计数据

    def run(self):
        try:
            ip = self.ip
            post = self.post
            # url = 'http://web.chacuo.net/netproxycheck/?data='+ip+'&type=proxycheck&arg=p='+post+'_t=1_o=3'
            url = 'http://'+ip+':'+post+''
            wds = self.conn.check_proxies(url)
            if wds:
                outputfile.write(ip + ':' + post + '\r\n')
                self.sumcode = 1
            else:
                errorfile.write(ip + ':' + post + '\r\n')
        except Exception,e:
            print e 
            self.exitcode = 1
            
if __name__=='__main__':
    try:
        starttime = datetime.datetime.now()
        bg = time.localtime().tm_min 
        # outputfile = open('proxy_ip_pool.txt5','w') 
        # errorfile = open('eproxy_ip_pool.txt5','w')
        outputfile = open('/data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt5','w') 
        errorfile = open('/data1/user-data/huangyaochun/sogou/baidu_crawl/eproxy_ip_pool.txt5','w')
        conn = Conn()
        sumn = []
        n = 0 
        while True:
            n = n + 1 
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次爬取ip'
            urls = [
            ['http://www.66ip.cn/mo.php?sxb=&tqsl=300&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=','0'],
            ['http://www.66ip.cn/nmtq.php?getnum=500&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip','0'],
            ['http://www.xicidaili.com/nn/','1'],
            ['http://www.xicidaili.com/nn/2','1'],
            # ['http://www.xicidaili.com/nn/3','1'],
            # ['http://www.ip3366.net/free/','1'],
            ['http://www.89ip.cn/apijk/?&tqsl=500&sxa=&sxb=&tta=&ports=&ktip=&cf=1','0'],
            ['http://www.kuaidaili.com/free/inha/','2'],
            ['http://www.kuaidaili.com/free/inha/2/','1'],
            ['http://www.kuaidaili.com/free/inha/3/','1'],
            ['http://www.kuaidaili.com/free/inha/4/','1'],
            ['http://www.kuaidaili.com/free/inha/5/','1'],
            # ['http://www.kuaidaili.com/free/inha/6/','1'],
            ['http://www.kuaidaili.com/free/intr/','2'],
            ['http://www.kuaidaili.com/free/intr/2/','2'],
            ['http://www.kuaidaili.com/free/intr/3/','2'],
            # ['http://www.kuaidaili.com/free/intr/4/','2'],
            # ['http://www.kuaidaili.com/free/intr/5/','2'],
            # ['http://www.kuaidaili.com/free/intr/6/','2'],
            ['http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10','3']]
            patterns = []
            for urli in urls:
                try:
                    url = urli[0]
                    i = urli[1]
                    data = conn.port_conn(url)
                    if i == '3': #接口数据
                        searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                        data = searchjson.group()
                        encodedjson=json.loads(data)
                        ips = encodedjson["RESULT"]["rows"]
                        ipsnum = len(ips)
                        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次'+str(urli)+'爬取ip的ip量：' + str(ipsnum)
                        for ip_p in ips:
                            patterns.append((ip_p["ip"].encode('utf-8'),ip_p["port"].encode('utf-8')))
                    else: #页面数据
                        pattern = re.findall(r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,5})',data)
                        pattern66 = re.findall(r'((?:\d{1,3}\.){1,3}\d{1,3}):([1-9]\d*)',data)
                        if len(pattern)>=5:
                            # print data[1000:2500]
                            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次'+str(urli)+'爬取ip的ip量：' + str(len(pattern))
                            patterns = patterns + pattern
                        elif len(pattern66)>=5:
                            # print data[1000:2500]
                            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次'+str(urli)+'爬取ip的ip量：' + str(len(pattern66))
                            patterns = patterns + pattern66
                        else:
                            try:
                                buf = StringIO(data)
                                f = gzip.GzipFile(fileobj=buf)
                                response = f.read()
                                pattern = re.findall(r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})',response)
                                # print response[1000:2500]
                                print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次'+str(urli)+'爬取ip的ip量：' + str(len(pattern))
                                patterns = patterns + pattern
                            except:
                                print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次异常data：' + str(urli) + str(data)
                except Exception,e:
                    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次异常连接：' + str(urli)
                    print e

            patterns_ip = list(set(patterns))
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -- 第'+str(n)+'次爬取ip的ip量：' + str(len(patterns_ip))
            patterns_num = [tuple(patterns_ip[i:i+350]) for i in range(0,len(patterns_ip),350)]
            for patterns in patterns_num:
                maxT = []
                threads = []       
                for ips in patterns:
                    threads.append(MyThread(ips[0],ips[1])) 
                for i in threads:
                    i.start()
                for t in threads:
                    t.join()
                 
                for t in threads:#检查线程执行时是否发生异常
                    if t.exitcode==1:
                        print t.ip,t.post,t.exitcode,"~~~线程真异常"
                        raise Exception(str(t.ip)+":" + str(t.post) + "~~~线程异常")
                    if t.sumcode != 0 :   
                        maxT.append(t.sumcode)
                wds = sum(maxT)
                print "共运行线程数："+str(len(threads))+"\t 可用ip量："+str(wds)
                sumn.append(wds)
            sumip = sum(sumn)
            if sumip >= 500:
                break
        print "可用ip量数：" + str(sumip)
        outputfile.close()
        errorfile.close()
        # os.system("sort proxy_ip_pool.txt5 |uniq  > proxy_ip_pool.txt6")
        try:
            num_s = int(commands.getstatusoutput("wc -l /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt")[1].split(' ')[0])
        except:
            num_s = 0
        if (int(time.localtime().tm_hour)%2 == 0 and bg <=5 ) or num_s<300:
            #每隔4个小时重新抓取一次
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt5 |uniq  >  /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt6")
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt5 |uniq  >  /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt3")
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt6|uniq -D >> /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt3") 
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt3|uniq -u > /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt")
        else:
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt5 |uniq  >>  /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt6")
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt5 |uniq  >  /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt3")
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt6|uniq -D >> /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt3") 
            os.system("sort /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt3|uniq -u > /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt")
        num_b = int(commands.getstatusoutput("wc -l /data1/user-data/huangyaochun/sogou/baidu_crawl/proxy_ip_pool.txt")[1].split(' ')[0])
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" -- 本次ip文件入库量：" + str(num_b)
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" -- 本次共执行 "+ str((datetime.datetime.now() - starttime).seconds) +" 秒\r\n"       
    except Exception,e:
            print e 
