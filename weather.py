import json, requests
import datetime
from auth_data import token_weather


APPID = token_weather
lat = '52.16513438358974'
lon = '21.074802717769806'
cnt = 3


def weather_now():
    url_now = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APPID}&units=metric"
    response_now = requests.get(url_now)
    response_now.raise_for_status()
    weather_now = json.loads(response_now.text)

    # return      weather_now
    return    {'температура':weather_now['main']['temp'],
                    'облачность':weather_now['weather'][0]['description'],
                    'ветер':weather_now['wind']['speed'],
                    'восход':datetime.datetime.fromtimestamp(weather_now['sys']['sunrise']).strftime('%H:%M:%S'),
                    'заход':datetime.datetime.fromtimestamp(weather_now['sys']['sunset']).strftime('%H:%M:%S')
               }


def weather_3day():
    forecast_3day = []
    url_3days = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={cnt}&lang=ru&appid={APPID}&units=metric"
    response_3day = requests.get(url_3days)
    response_3day.raise_for_status()
    weather_3day = json.loads(response_3day.text)['list']
    for w in weather_3day:
        forecast = {'температура минимальная':w['main']['temp_min'],
                    'температура максимальная':w['main']['temp_max'],
                    'temp':w['main']['feels_like'],
                    'облачность':w['weather'][0]['description'],
                    'ветер':w['wind']['speed']}

        forecast_3day.append(forecast)


    return forecast_3day


# url_3days = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={cnt}&lang=ru&appid={APPID}&units=metric"
# response_3day = requests.get(url_3days)
# response_3day.raise_for_status()
# weather_3day = json.loads(response_3day.text)['list']
# print(weather_3day[0])
#
#
# print(weather_3day())
#
# print(weather_now())
#
