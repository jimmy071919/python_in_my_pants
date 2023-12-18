#這邊是用來存放 urls.py中會使用到的函數的地方

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
#用於讀取LINEBOT的token以及secret


@csrf_exempt
def callback(request):   #建立callback函數
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
            if isinstance(event, MessageEvent):
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text)
)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
        #用於將所讀入的訊息以文字傳回 

