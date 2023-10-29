from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from crawler import crawler

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('zX76+KBtn8rnoNpuRGANkfFaGzaoGdVrgaAAU2KQoOJ1rIgNr2OHeV6Q7YVX3YTj6CYD9N+w1K010HmTL9FKoRKLFL0gEVTA9Sc+VASenDsGC1FaIf79r1lkfkaZuZip143Rw3fkq9aUNpena1BlbgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f29bbe236b8fa276af6064f1a7d46cf1')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    if "資訊" == event.message.text:
        DcardCrawl = crawler()
        result = DcardCrawl.infomation
    elif "找電影" == event.message.text:
        name = event.message.text
        MovieCrawl = crawler()
        result = MovieCrawl.crawl_movie_types(name)
    elif "評分電影" == event.message.text:
        name = event.message.text
        MovieCrawl = crawler()
        result = MovieCrawl.crawl_movie_types(name)
    elif "股票" in event.message.text:
        StockCrawl = crawler()
        name = event.message.text[2:]
        result = StockCrawl.crawl_stock(name)
    else:
        DcardCrawl = crawler()
        result = DcardCrawl.crawl_specific_forum(event.message.text)

    message = TextSendMessage(text=result)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
