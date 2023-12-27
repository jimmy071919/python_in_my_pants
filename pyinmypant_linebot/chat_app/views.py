#這邊是用來存放 urls.py中會使用到的函數的地方

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import requests
from lxml import etree

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
user_id = 'Uaa22ec86541cbdfd2210e8dcdaa52b0d'
#用於讀取LINEBOT的token以及secret

@csrf_exempt
def callback(request):   #建立callback函數
    line_bot_api.push_message(user_id, TextSendMessage(text=f"嗨"))
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        #用於判斷有無取用linebot成功

        for event in events:
            try :
                if  "目前價格" in event.message.text :
                    with open('num.txt','r') as f:
                        num = f.read()
                    price = get_stock_price(num)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=price))

                if "設定" in event.message.text :
                    num = extract_numbers_from_string(event.message.text)
                    setnum(num)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已設定"))
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入正確的股票代號"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
        #用於將所讀入的訊息以文字傳回 
    
def get_stock_price(num):

    url = f'https://tw.stock.yahoo.com/quote/{num}.TW'
    anti_UA = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36 Edg/115.0.0.0'
    }
    response = requests.get(url, headers=anti_UA).text
    tree = etree.HTML(response)
    price = tree.xpath('//div[1]/div[2]/div[1]/div[1]/span[1]/text()')
    print(price)
    return price[0]  # 這只是一個示例，請替換為實際的價格

def extract_numbers_from_string(input_string):
    x = [int(char) for char in input_string if char.isdigit()]
    x = ''.join(map(str, x))
    return x

def setnum(num):
    with open('num.txt','w') as f:
        f.write(num)
    return num
        