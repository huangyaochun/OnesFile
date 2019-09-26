#!/usr/bin/env python
#coding:utf-8
'''
*****各大搜索推荐引擎接口,疾病库症状库药品库
baidu:  http://suggestion.baidu.com/su?wd=高血压&cb=window.baidu.sug
bing : http://api.bing.com/qsonhs.aspx?type=cb&q=高血压&cb=window.bing.sug
好搜(360) : https://sug.so.360.cn/suggest?encodein=utf-8&encodeout=utf-8&format=json&word=高血压&callback=window.so.sug
搜狗（Sogou） : https://www.sogou.com/suggnew/ajajjson?type=web&key=高血压
淘宝（Taobao）: https://suggest.taobao.com/sug?code=utf-8&q=高血压&callback=window.taobao.sug
有道 : http://sug.so.360.cn/suggest/word?callback=YD.updateCall&encodein=utf-8&encodeout=utf-8&word=高血压
中国yahoo: https://sg.search.yahoo.com/sugg/gossip/gossip-sg-ura/?f=1&.crumb=KWysoMMUhLM&output=sd1&command=高血压
360良医： http://sug.ly.haosou.com/suggest/word?callback=suggest_so&encodein=utf-8&encodeout=utf-8&word=高血压
sogou明医: http://mingyi.sogou.com/suggnew/english?key=高血压&type=medic&ori=yes&pr=medic&abtestid=7&ipn=
url = 'http://suggestion.baidu.com/su?wd=' + key + '&cb=window.baidu.sug'
hive -e "select distinct name FROM (SELECT distinct regexp_replace(name,'(^[　 ]*)|([　 ]*$)','') name FROM ixywy_new.zzk UNION ALL SELECT distinct regexp_replace(name,'(^[　 ]*)|([　 ]*$)','') name FROM ixywy_new.ill UNION ALL SELECT distinct regexp_replace(name,'(^[　 ]*)|([　 ]*$)','') name FROM yao_db.drug_common ) s " > zzk_jib_yao_keys.txt 
nohup python -u /home/hadoop/huangyaochun/python/sogou/sogou_api_keywords.py zzk_jib_yao_keys.txt > nohup.log 2>&1 &
scp /home/hadoop/huangyaochun/python/sogou/zzk_jib_yao_keys.txt 10.20.2.19:/home/hadoop/huangyaochun/sogou/
'''

import sys
import os
import datetime
import urllib
import urllib2
import json
import re
import random
reload(sys)
sys.setdefaultencoding("utf-8")
import threading

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

class Conn:
    def port_conn(self,url):
        fails = 0 
        self.url = url
        while fails < 5:
            try:
                req = urllib2.Request(self.url)
                req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
                req.add_header("Connection", "keep-alive")
                req.add_header("User-Agent", "%s" % getUA() )
                rd = urllib2.urlopen(req, timeout=5)    #设置超时时间
                data = rd.read()
                rd.close()
                break
            except: 
                fails += 1
                data = '网络连接出现问题'
                print '网络连接出现问题, 正在尝试再次请求: ', fails 
        return data

    def baidu_api(self,key):
        self.key = key
        url = 'http://suggestion.baidu.com/su?wd=' + self.key + '&cb=window.baidu.sug'
        wds = ''
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = data
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group().decode('GBK').encode('utf-8')
                search_wds = re.search( r's:\[(.*?)\]', data, re.M|re.I)
                search_wds = search_wds.group(1)
                wds = search_wds.replace('","',',')
        except Exception,e:
            print e 
        return wds.strip('"').split(',')
        
    def bing_api(self,key):
        self.key = key
        url = 'http://api.bing.com/qsonhs.aspx?type=cb&q=' + self.key + '&cb=window.bing.sug'
        wds = []
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = [data]
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group()
                encodedjson=json.loads(data)
                if "Results" in encodedjson["AS"]:
                    for i in range(len(encodedjson["AS"]["Results"])):
                        Suggests = encodedjson["AS"]["Results"][i]
                        for j in range(len(Suggests["Suggests"])):
                            wds.append(Suggests["Suggests"][j]["Txt"])
        except Exception,e:
            print e   
        return wds
        
    def haoso_api(self,key):
        self.key = key
        url = 'https://sug.so.360.cn/suggest?encodein=utf-8&encodeout=utf-8&format=json&word=' + self.key + '&callback=window.so.sug'
        wds = []
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = [data]
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group()
                encodedjson=json.loads(data)
                for i in range(len(encodedjson['result'])):
                    wds.append(encodedjson['result'][i]['word'])
        except Exception,e:
            print e  
        return wds

    def sogou_api(self,key):
        self.key = key
        url = 'https://www.sogou.com/suggnew/ajajjson?type=web&key=' + self.key + ''
        wds = []
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = [data]
            else:
                searchjson = re.search( r'\[(.*)\]', data, re.M|re.I)
                data = searchjson.group().decode('GBK').encode('utf-8')
                search_wds = eval(data)[1]
                for i in range(len(search_wds)):
                    wds.append(search_wds[i])
        except Exception,e:
            print e   
        return wds

    def taobao_api(self,key):
        self.key = key
        url = 'https://suggest.taobao.com/sug?code=utf-8&q=' + self.key + '&callback=window.taobao.sug'
        wds = []
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = [data]
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group()
                encodedjson=json.loads(data)
                for i in range(len(encodedjson['result'])):
                    wds.append(encodedjson['result'][i][0])
        except Exception,e:
            print e  
        return wds

    def youdao_api(self,key):
        self.key = key
        url = 'http://sug.so.360.cn/suggest/word?callback=YD.updateCall&encodein=utf-8&encodeout=utf-8&word=' + self.key + ''
        wds = ''
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = data
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group()
                search_wds = re.search( r's:\[(.*?)\]', data, re.M|re.I)
                search_wds = search_wds.group(1)
                wds = search_wds.replace('","',',')
        except Exception,e:
            print e 
        return wds.strip('"').split(',')

    def yahoo_api(self,key):
        self.key = key
        url = 'https://sg.search.yahoo.com/sugg/gossip/gossip-sg-ura/?f=1&.crumb=KWysoMMUhLM&output=sd1&command=' + self.key + ''
        wds = []
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = [data]
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group()
                encodedjson=json.loads(data)
                for i in range(len(encodedjson['r'])):
                    wds.append(encodedjson['r'][i]['k'])
        except Exception,e:
            print e  
        return wds

    def ly_api(self,key):
        self.key = key
        url = 'http://sug.ly.haosou.com/suggest/word?callback=suggest_so&encodein=utf-8&encodeout=utf-8&word=' + self.key + ''
        wds = ''
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = data
            else:
                searchjson = re.search( r'{(.*)}', data, re.M|re.I)
                data = searchjson.group()
                search_wds = re.search( r's:\[(.*?)\]', data, re.M|re.I)  
                search_wds = search_wds.group(1)
                wds = search_wds.replace('","',',')
        except Exception,e:
            print e 
        return wds.strip('"').split(',')

    def sogoumy_api(self,key):
        self.key = key
        url = 'http://mingyi.sogou.com/suggnew/english?key=' + self.key + '&type=medic&ori=yes&pr=medic&abtestid=7&ipn= '
        search_wds = []
        try:
            data = self.port_conn(url)
            if data == '网络连接出现问题':
                wds = [data]
            else:
                searchjson = re.search( r'\[(.*)\]', data, re.M|re.I)
                data = searchjson.group().decode('GBK').encode('utf-8')
                search_wds = eval(data)[1]
        except Exception,e:
            print e  
        return search_wds

    
