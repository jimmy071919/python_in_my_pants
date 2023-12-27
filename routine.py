import requests
from lxml import etree
import time
import schedule 
from linebot import LineBotApi
from linebot.models import TextSendMessage

#----------------------------------------Line token--------------------------------------------
LINE_CHANNEL_ACCESS_TOKEN = '5hJrIFYru2vIfeLWSzOwCorpzLRa+MdaSi6FYLtrLiWIhHuyJzmD5XBGLxt0/6R8zmBJrKdBzDVl5FbcHJfHEIr1nX0dEGggjBBTT1oL+ppkKshLmEifWJFvaBL90BAVYoSQ3Mn8xKRKAp4tsWM1AgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '2d1a5a0d69dfb380db22308ec4aed505'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

user_id = 'Uaa22ec86541cbdfd2210e8dcdaa52b0d'
#------------------------------------------------------------------------------------
url = 'https://tw.stock.yahoo.com/quote/0050.TW'
anti_UA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36 Edg/115.0.0.0'
}


def get_stock_price():
    response = requests.get(url, headers=anti_UA).text
    tree = etree.HTML(response)

    price = tree.xpath('//div[1]/div[2]/div[1]/div[1]/span[1]/text()')

    price = float(price[0])  # Convert string to float and remove commas
    #print(price)
    return price

def notify_user(price, threshold):
    if price > threshold:
        line_bot_api.push_message(user_id, TextSendMessage(text=f"股價達到 {price}，超過閾值 {threshold}，請注意！"))
        # 在這裡可以加入通知的程式碼，例如發送郵件或推送通知

def check_stock():
    threshold_price = 100.00  # 設定觸發通知的價格閾值

    current_price = get_stock_price()
    print(f"當前股價為: {current_price}")
    notify_user(current_price, threshold_price)

def main():
    check_stock()
    # 設定每小時檢查一次股價
    schedule.every(30).minutes.do(check_stock)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    main()
