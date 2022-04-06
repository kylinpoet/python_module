#coding=UTF-8
from telegram.client import Telegram
import re,time

tg = Telegram(
    api_id='xxx',
    api_hash='xxx',
    phone='xxx',  # you can pass 'bot_token' instead
    database_encryption_key='xxx',
    library_path='xxx',
    #tdlib_verbosity=4,
)
tg.login()


def send_verification_code(update):
    # 所有的新消息都会被监听，增加判断只监听自己感兴趣的
    if 1429576125 == update['message']['chat_id']:
        # 提取问题并且计算
        if "text" in update['message']['content']:
            question1 = update['message']['content']['text']['text']
            print("终点站:",question1)
            a = re.findall(r"\s\s(.+?)\+", question1, re.M)
            b = re.findall(r"\+(.+?)=", question1, re.M)
            if a and b:
                #print("终点站:",a, b)
                c = int(a[-1].strip()) + int(b[-1].strip())
                answers = update['message']['reply_markup']['rows'][0]
                print("终点站:",f'{a} + {b} = {c}')
                # 用答案和内联键盘值做匹配，一旦匹配执行按钮点击效果
                for answer in answers:
                    print("终点站:",f'答案项：{answer["text"]}')
                    if int(answer['text']) == c:
                        payload = {
                            '@type': 'callbackQueryPayloadData',
                            'data': answer['type']['data'],  ##每一个内联键盘都带有data数据
                        }
                        # 发送答案（点击内联键盘）
                        result = tg.call_method(method_name='getCallbackQueryAnswer',
                                                params={'chat_id': update['message']['chat_id'],
                                                        'message_id': update['message']['id'], 'payload': payload})
                        result.wait()
                        if result.error:
                            print(f'getCallbackQueryAnswer error: {result.error_info}')
                        else:
                            print(f'getCallbackQueryAnswer: {result.update}')
    if 1260610044 == update['message']['chat_id']:
        # 提取问题并且计算
        if "text" in update['message']['content']:
            question2 = update['message']['content']['text']['text']
            print("卷毛鼠:",question2)
            uptest = re.findall(r"\w{1,3}", question2, re.M|re.U)
            if len(uptest) > 6:
                #print("卷毛鼠:",uptest)
                a = uptest[7]
                #print("卷毛鼠a:",a)
                b = uptest[9]
                #print("卷毛鼠b:",b)
                d = uptest[8]
                print("卷毛鼠d:",d)
                if a and b:
                    #print("卷毛鼠:",a, b)
                    if d == "加上":
                        #print("这是加法")
                        c = int(a.strip()) + int(b.strip())
                    elif d == "减去":
                        #print("这是减法")
                        c = int(a.strip()) - int(b.strip())
                    elif d == "乘以":
                        #print("这是乘法")
                        c = int(a.strip()) * int(b.strip())
                    else :
                        #print("这是除法")
                        c = int(a.strip()) / int(b.strip())
                    answers = update['message']['reply_markup']['rows'][0]
                    print("卷毛鼠:",f'{a} {d} {b} = {c}')
                    # 用答案和内联键盘值做匹配，一旦匹配执行按钮点击效果
                    for answer in answers:
                        print("卷毛鼠:",f'答案项：{answer["text"]}')
                        if int(answer['text']) == c:
                            payload = {
                                '@type': 'callbackQueryPayloadData',
                                'data': answer['type']['data'],  ##每一个内联键盘都带有data数据
                            }
                            # 发送答案（点击内联键盘）
                            result = tg.call_method(method_name='getCallbackQueryAnswer',
                                                    params={'chat_id': update['message']['chat_id'],
                                                            'message_id': update['message']['id'], 'payload': payload})
                            result.wait()
                            if result.error:
                                print(f'getCallbackQueryAnswer error: {result.error_info}')
                            else:
                                print(f'getCallbackQueryAnswer: {result.update}')

tg.add_update_handler('updateNewMessage', send_verification_code)

#终点站 签到发送
print(f'终点站:签到信息发送中')
result = tg.send_message(
    chat_id=1429576125, 
    text="/checkin",
)

time.sleep(2)

#卷毛鼠 签到发送
print(f'卷毛鼠:签到信息发送中')
result = tg.send_message(
    chat_id=1260610044, 
    text="/checkin",
)


result.wait()
print(f'等待接收签到验证信息')
time.sleep(15)
tg.stop()