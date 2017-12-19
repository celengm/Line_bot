#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from datetime import datetime

#一般與其他API連線所需
import urllib3
import logging

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

#from FlaskApp import app
app = Flask(__name__)

#Line訊息API的所需參數
LINE_CHANNEL_ACCESS_TOKEN = "5IDk9+6UJ9EeEDRq1gn5q0jdRRdYW6Bw5HSbJ3WrzBCty7QeYYZebNF29vXlT+NOfMB0XQCN+QcqGhljRKdihkupgfP9qm9vs4+wmZRr/geWRBV32deYoCCGd5mBEB3zlu4Z1qWDvSFJ8OmsSkYoLAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "f43ae5e01e836c209010771daea3da20"
NEWLINE = "\n"

#Line訊息API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)





#被Line Message API呼叫運作
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value 回覆所需的簽章(會不斷變換)
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body 處理webhook事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def stauts(st):
	response = urllib2.urlopen('http://120.105.129.29/appliances/appliances.php?relay=1')
	#print ('response of json :')
	responseJson = response.read()
	#回傳後事物件所以要用READ讀取內容
	decode = json.loads(responseJson)
	if st==2:
		relay = decode["Relay_status"]
			if relay == 'Y':
				return 'Y'
			else
				return 'N'
	elif st==1:
		relay = decode["Fan_status"]
			if relay == 'X':
				return 'Y'
			else
				return 'N'
				

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    app.logger.info("user sent to line bot message: " + msg)
    msg = msg.encode('utf-8')
    if "開關" in msg:
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="是要開還是關？"))
    if "開" in msg:
		if "扇" in msg:
			http = urllib3.PoolManager()
			r = http.request('GET', 'http://120.105.129.29/appliances/appliances.php?Fan_status=%27X%27')
			#line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開啟電風扇成功 連線狀況:"+str(r.status)))
			st=1
			if(stauts(st)=='Y'):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開啟電風扇成功 連線狀況:"+str(r.status)))
			else
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開啟電風扇失敗 連線狀況:"+str(r.status)))
		elif "燈" in msg:
			http = urllib3.PoolManager()
			r = http.request('GET', 'http://120.105.129.29/appliances/appliances.php?relaystatus=%27Y%27')
			#line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開啟電燈成功 連線狀況:"+str(r.status)))
			st=2
			if(stauts(st)=='Y'):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開啟電燈成功 連線狀況:"+str(r.status)))
			else
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開啟電燈失敗 連線狀況:"+str(r.status)))
		else:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請說明要開啟的物件名稱 可選擇電風扇或電燈"))
			
    if "關" in msg:
		if "扇" in msg:
			http = urllib3.PoolManager()
			r = http.request('GET', 'http://120.105.129.29/appliances/appliances.php?Fan_status=%27O%27')
			#line_bot_api.reply_message(event.reply_token,TextSendMessage(text="關閉電風扇成功 連線狀況:"+str(r.status)))
			st=1
			if(stauts(st)=='N'):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="關閉電風扇成功 連線狀況:"+str(r.status)))
			else
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="關閉電風扇失敗 連線狀況:"+str(r.status)))
		elif "燈" in msg:
			http = urllib3.PoolManager()
			r = http.request('GET', 'http://120.105.129.29/appliances/appliances.php?relaystatus=%27N%27')
			#line_bot_api.reply_message(event.reply_token,TextSendMessage(text="關閉電燈成功 連線狀況:"+str(r.status)))
			st=2
			if(stauts(st)=='N'):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="關閉電燈成功 連線狀況:"+str(r.status)))
			else
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="關閉電燈失敗 連線狀況:"+str(r.status)))
		else:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請說明要關閉的物件名稱 可選擇電風扇或電燈"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    
@app.route('/test')
def lineBotTest():
    indexString = u'lineBot for 301 home server functional 運作成功'
    return indexString.encode('utf-8')

if __name__ == '__main__':
    app.debug = True
    app.logger.setLevel(logging.INFO)
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run()

