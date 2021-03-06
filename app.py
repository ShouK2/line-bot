from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('uLauZ+6yio7WOMVSN6eR6ZASr+7Ja7ztej66i24Uw8LVI67IgNuoGBzkIUxsR2eOJY6w7XkNu4ZXKCFsGLds6DIyU1h9uPnflyegN4ydc1mAqO0ncNqqfYj6Na4sSosVkw/uy5hAt9FFzwzS32JM6gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('08b5ccad2e497cfb3bb47d11b0d24e1d')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '抱歉 你在說什麼？'
    
    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你是誰':
        r = 'I Am Robot'
    elif msg == '訂位':
       r = '你需要訂位嗎？'     	
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()