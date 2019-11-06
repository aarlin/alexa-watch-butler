import re
import json
import requests
import robobrowser

def get_fb_access_token(email, password):
    MOBILE_USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"
    FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y"

    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    ## submit login form
    f = s.get_form()
    f["email"] = email
    f["pass"] = password
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

def get_auth_token(fb_auth_token):
    headers = {
        'app_version': '6.9.4',
        'platform': 'ios',
        "Content-Type": "application/json",
        "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"
    }
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    url = 'https://api.gotinder.com/v2/auth/login/facebook'
    data = {"token": fb_auth_token }
    req = requests.post(url,
                        headers=headers,
                        json=data
                        )
    try:
        if 'error' in req.json():
            return req.json()['error']
        elif 'data' in req.json() and req.json()["data"]["is_new_user"] == 'true':
            return {"error": "Login through Tinder one time before an api token can be retrieved"}
        else:
            tinder_auth_token = req.json()["data"]["api_token"]
            return tinder_auth_token
    except Exception as e:
        print(e)
        return {"error": "Something went wrong. Sorry, but we could not authorize you."}