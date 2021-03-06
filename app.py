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

line_bot_api = LineBotApi('hOpipJgVE+szrxrmr8+antqwQI6YRZVXNFgCwngIX88YG8CCLnD7slPBx/MG03XavzCS3eyf7zsq3nsq2sFMkR9du4SllmoIq8qJrjrngFsNYXTGy0vD3EUrDq92VUV3jb3shbm5M9aN8x8Q6I2T0gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dc77f5c8ff79b8ea908619ef2f17051c')


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
    r = "Excuse me, I don't understand"
    if 'give me a photo' in msg:
        sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', 'Hi']:
        r = 'Hello'
    elif msg == 'Have you eaten':
        r = 'Not yet'
    elif msg == 'Who are you?':
        r = 'I am a Robot'
    elif 'booking' in msg:
        r = 'Do you want to book a table?'



    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()