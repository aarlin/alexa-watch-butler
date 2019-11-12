from string import Formatter
from ask_sdk_core.handler_input import HandlerInput
import dateutil.parser
from datetime import date 
import re

class EmptyNoneType(object):

    def __nonzero__(self):
        return False

    def __str__(self):
        return ''

    def __getattr__(self, name):
        return EmptyNoneType()

    def __getitem__(self, idx):
        return EmptyNoneType()
    
class EmptyNoneFormatter(Formatter):

    def get_value(self, field_name, args, kwds):
        v = Formatter.get_value(self, field_name, args, kwds)
        if v is None:
            return EmptyNoneType()
        return v

def supports_display(handler_input):
    # type: (HandlerInput) -> bool
    """Check if display is supported by the skill."""
    try:
        if hasattr(
                handler_input.request_envelope.context.system.device.
                        supported_interfaces, 'display'):
            return (
                    handler_input.request_envelope.context.system.device.
                    supported_interfaces.display is not None)
    except:
        return False

def get_age(birth_date):
    # birth_date in ISO8601 format ex. 1994-11-12T02:11:54.099Z
    born = dateutil.parser.parse(birth_date).date()
    today = date.today() 
    try:  
        birthday = born.replace(year = today.year) 
    # raised when birth date is February 29 
    # and the current year is not a leap year 
    except ValueError:  
        birthday = born.replace(year = today.year, 
        month = born.month + 1, day = 1) 
    if birthday > today: 
        return today.year - born.year - 1
    else: 
        return today.year - born.year 

def extract_user_data(user):
    id = user['_id']
    name = sanitize_information(user['name'])
    photo = user['photos'][0]['processedFiles'][0]['url']
    age = str(get_age(user['birth_date']))
    print(type(user['bio']))
    bio = sanitize_information(user['bio'])
    print(type(bio))
    try:
        job = user['jobs'][0]['title']['name']
    except (IndexError, KeyError):
        job = ''
    
    try:
        company = user['jobs'][0]['company']['name']
    except (IndexError, KeyError):
        company = ''
    
    try:
        school = user['schools'][0]['name']
    except (IndexError, KeyError):
        school = ''
        
    user_data = {"id": id, "name": name, "photo": photo, "age": age, "bio": bio, "job": job, "company": company, "school": school}
    return user_data

def sanitize_information(information):
    return re.sub('&', 'and', str(information))