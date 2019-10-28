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
