# -*- coding: utf-8 -*-
import random
import time
import tweetpony
import urllib2
import json

from config import config


def fetch(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()


def get_json():
    return json.loads(fetch("http://weather.spychalski.info/api.php"))


def main():
    api = tweetpony.API(consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'],
                        access_token=config['access_token'], access_token_secret=config['access_token_secret'])

    # noinspection PyStatementEffect
    api.user

    weather_data = get_json()

    temperature = int(round(float(weather_data['Temperature'])))
    humidity = int(round(float(weather_data['Humidity'])))
    pressure = int(round(float(weather_data['Pressure'])))

    try:

        # print weather_data

        message_type = 1

        current_hour = int(time.strftime("%H"))

        if current_hour >= 6 and current_hour <= 10:
            message_type = 2
        elif current_hour >= 19 and current_hour <= 23:
            message_type = 3

        text = ''

        if message_type == 1:
            text = u'Witaj Szczecinie, mamy ' + unicode(str(temperature)) + u'C i ' + unicode(
                str(humidity)) + u'% wilgotności. Ciśnienie wynosi ' + unicode(str(pressure)) + 'hPa #szczecin #pogoda'
        elif message_type == 2:
            text = u'Prognoza na dziś: ' + unicode(
                str(int(round(float(weather_data['Forecast'][0]['TempDay']))))) + u'C, ciśnienie ' + \
                   unicode(str(pressure)) + u'hPa, wiatr ' + unicode(
                str(int(round(float(weather_data['Forecast'][0]['WindSpeed']))))) + u'm/s, '

            rain = float(weather_data['Forecast'][0]['Rain'])
            snow = float(weather_data['Forecast'][0]['Snow'])

            if rain > 0 and snow == 0:
                text += u'będzie padać'
            elif rain == 0 and snow > 0:
                text += u'będzie padać śnieg'
            elif rain > 0 and snow > 0:
                text += u'będzie padać śnieg z deszczem'
            else:
                text += u'brak opadów'

            text += ' #pogoda #szczecin'
        elif message_type == 3:
            text = u'Prognoza na jutro: ' + unicode(
                str(int(round(float(weather_data['Forecast'][1]['TempDay']))))) + u'C, ciśnienie ' + \
                   unicode(str(pressure)) + u'hPa, wiatr ' + unicode(
                str(int(round(float(weather_data['Forecast'][1]['WindSpeed']))))) + u'm/s, '

            rain = float(weather_data['Forecast'][1]['Rain'])
            snow = float(weather_data['Forecast'][1]['Snow'])

            if rain > 0 and snow == 0:
                text += u'będzie padać'
            elif rain == 0 and snow > 0:
                text += u'będzie padać śnieg'
            elif rain > 0 and snow > 0:
                text += u'będzie padać śnieg z deszczem'
            else:
                text += u'brak opadów'

            text += ' #pogoda #szczecin'

        # print text
        api.update_status(status=text)
    except tweetpony.APIError as err:
        print "Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description)
    else:
        print "Yay! Your tweet has been sent!"


if __name__ == "__main__":
    main()
