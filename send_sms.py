from twilio.rest import Client

account_sid = 'ACd86d53f26588561850a3a05e4d8a0b3f'
auth_token = 'cf96bf053df18c82554813098b8d67e2'
client = Client(account_sid, auth_token)

def send_sms(to, message):
    try:
        message = client.messages.create(
            body=message,
            from_='+17755877484',  # Замените вашим Twilio номером
            to=to
        )
        print(f"Сообщение отправлено! SID: {message.sid}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

# Пример отправки SMS
send_sms('+48436519415', 'hello world')
