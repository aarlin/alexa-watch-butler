import 'source-map-support/register';
const axios = require('axios');

export const setLocation = async (event, _context) => {
  console.log('event', event);

  var postData = {
      "lat": 34.6937,
      "lon": 135.5023
  };
  
  let axiosConfig = {
    headers: {
      'X-Auth-Token' : '7b3fe0b6-50c4-47e2-b6bd-264e144778d1',
      'Content-Type': 'application/json',
      'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
    }
  };
  
  axios.post('https://api.gotinder.com/user/ping', postData, axiosConfig)
  .then(_res => {
    console.log("RESPONSE RECEIVED");
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
