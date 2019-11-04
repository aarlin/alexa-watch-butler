# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from authentication import send_phone_code, get_token_through_phone

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to the Tinder Alexa skill! " +
        "Would you like to authenicate with phone or authenticate through email"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_request_type("PhoneAuthIntent"))
def phone_auth_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "To access Tinder, we will send a request code to you. What is your phone number?"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_request_type("FacebookAuthIntent"))
def facebook_auth_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "To access Tinder, what is your Facebook email and password?"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Facebook Authentication", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("PhoneRequestCodeIntent"))
def phone_request_code_intent_handler(handler_input):
    """Handler for Phone Authentication Intent."""
    # type: (HandlerInput) -> Response

    slots = handler_input.request_envelope.request.intent.slots

    if 'PhoneNumber' in slots:
        phone_number = slots['PhoneNumber'].value
        handler_input.attributes_manager.session_attributes['PHONE_NUMBER'] = phone_number
    else:
        speech = "I'm not sure what your phone number is, please try again"
        reprompt = ("I'm not sure what your phone number is. "
                    "You can tell me your phone number by saying, "
                    "my phone number is ")

    speech_text = "What is the request code that was sent to your phone?"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("PhoneAuthenticationIntent"))
def phone_authentication_intent_handler(handler_input):
    """Handler for Phone Authentication Intent."""
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots

    if 'RequestCode' in slots:
        request_code = slots['RequestCode'].value
        handler_input.attributes_manager.session_attributes['REQUEST_CODE'] = request_code
    else:
        speech = "I'm not sure what your request code is, please try again"
        reprompt = ("I'm not sure what your request code is. "
                    "You can tell me your request code by saying, "
                    "my request code is ")

    speech_text = "Okay, we have you authenticated. Where do you want to set your location to?"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
        True).response

# set location to <city>
@sb.request_handler(can_handle_func=is_intent_name("SetLocationIntent"))
def set_location_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "We set your location to this New York"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Location Set", speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can say hello to me!"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Hello World", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Hello World skill can't help you with that.  "
        "You can say hello!!")
    reprompt = "You can say hello!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()


    # if color_slot_key in handler_input.attributes_manager.session_attributes:
    #     fav_color = handler_input.attributes_manager.session_attributes[
    #         color_slot_key]
