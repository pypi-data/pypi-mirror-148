import requests

SEND_MESSAGE_FORMAT = "https://api.telegram.org/bot{0}/sendmessage"
PIN_MESSAGE_FORMAT = "https://api.telegram.org/bot{0}/pinchatmessage?chat_id={1}&message_id={2}&disable_web_page_preview=true"

def send_message(bot_token, chat_id, chat_message):
    print(chat_message)
    uri = SEND_MESSAGE_FORMAT.format(bot_token)
    res = requests.post(uri, data={'chat_id':chat_id, 'text': chat_message, 'disable_web_page_preview': True, 'parse_mode': 'markdown'})
    print(res)
    if res.ok:
        return res.json(), res.ok
    else:
        return None, res.ok

def pin_message(bot_token, chat_id, chat_message_id):
    uri = PIN_MESSAGE_FORMAT.format(bot_token, chat_id, chat_message_id)
    res = requests.get(uri)
    print(res)
    if res.ok:
        return res.json(), res.ok
    else:
        return None, res.ok

def send_and_pin_message(bot_token, chat_id, chat_message):
    retryCount = 0
    ok = False
    data = None
    while retryCount < 3 and not ok:
        data, ok = send_message(bot_token, chat_id, chat_message)
        retryCount += 1
    
    if not ok:
        raise Exception("failed to post message")
    
    retryCount = 0
    print(data)
    message_id = data['result']['message_id']
    data = None
    ok = False
    while retryCount < 3 and not ok:
        data, ok = pin_message(bot_token, chat_id, message_id)
        retryCount += 1
    
    if not ok:
        raise Exception("failed to pin")
