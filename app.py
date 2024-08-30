from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

SOURCE_URL_PREFIX = os.environ['SOURCE_URL_PREFIX']
TARGET_URL_PREFIX = os.environ['TARGET_URL_PREFIX']
URL_SUFFIX = os.environ['URL_SUFFIX']
RESPONSE_MESSAGE_TEMPLATE = os.environ['RESPONSE_MESSAGE_TEMPLATE']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error: {e}")
        abort(400)

    return 'OK'

@app.route("/")
def hello():
    return "ↀᴥↀ"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text.startswith(SOURCE_URL_PREFIX) and text.endswith(URL_SUFFIX):
        converted_url = convert_url(text)
        response_message = RESPONSE_MESSAGE_TEMPLATE.format(url=converted_url)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message)
        )

def convert_url(url):
    url_core = url[len(SOURCE_URL_PREFIX):-len(URL_SUFFIX)]
    return TARGET_URL_PREFIX + url_core + URL_SUFFIX

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
