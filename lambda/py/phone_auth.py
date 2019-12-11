import json
import requests

def send_phone_code(phone_number):
    CODE_REQUEST_URL = "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms"
    HEADERS = {
        'User-Agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)',
        'Content-Type': 'application/json',
    }
    
    print(phone_number)
    
    data = {
        "phone_number": phone_number
    }
    
    print(json.dumps(data))
    
    r = requests.post(CODE_REQUEST_URL, headers=HEADERS, data=json.dumps(data), verify=True)
    
    print(r)

    response = r.json()
    print(response)
    if(response.get("data")['sms_sent'] == 'false'):
        return False
    else:
        return True

def get_token_through_phone(otp_code, phone_number):
    CODE_REQUEST_URL = "https://api.gotinder.com/v2/auth/sms/validate?auth_type=sms"
    HEADERS = {
        'User-Agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)',
        'Content-Type': 'application/json',
    }
    
    data = {
        "otp_code": otp_code,
        "phone_number": phone_number
    }
    
    r = requests.post(CODE_REQUEST_URL, headers=HEADERS, data=json.dumps(data), verify=True)

    response = r.json()
    print('first', response)
    
    if(response.get("data")['validated'] == True):
        refresh_token = response.get("data")['refresh_token']
        
        CODE_REQUEST_URL = "https://api.gotinder.com/v2/auth/login/sms"
        HEADERS = {
            'User-Agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)',
            'Content-Type': 'application/json',
        }
        
        data = {
            "client_version": "11.4.0",
            "refresh_token": refresh_token
        }
        
        r = requests.post(CODE_REQUEST_URL, headers=HEADERS, data=json.dumps(data), verify=True)

        response = r.json()
        print(response)
            
        return response.get('data')['api_token']
    else:
        return False

