# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.response_helper import get_plain_text_content

from ask_sdk_model.ui import SimpleCard, StandardCard
from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective,
    BackButtonBehavior, BodyTemplate3)
from ask_sdk_model import ui
from ask_sdk_model import Response

from fb_auth import get_auth_token
from phone_auth import send_phone_code, get_token_through_phone
from tinder_api import set_location, get_matches, swipe_left, swipe_right, get_profile, super_like
from alexa_api import get_permissions
from utils import EmptyNoneFormatter, supports_display, get_age

sb = CustomSkillBuilder(api_client=DefaultApiClient())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        access_token = handler_input.request_envelope.context.system.user.access_token

        api_access_token = handler_input.request_envelope.context.system.api_access_token
        api_endpoint = handler_input.request_envelope.context.system.api_endpoint

        permissions_response = get_permissions(api_access_token, api_endpoint)
        
        session_attributes['AUTH_TOKEN'] = '3ac77b1f-0e7b-45b2-bfdf-cfb23a4029e9' # TODO
        
        phone_number = ''
        if 'ACCESS_DENIED' not in permissions_response.values():
            print('here')
            user_preferences_client = handler_input.service_client_factory.get_ups_service()
            profile_mobile_number = user_preferences_client.get_profile_mobile_number()

            phone_number = profile_mobile_number.country_code + profile_mobile_number.phone_number.replace(" ", "")
            print(phone_number)

            session_attributes['PHONE_NUMBER'] = phone_number

        if phone_number:
            # request_code = send_phone_code(phone_number) TODO
            request_code = ''
            session_attributes['REQUEST_CODE'] = request_code

            authorized_speech_text = (
                "Welcome to Tinder Voice! "
                "What is the request code we sent your phone number?")
            return handler_input.response_builder.speak(authorized_speech_text).set_card(
            SimpleCard("Hello World", authorized_speech_text)).set_should_end_session(
            False).response
        else:
            # speech_text = (
            #     "Welcome to Tinder Lite! "
            #     "Would you like to authenicate with phone or authenticate through facebook?")
                

            # return handler_input.response_builder.speak(speech_text).set_card(
            #     SimpleCard("Hello World", speech_text)).set_should_end_session(
            #     False).response
            NOTIFY_MISSING_PERMISSIONS = ("Please enable Location permissions in "
                "the Amazon Alexa app.")
            permissions = ["alexa::profile:mobile_number:read"]
            return handler_input.response_builder.speak(NOTIFY_MISSING_PERMISSIONS).set_card(
            AskForPermissionsConsentCard(permissions=permissions)).response

class PhoneAuthIntentHandler(AbstractRequestHandler):
    """Handler for Phone Auth Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PhoneAuthIntent")(handler_input)
        
    def handle(self, handler_input):
        """Handler for Skill Launch."""
        # type: (HandlerInput) -> Response
        speech_text = "To access Tinder, we will send a request code to you. What is your phone number?"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
            False).response

class FacebookAuthIntentHandler(AbstractRequestHandler):
    """Handler for Facebook Auth Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FacebookAuthIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Skill Launch."""
        # type: (HandlerInput) -> Response
        speech_text_invalid_acc_link = "To access Tinder, please setup account linking."
        speech_text_valid_acc_link = "We have you authenticated. Where do you want to set your location to?"
        
        access_token = handler_input.request_envelope.context.system.user.access_token
        session_attributes = handler_input.attributes_manager.session_attributes


        if access_token:
            auth_token = get_auth_token(access_token)
            session_attributes['AUTH_TOKEN'] = auth_token
            return handler_input.response_builder.speak(speech_text_valid_acc_link).set_card(
                SimpleCard("Facebook Authentication", speech_text_valid_acc_link)).set_should_end_session(
                False).response
        else:
            return handler_input.response_builder.speak(speech_text_invalid_acc_link).set_card(
                SimpleCard("Facebook Authentication", speech_text_invalid_acc_link)).set_should_end_session(
                False).response

class PhoneRequestCodeIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PhoneRequestCodeIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Phone Authentication Intent."""
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        session_attributes = handler_input.attributes_manager.session_attributes

        if 'PhoneNumber' in slots:
            phone_number = slots['PhoneNumber'].value
            session_attributes['PHONE_NUMBER'] = phone_number
            request_code = send_phone_code(phone_number)
            session_attributes['REQUEST_CODE'] = request_code
        elif session_attributes['REQUEST_CODE'] == False:
            print('here')
        else:
            speech = "I'm not sure what your phone number is, please try again"
            reprompt = ("I'm not sure what your phone number is. "
                        "You can tell me your phone number by saying, "
                        "my phone number is ")

        speech_text = "What is the request code that was sent to your phone?"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
            False).response

class PhoneAuthenticationIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PhoneAuthenticationIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Phone Authentication Intent."""
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        session_attributes = handler_input.attributes_manager.session_attributes

        if 'SMSCode' in slots:
            sms_code = slots['SMSCode'].value
            session_attributes['SMS_CODE'] = sms_code
            auth_token = get_token_through_phone(sms_code, session_attributes['PHONE_NUMBER'], session_attributes['REQUEST_CODE'])

            session_attributes['AUTH_TOKEN'] = auth_token
        else:
            speech = "I'm not sure what your confirmation code is, please try again"
            reprompt = ("I'm not sure what your confirmation code is. "
                        "You can tell me your confirmation code by saying, "
                        "my confirmation code is ")

        speech_text = "Okay, we have you authenticated. Do you want matches or set your location?"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
            False).response

class GetMatchesIntentHandler(AbstractRequestHandler):
    """Handler for Get Matches Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetMatchesIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Get Matches Intent."""
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        
        session_attributes['AUTH_TOKEN'] = '3ac77b1f-0e7b-45b2-bfdf-cfb23a4029e9' # TODO

        matches = get_matches(session_attributes['AUTH_TOKEN'])
        print(matches)
        
        session_attributes['CURRENT_MATCH'] = matches['_id']

        speech_text = matches['name']
        image = {
            "smallImageUrl": matches['photos'][0]['processedFiles'][0]['url'],
            "largeImageUrl": matches['photos'][0]['processedFiles'][0]['url']
        }
        print(image)
        
        name = matches['name']
        age = ' ' + str(get_age(matches['birth_date']))
        bio = matches['bio']
        photo = matches['photos'][0]['processedFiles'][0]['url']
        try:
            job = matches['jobs'][0]['title']['name']
        except (IndexError, KeyError):
            job = ''
        
        try:
            company = ' @ ' + matches['jobs'][0]['company']['name']
        except (IndexError, KeyError):
            company = ''
        
        try:
            school = matches['schools'][0]['name']
        except (IndexError, KeyError):
            school = ''
        
        handler_input.response_builder.set_card(
            ui.StandardCard(
                title= name + age,
                text=job + company + '\n' + school + '\n' + bio,
                image=ui.Image(
                    small_image_url=photo,
                    large_image_url=photo
                )
            )
        )
        
        if supports_display(handler_input):
            print('here')
            img = Image(
                sources=[ImageInstance(url=photo)])
            title = name + age
            primary_text = job + company
            secondary_text = school
            tertiary_text = bio
            text_content = get_plain_text_content(
                primary_text=primary_text, secondary_text=secondary_text, tertiary_text=tertiary_text)
            
            handler_input.response_builder.add_directive(
                RenderTemplateDirective(
                    BodyTemplate3(
                        back_button=BackButtonBehavior.VISIBLE,
                        image=img, title=title,
                        text_content=text_content)))

        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

class SwipeLeftIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SwipeLeftIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Hello World Intent."""
        session_attributes = handler_input.attributes_manager.session_attributes
        
        print(session_attributes['CURRENT_MATCH'])
        
        response = swipe_left(session_attributes['AUTH_TOKEN'], session_attributes['CURRENT_MATCH'])
        
        speech_text = "You swiped left"
        print('left', response)

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Swipe Left", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

class SwipeRightIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SwipeRightIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Hello World Intent."""
        session_attributes = handler_input.attributes_manager.session_attributes
        
        response = swipe_right(session_attributes['AUTH_TOKEN'], session_attributes['CURRENT_MATCH']) 
        print('right', response)
        
        speech_text = "You swiped right"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Swipe Right", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

class SuperLikeIntentHandler(AbstractRequestHandler):
    """Handler for Super Like Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SuperLikeIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Super Like Intent."""
        session_attributes = handler_input.attributes_manager.session_attributes
        
        response = super_like(session_attributes['AUTH_TOKEN'], session_attributes['CURRENT_MATCH']) 
        print('super like', response)
        
        speech_text = "You super liked {}".format(session_attributes['CURRENT_MATCH'])
        
        if 'limit_exceeded' in response.keys():
            speech_text = 'You do not have any super likes. Your super like resets at {}'.format(response['super_likes']['resets_at'])

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Super Like", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response
    

class SetLocationIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SetLocationIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Hello World Intent."""
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        session_attributes = handler_input.attributes_manager.session_attributes

        city = slots['City'].value
        country = slots['Country'].value
        
        print(city, country)

        if city is not None:
            session_attributes['CITY'] = city
            response = set_location(session_attributes['AUTH_TOKEN'], city)
        elif country is not None:
            session_attributes['COUNTRY'] = country
            response = set_location(session_attributes['AUTH_TOKEN'], country)
        else:
            speech = "I'm not sure what city you asked for, please try again"
            reprompt = ("I'm not sure what city you set your location to. "
                        "You can tell me your set city location by saying, "
                        "set my location to ")

        fmt = EmptyNoneFormatter()
        speech_text = fmt.format("We set your location to {} {}", city, country) 

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Location Set", speech_text)).set_should_end_session(
            False).response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        print(session_attributes)
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PhoneAuthIntentHandler())
sb.add_request_handler(FacebookAuthIntentHandler())
sb.add_request_handler(PhoneRequestCodeIntentHandler())
sb.add_request_handler(PhoneAuthenticationIntentHandler())
sb.add_request_handler(GetMatchesIntentHandler())
sb.add_request_handler(SwipeLeftIntentHandler())
sb.add_request_handler(SwipeRightIntentHandler())
sb.add_request_handler(SuperLikeIntentHandler())
sb.add_request_handler(SetLocationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

