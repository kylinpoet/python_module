# coding:utf-8
import urllib.request
import urllib.parse

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://10.131.7.37/ac_portal/default/pc.html?tabs=pwd',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4'
}


# get取网页数据
def geturl(url, data={}):
    try:
        params = urllib.parse.urlencode(data).encode(encoding='UTF8')
        req = urllib.request.Request("%s?%s" % (url, params))
        # 设置headers
        for i in headers:
            req.add_header(i, headers[i])
        r = urllib.request.urlopen(req)
        html = r.read()
        return html
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))


# post取网页数据
def posturl(url, data={}):
    try:
        # params = urllib.parse.urlencode(data).encode(encoding='UTF8')
        params = data.encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        r = urllib.request.urlopen(req)
        html = r.read()
        return html
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))

postdata = {
    'opr': 'pwdLogin',
    'userName': '691740',
    'pwd': '22222x',
    'rememberPwd': 1
}

postdata = 'opr=pwdLogin&userName=691740&pwd=22222x&rememberPwd=1'
url = 'http://10.131.7.37/ac_portal/login.php'
retTemp = posturl(url, postdata)
print(retTemp.decode('utf-8'))