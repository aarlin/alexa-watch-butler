import 'source-map-support/register';
const axios = require('axios');

export const sendPhoneCode = async (event, _context) => {
  let axiosConfig = {
    headers: {
      'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0'
    }
  }

  let codeRequestUrl = 'https://graph.accountkit.com/v1.2/start_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=en_US&phone_number=#placeholder&response_type=token&sdk=ios'
  codeRequestUrl = codeRequestUrl.replace(/#placeholder/, event)

  axios.post(codeRequestUrl, '', axiosConfig)
  .then(_res => {
    console.log("RESPONSE RECEIVED", _res);
  })
  .catch(err => {
    console.log("AXIOS ERROR: ", err);
  })

  // This may not work since we need the request code 
  // which then leads to the confirmation code

}

export const setLocation = async (event, _context) => {
  console.log('event', event);
  
  let axiosConfig = {
    headers: {
      'X-Auth-Token' : '7b3fe0b6-50c4-47e2-b6bd-264e144778d1',
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
  };
  
  axios.post('https://api.gotinder.com/user/ping', event, axiosConfig)
  .then(_res => {
    console.log("RESPONSE RECEIVED", _res);
  })
  .catch(err => {
    console.log("AXIOS ERROR: ", err);
  })

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: 'OK',
      input: event,
    }, null, 2),
  };
}
