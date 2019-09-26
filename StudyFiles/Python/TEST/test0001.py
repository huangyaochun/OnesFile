# -*- coding: utf-8 -*-

import time

file_path = r'c:/Users/52702/Desktop/test/test0001.txt'
fp = open(file_path,'a')
fp.write('\n' + str('x') + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + '\n') 
fp.close()