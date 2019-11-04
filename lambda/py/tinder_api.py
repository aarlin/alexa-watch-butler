from geopy.geocoders import Nominatim

def set_location(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    print(event['request'])
    print(event['request']['intent'])
    print(event['request']['intent']['slots'])
    location_headers = {
      'X-Auth-Token' : '<TOKEN>',
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }

    URL = 'https://api.gotinder.com/user/ping'

    # city_dict = event['request']['intent']['slots']['US_CITY']
    # state_dict = event['request']['intent']['slots']['US_STATE']
    # longitude_dict = event['request']['intent']['slots']['Longitude']
    # latitude_dict = event['request']['intent']['slots']['Latitude']
    latitude = None
    longtitude = None
    geolocator = Nominatim(user_agent="Tinder Location Setter")

    if 'value' in city_dict:
        location = geolocator.geocode("Austin Texas")
        print((location.latitude, location.longitude))
        latitude = location.latitude
        longtitude = location.longtitude
    else:
        latitude = 0
        longtitude = 0
    # if 'value' in longitude_dict and 'value' in latitude_dict:
    #     longtitude = longitude_dict['value']
    #     latitude = latitude_dict['value']
    # else:
    #     upperLimit = 100

    data = {
        "lat": latitude,
        "lon": longtitude
    }
    
    speech_text = "Hello Python World from Decorators!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        True).response
    
    r = requests.post(URL, headers=location_headers, data=json.dumps(data), verify=False)
    response = r.json()
    if(response['status'] == None):
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Error occurred from API response'
                }
            }
        }
    else:
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': '200 OK'
                }
            }
        }