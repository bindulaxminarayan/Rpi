'''
Retrieve the sunrise time from weather app for the next day and capture a pic

You can get the lat and lng https://gist.github.com/erichurst/7882666
Get sunrise time with lat and lng from http://sunrise-sunset.org/api
'''
import schedule
import time
import requests
import json
import logging
from datetime import datetime, timedelta
import picamera

logging.basicConfig(level=logging.DEBUG)

def getNextDate():
    '''
        None -> str
        Returns the next date related to the local time
    '''
    return (datetime.now() + timedelta(days = 1)).strftime('%Y-%m-%d')

def getSunRiseTime(lat, lng):
    '''
    (num, num) -> str
    Returns the sunrise time for a given latitude and longitude
    '''
    url = "http://api.sunrise-sunset.org/json"
    payload = {'lat': lat, 'lng': lng, 'date': getNextDate()}
    response = requests.get(url, params=payload)
    t = json.loads(response.text)
    return t['results']['sunrise'][:-6]

def convert_to_est(stime):
    '''
    datetime -> str
    Returns the hours and minutes in est time for a given utc time 
    '''
    stime = datetime.strptime(stime, '%Y-%m-%dT%H:%M:%S')
    est_time = stime + timedelta(hours = -4)
    #Write to file
    f = open("sunrisetimes.txt","a+")
    f.write(str(est_time)+"\n")
    f.close()
    return est_time.strftime('%H:%M')

def scheduleSunRiseTime():
    '''
    (num, num) -> None
    Schedule the job to take a picture
    '''
    lat = 42.282379
    lng = -71.436621
    utc_time = getSunRiseTime(lat, lng)
    sunrise_time = convert_to_est(utc_time)
    schedule.every().day.at(sunrise_time).do(capture)
    print "The picture will be captured tomorrow at: ",(sunrise_time)

def capture():
    '''
    None -> None
    Capture the picture and save it with todays date and time
    '''
    print "Capturing"
    with picamera.PiCamera() as camera:
        filename = (datetime.now()).strftime('%Y_%m_%d_%H_%M') + ".jpg"
        camera.start_preview()
        camera.capture("./" + filename)
        camera.stop_preview()


schedule.every().day.at("01:00").do(scheduleSunRiseTime)

while True:
    schedule.run_pending()
    time.sleep(1)

