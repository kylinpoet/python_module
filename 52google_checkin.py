#coding = utf-8

import requests
##from urllib.parse import unquote
import json
urls = "https://s1.52google.cc"
login_url = urls + "/auth/login"
postdata = {
    'email':'kylinpoet@gmail.com',
    'passwd':'2222222x',
    'code':''
}

checkin_url =urls + "/user/checkin"
u_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Referer': urls + '/user',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
}


s = requests.session()
response = s.post(login_url, data = postdata,headers = u_headers,verify=False)
print(json.loads(response.text)['msg'])
u_Cookies = response.headers['Set-Cookie']

u_headers.update(Cookies=u_Cookies)

response = s.post(checkin_url, data = postdata,headers = u_headers,verify=False)
print(json.loads(response.text)['msg'])


