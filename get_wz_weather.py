# -*- coding:utf-8 -*-
# from bs4 import BeautifulSoup
import requests
import json
import setLogger
myLogger = setLogger.setLogger()
html_doc = """
测试数据
"""


def delextra(oldstr):
    return oldstr.replace('<br/>', '')

headers = {"Referer": "http://www.wz121.com", 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
url_wz121 = 'http://www.wz121.com/'
try:
    html_doc = requests.get(url_wz121, headers=headers)
    html_doc = html_doc.content.decode('utf-8')
    pass
except:
    myLogger.exception('网站访问错误')
# print(html_doc)
myindex_start = html_doc.find('<td align="left" height="20" width="240">')
print(myindex_start)
if myindex_start < 0: exit(2)
myindex_end = html_doc.find('</td>', myindex_start)
print(myindex_end)
len_myindex = len('<td align="left" height="20" width="240">')
weather_old = html_doc[myindex_start+len_myindex:myindex_end].replace(' ', '')
weather_old = weather_old.replace('\r\n', '')
weather_all = weather_old.split('<br/><br/>')
if len(weather_all) < 1: exit(3)
print(weather_all)
pre_weather = weather_all[0][0:weather_all[0].find('发布的')+3] + '天气预报:'
pre_weather = delextra(pre_weather)
for i in range(len(weather_all)):
    if weather_all[i].startswith('【温州市区和各县】'):
        break
today_weather = ''
if i == 2:
    today_weather = pre_weather + delextra(weather_all[1]) + delextra(weather_all[2])
elif i == 1:
    today_weather = pre_weather + delextra(weather_all[1])
else:
    exit(4)
print(today_weather)
try:
    dd_robot = 'https://oapi.dingtalk.com/robot/send?access_token=9d9effa6d1f5937b58bda96a2e94c62fc8a3afec10ea44ae7d02ea64812724c4'
    # dd_robot = 'https://oapi.dingtalk.com/robot/send?access_token=f05aaf9e63a1319629ca6078d5d10da8ab42521b11d263273270eb1f2b141ba4'
    weather_to_dd = {"msgtype": "text", "text": {"content": today_weather}}
    json_weather = json.dumps(weather_to_dd, ensure_ascii=False)
    print(json_weather)
    headers = {"Content-Type": "application/json"}
    # print(json.dumps(weather_to_dd))
    ret = requests.post(dd_robot, headers=headers, data=json_weather.encode())
    # print(ret.text)
except Exception as e:
    myLogger(e)
