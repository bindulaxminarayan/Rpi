This script retrieves the sunrise time for a given latitude and longitude and captures image using your raspberry pi's picamera

#How to setup the environment:
This script requires python 2.7

Once you install python 2.7 install the below packages to work:
~~~~
 pip install schedule
 pip install requests
 pip install logging
 pip install picamera
~~~~

This script is designed to convert the time to EST. So, make sure you update the latitude, longitude and 
time conversion for your zone.


##Credit Links
We use sunset api for retrieving the sunrise time:
http://api.sunrise-sunset.org/json
