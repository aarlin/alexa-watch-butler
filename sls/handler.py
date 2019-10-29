import json
import re
import requests
import robobrowser

MOBILE_USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y"
CODE_REQUEST_URL = "https://graph.accountkit.com/v1.2/start_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=en_US&phone_number=#placeholder&response_type=token&sdk=ios"
CODE_VALIDATE_URL = "https://graph.accountkit.com/v1.2/confirm_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&confirmation_code=#confirmation_code&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=en_US&login_request_code=#request_code&phone_number=#phone_number&response_type=token&sdk=ios"
TOKEN_URL = "https://api.gotinder.com/v2/auth/login/accountkit"

HEADERS = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0'}

def get_fb_access_token(event, context):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    ## submit login form
    f = s.get_form()
    f["pass"] = event['password']
    f["email"] = event['email']
    s.submit_form(f)

    ## click the 'ok' button on the dialog informing you that you have already authenticated with the Tinder app
    f = s.get_form()
    access_token = ''
    try:
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
        access_token = re.search(
            r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
    except requests.exceptions.InvalidSchema as browserAddress:
        access_token = re.search(
            r"access_token=([\w\d]+)", str(browserAddress)).groups()[0]

    auth_token = get_auth_token(access_token)
    response = {
        "statusCode": 200,
        "body": auth_token
    }

    return response

# def get_fb_id(access_token):
#     if "error" in access_token:
#         return {"error": "access token could not be retrieved"}
#     """Gets facebook ID from access token"""
#     req = requests.get(
#         'https://graph.facebook.com/me?access_token=' + access_token)
#     return req.json()["id"]

def get_auth_token(fb_auth_token):
    headers = {
        'app_version': '6.9.4',
        'platform': 'ios',
        "content-type": "application/json",
        "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
        "Accept": "application/json"
    }
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    url = 'https://api.gotinder.com/v2/auth/login/facebook'
    req = requests.post(url,
                        headers=headers,
                        data=json.dumps(
                            {'token': fb_auth_token })
                        )
    try:
        if (req.json()["data"]["is_new_user"] == 'true'):
            return {"error": "Login through Tinder one time before an api token can be retrieved"}
        tinder_auth_token = req.json()["data"]["api_token"]
        headers.update({"X-Auth-Token": tinder_auth_token})
        print("You have been successfully authorized!")
        return tinder_auth_token
    except Exception as e:
        print(e)
        return {"error": "Something went wrong. Sorry, but we could not authorize you."}

def send_phone_code(event, context):
    URL = CODE_REQUEST_URL.replace("#placeholder", event['number'])
    r = requests.post(URL, headers=HEADERS, verify=False)
    response = r.json()
    if(response.get("login_request_code") == None):
        return False
    else:
        return response["login_request_code"]

def get_token_through_phone(event, context):
    VALIDATE_URL = CODE_VALIDATE_URL.replace("#confirmation_code", event['code'])
    VALIDATE_URL = VALIDATE_URL.replace("#phone_number", event['number'])
    VALIDATE_URL = VALIDATE_URL.replace("#request_code", event['req_code'])
    r_validate = requests.post(VALIDATE_URL, headers=HEADERS, verify=False)
    validate_response = r_validate.json()
    access_token = validate_response["access_token"]
    access_id = validate_response["id"]
    GetToken_content = json.dumps({'token':access_token, 'id':access_id, "client_version":"9.0.1"})
    GetToken_headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0', 'Content-Type':'application/json'}
    r_GetToken = requests.post(TOKEN_URL, data=GetToken_content, headers=GetToken_headers, verify=False)
    token_response = r_GetToken.json()
    if(token_response["data"].get("api_token") == None):
        return token_response
    else:
        return token_response["data"]["api_token"]

def set_location(event, context):
    location_headers = {
      'X-Auth-Token' : event['auth_token'],
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }

    URL = 'https://api.gotinder.com/user/ping'
    
    r = requests.post(URL, headers=location_headers, data=json.dumps(event), verify=False)
    print(r.url)
    response = r.json()
    if(response['status'] == None):
        return False
    else:
        return response['status']