class MyThread(threading.Thread):#自定义线程类
    def __init__(self,api,keyword,key ):
        threading.Thread.__init__(self) #在init中要先初始化Thread，然后在给参数赋值，不能少这个，不然会报thread.__init__() not called
        self.api = api
        self.keyword = keyword
        self.key = key
        self.conn = Conn()
        self.exitcode = 0 #线程正常退出时该值为0，非正常退出时该值为1

    def run(self):
        try:
            api = self.api
            keyword = self.keyword
            key = self.key
            wds = eval('self.conn.'+api)(key)

            if len(wds)>0:   
                for wd in wds:
                    if wd == '网络连接出现问题':
                        outerrorfile.write(keyword + "\t" + api  + "\n")
                    else:
                        output = keyword + "\t" + wd + "\t" + api 
                        print output
                        outputfile.write(output + "\n")
            else:
                output = keyword + "\t" + '' + "\t" + api
                outputfile.write(output + "\n")
        except Exception,e:
            print e 
            self.exitcode = 1

if __name__=='__main__':

    input = sys.argv[1]
    #keywords = ["高血压","嗳气时有腐败鸡蛋的气味","嗳气"]
    
    inputfile = open(input,'r')
    outputfile = open("sogou_api_keywords.txt",'w') 
    outerrorfile = open("sogou_error_keywords.txt",'w')
    starttimez = datetime.datetime.now()
    
    dict = []
    for keyword_all in inputfile:
        dict.append(keyword_all.strip())

    keywords_num = [tuple(dict[i:i+200]) for i in range(0,len(dict),200)]  #一次最多运行 200*9个线程

    for keywords in keywords_num:
        threads = []
        try:
            for keyword in keywords:
                keyword = keyword.strip()
                p = {'keyword': keyword}
                key = urllib.urlencode(p).replace('keyword=','')
                threads.append(MyThread("baidu_api",keyword,key))
                threads.append(MyThread("bing_api",keyword,key))       
                threads.append(MyThread("haoso_api",keyword,key))
                threads.append(MyThread("sogou_api",keyword,key))
                threads.append(MyThread("taobao_api",keyword,key))
                threads.append(MyThread("youdao_api",keyword,key))  
                threads.append(MyThread("yahoo_api",keyword,key))
                threads.append(MyThread("ly_api",keyword,key))  
                threads.append(MyThread("sogoumy_api",keyword,key))            

            for i in threads:
                i.start()
            for t in threads:
                t.join()
                
            for t in threads:#检查线程执行时是否发生异常
                if t.exitcode==1:
                    print t.api,t.keyword,t.exitcode,"~~~线程真异常"
                    raise Exception(str(t.api)+"\t" + str(t.keyword) + "~~~线程异常") 
            print "共运行线程数：",len(threads)
            print '共执行' + str((datetime.datetime.now() - starttimez).seconds) + '秒'
        except Exception,e:
                print e   
                    
    inputfile.close()
    outputfile.close()
    outerrorfile.close()
