#!/usr/bin/python
#coding=utf-8
'''
Created on 2019-7-26
@author: Administrator
验证ip地址，访问 #http://172.16.71.246:8080/login
情景：只知道端口，和ip段，查找有效地址
'''

import threading,subprocess
from time import ctime,sleep,time
import Queue

queue=Queue.Queue()

class ThreadUrl(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
    def run(self):
        while True:
            host=self.queue.get()
            # ret=subprocess.call('ping -n 1 -w 1 '+host,shell=True,stdout=open('F:\Eclipse\logs_parse\ipsear.log','a'))
            # ret=subprocess.Popen('ping -n 1 -w 1 '+host, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ret=subprocess.Popen('tcping -n 1 '+host+' 8080', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            sout = ret.communicate()[0]
            stdout.write(sout.replace('\r\n','\t').replace('\n','\t') +'\n')
            if '1 successful' in sout:
                print sout
            self.queue.task_done()

def main():
    for i in range(100):
        t=ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    for host in b:
        queue.put(host)
    queue.join()


if __name__ == '__main__':
    b=['172.16.71.'+str(x) for x in range(1,256)] #ping 172.16.71 网段
    stdout=open('F:\Eclipse\logs_parse\ipsear.log','a')
    start=time()
    main()
    stdout.close()
    print "Elasped Time:%s" % (time()-start)

 