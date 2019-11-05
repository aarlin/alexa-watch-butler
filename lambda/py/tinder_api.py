import json
import requests
from geopy.geocoders import Nominatim

def set_location(auth_token, location):
    location_headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }

    URL = 'https://api.gotinder.com/user/ping'

    latitude = None
    longtitude = None
    geolocator = Nominatim(user_agent="Tinder Location Setter")

    location = geolocator.geocode(location)
    print((location.latitude, location.longitude))
    latitude = location.latitude
    longtitude = location.longtitude

    data = {
        "lat": latitude,
        "lon": longtitude
    }
    
    r = requests.post(URL, headers=location_headers, data=json.dumps(data), verify=False)
    response = r.json()
    return response