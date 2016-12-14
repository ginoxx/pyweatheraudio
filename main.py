import requests
import json
# Set the request parameters
cityid = 2643743
units = 'metric'
apikey = '0bc458f67af4c677b83b2f7da9cb9d30'
url = "http://api.openweathermap.org/data/2.5/weather?id=%s&units=%s&apikey=%s" % (cityid,units,apikey)

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
print('Weather today in %s : %s - %s with %s degrees')% (location,main,descr, temp)
print "-------"

#decoded = json.loads(data)
#print decoded
#print data
for row in data.items():
    print row
