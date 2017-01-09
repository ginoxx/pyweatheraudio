import requests
import json
import boto3

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir


class Weather(object):
    def __init__(self, cityid):
        self.cityid = cityid

    def status(self):
        units = 'metric'
        apikey = '0bc458f67af4c677b83b2f7da9cb9d30'
        url = "http://api.openweathermap.org/data/2.5/weather?id=%s&units=%s&apikey=%s" % (self.cityid,units,apikey)
        # Fetch url
        print("Fetching url..")

        # Do the HTTP get request
        response = requests.get(url, verify=True) #Verify is check SSL certificate

        # Error handling

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            exit()

        # Decode the JSON response into a dictionary and use the data

        data = response.json()

        main = data['weather'][0]['main']
        descr = data['weather'][0]['description']
        temp = data['main']['temp']
        location =data['name']
        #print('Weather today in %s : %s - %s with %s degrees')% (location,main,descr, temp)
        #print "-------"
        text = 'Weather today in %s is %s with %s degrees' % (location,main,temp)
        return text

    def forecast(self):
        pass

    def speak(self,text):
        session = Session(profile_name="default")
        polly = session.client("polly")

        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                                VoiceId="Joanna")
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)

        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important as the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        print text
        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])


a_weather = Weather(2643743)
#out = a_weather.status()
#a_weather.speak(out)
a_weather.speak(a_weather.status())
