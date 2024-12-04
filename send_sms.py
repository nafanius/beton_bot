from twilio.rest import Client

account_sid = 'AC7aefd964e013aa84e02dde068682ca23'
auth_token = 'b78b21e2eaf5a7df2af171022a73f383'
client = Client(account_sid, auth_token)

def send_sms(to, message):
    try:
        message = client.messages.create(
            body=message,
            from_='+16814484273',  # Замените вашим Twilio номером
            to=to
        )
        print(f"Сообщение отправлено! SID: {message.sid}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

# Пример отправки SMS
send_sms('+48436519415', 'hello world')

# import requests
#
# resp = requests.post('https://textbelt.com/text', {
#   'phone': '48436519415',
#   'message': 'Hello world',
#   'key': 'textbelt',
# })
# print(resp.json())