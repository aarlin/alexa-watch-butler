# Steps to Retrieve Tinder Auth


# Commands

```bash
# Create virtual environment
python -m venv facebook-auth
# Windows
facebook-auth\Scripts\activate  
# MacOS/Linux
source facebook-auth/bin/activate  
# Install dependencies  
pip install -r requirements.txt
# Deactivate venv
deactivate  
```

```bash
# Add your Facebook credentials
echo ""

# Run locally
sls invoke local -f get_fb_access_token --path events/login.json  
sls invoke local -f send_phone_code --path events/phone_number.json  
sls invoke local -f get_token --path events/phone_auth.json  
sls invoke local -f set_location --path events/coordinates.json  

# Deploy to AWS
sls deploy -v  
```

# Alexa Commands 
```bash 
sls alexa auth  
sls alexa create --name LocationSpoofer --locale en_US --type custom  
sls alexa update  
sls alexa build  
```

# References

Amazon OAuth2 - does not allow localhost; use 127.0.0.1

https://github.com/marcy-terui/serverless-alexa-skills  
https://medium.com/@rupakg/how-to-build-a-serverless-alexa-skill-51d8479e0432  
https://serverless.com/blog/how-to-manage-your-alexa-skills-with-serverless/  
https://forums.developer.amazon.com/questions/94166/alexa-skill-cant-work-after-changed-the-invocation.html  

get_fb_access_token -> get_auth_token -> set_location  

send_phone_code -> SMS -> get_token_through_phone -> set_location  

following steps...
env map file for username and password
either use step functions or just pass through into new function that uses all the other helpers
create slots for AMAZON.City, AMAZON.AT_REGION, AMAZON.AT_CITY

alexa -> ping location -> tracker

golang alexa skill
https://developer.here.com/blog/geocode-addresses-with-amazon-alexa-golang-and-the-here-geocoder-api