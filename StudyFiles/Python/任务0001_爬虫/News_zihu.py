import requests
from lxml import etree
import json

# get dictionary value
def get_dict_value(d,key):
    result = 'default'
    if isinstance(d,dict):
        if key in d.keys():
            result = d.get(key)
        else:
            for v in d.values():
                result = get_dict_value(v,key)
                if result != 'default':
                    break
    else:
        pass
    return result

# zhihu/billboard
url = 'https://www.zhihu.com/billboard'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'}
content = requests.get(url, headers = header).text
html = etree.HTML(content)
JData = html.xpath('//*[@id="js-initialData"]/text()')[0]
Data = json.loads(JData)
List = get_dict_value(Data,"hotList")
print len(List)
for i in List:
    Qid = get_dict_value(i,"cardId")
    AnswerCount = get_dict_value(i,"answerCount")
    Title = get_dict_value(i,"titleArea")["text"]
    Abstract = get_dict_value(i,"excerptArea")["text"]
    Metrics = get_dict_value(i,"metricsArea")["text"]
    Link = get_dict_value(i,"link")["url"]
    print Qid,AnswerCount,Title,Abstract,Metrics,Link 