import json
import requests
from geopy.geocoders import Nominatim
from utils import get_age, extract_user_data
from datetime import datetime

def set_location(auth_token, location):
    location_headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }

    URL = 'https://api.gotinder.com/user/ping'

    geolocator = Nominatim(user_agent="Tinder Location Setter")
    location_data = geolocator.geocode(location)
    
    data = {
        "lat": location_data.latitude,
        "lon": location_data.longitude
    }
    
    r = requests.post(URL, headers=location_headers, data=json.dumps(data), verify=True)
    response = r.json()
    print('[set_location]: ', response)

    return data

def get_recommendations(auth_token):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/user/recs'
    
    r = requests.get(URL, headers=headers, verify=True)
    response = r.json()
    print('[get_recommendations]: ', response)
        
    return [extract_user_data(user) for user in response['results']]


def swipe_left(auth_token, id):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/pass/{}'.format(id)
    print(URL)
    
    r = requests.get(URL, headers=headers, verify=True)
    response = r.json()
    print('[swipe_left]: ', response)

    return response

def swipe_right(auth_token, id):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/like/{}'.format(id)
    print(URL)
    
    r = requests.get(URL, headers=headers, verify=True)
    response = r.json()
    print('[swipe_right]: ', response)

    return response

def super_like(auth_token, id):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/like/{}/super'.format(id)
    print(URL)
    
    r = requests.post(URL, headers=headers, verify=True)
    response = r.json()
    print('[super_like]: ', response)

    return response

def get_profile(auth_token, id):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/user/{}'.format(id)
    
    r = requests.get(URL, headers=headers, verify=True)
    response = r.json()
    print('[get_profile]: ', response)

    return response

def get_updates(auth_token):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/updates'
    
    data = {
        "last_activity_date": str(datetime.utcnow())
    }
    
    r = requests.post(URL, headers=headers, data=json.dumps(data), verify=True)
    response = r.json()
    print('[get_updates]: ', response)

    return response

def get_fast_match_teasers(auth_token):
    headers = {
      'X-Auth-Token' : auth_token,
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
    
    URL = 'https://api.gotinder.com/v2/fast-match/teasers'
    
    r = requests.get(URL, headers=headers, verify=True)
    response = r.json()
    print('[get_fast_match_teasers]: ', response)
    
    users = [user for user in response['data']['results']]
    user_photos = [user['user']['photos'][0]['url'] for user in users]
    
    return user_photos