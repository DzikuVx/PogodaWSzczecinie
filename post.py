# -*- coding: utf-8 -*-

import tweetpony
import os
import sqlite3
import urllib2
import json 

from config import config

def fetch(url):
    req = urllib2.Request(url)
    response=urllib2.urlopen(req)
    return response.read()

def getJSON():
	return json.loads(fetch("http://weather.spychalski.info/api.php"))

def main():
	api = tweetpony.API(consumer_key = config['consumer_key'], consumer_secret = config['consumer_secret'], access_token = config['access_token'], access_token_secret = config['access_token_secret'])
	user = api.user

	#conn = sqlite3.connect('/home/pi/WeatherStation/data.db')

	#cur = conn.cursor()
	#cur.execute('SELECT Temperature, Humidity FROM readouts_external ORDER BY `Date` DESC LIMIT 1')

	#data = cur.fetchone()

	#if data == None:
	#	exit()

	#conn.close()

	jData = getJSON()

	iTemp = int(round(jData['Temperature']))
	iHumidity = int(round(jData['Humidity']))
	iPressure = int(round(jData['Pressure']))

	try:

		text = u'Witaj Szczecinie, mamy ' + unicode(str(iTemp)) + u'C i ' + unicode(str(iHumidity)) + u'% wilgotności. Ciśnienie wynosi ' + unicode(str(iPressure)) + 'hPa #szczecin #pogoda'

		api.update_status(status = text)
	except tweetpony.APIError as err:
		print "Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description)
	else:
		print "Yay! Your tweet has been sent!"

if __name__ == "__main__":
	main()
