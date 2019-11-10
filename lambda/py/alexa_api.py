import json
import requests

def get_permissions(api_access_token, api_endpoint):
    headers = {
        'Host': 'api.amazonalexa.com',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + api_access_token
    }

    URL = api_endpoint + '/v2/accounts/~current/settings/Profile.mobileNumber'

    r = requests.get(URL, headers=headers, verify=True)
    response = r.json()
    return response