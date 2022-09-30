# -*- coding: utf-8 -*-

# This is the main file for handling requests to our skill
# Specific functionality is moved to other files for better organization

# Default imports
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# Maintain logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Other files
import hst_navigation
import hst_name_locator

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome! I can help you find someone in HST. Let me know who you want to find"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#COH customer intents 

#####

class HSTAssistantIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HSTAssistantIntent")(handler_input)

    def handle(self, handler_input):
        name = "Someone"
        slots = handler_input.request_envelope.request.intent.slots
        assistant = slots['type']
        speak_output = ""
        # take me down to the right person
        if assistant.value:
            if (assistant.value.replace(" ", "").lower() in ['minors','majors', 'declarations', 'internships', 'graduateadmissions', 'graduateprograms','courses','undergraduate admissions', 
            'undergraduate programs']):
                name = 'JenTopp'
            elif (assistant.value.replace(" ", "").lower() in ['graduatepopulationhealthprogram', 'graduatedirector', 'phdprograms', 'masterinpopulationhealth']):
                name = 'AlbertLiu'
            elif (assistant.value.replace(" ", "").lower() in ['paycheck', 'sponsorships', 'co-sponsorships', 'onecardreimbursements', 'onecardexpenses']):
                name = 'SherryBuss'
            elif (assistant.value.replace(" ", "").lower() in ['instituteforhealthpolicyandpolitics', 'ihpp']):
                name = 'EdGomez'
            elif (assistant.value.replace(" ", "").lower() in ['Institute for Indigenous Studies'.replace(" ", "").lower(), 'IIS'.replace(" ", "").lower()]):
                name = 'SeanDaley'
            elif (assistant.value.replace(" ", "").lower() in ['Health Data Warehouse'.replace(" ", "").lower(), 'HDW'.replace(" ", "").lower()]):
                name = 'BilalKhan'
            elif (assistant.value.replace(" ", "").lower() in ["children's environmental precision health institute".replace(" ", "").lower(), 'childrens health institute'.replace(" ", "").lower(), 'CEPHI'.replace(" ", "").lower()]):
                name = 'HyunokChoi'
            elif (assistant.value.replace(" ", "").lower() in ["director for Research and Graduate studies".replace(" ", "").lower(), 'Associate Dean for Research and Graduate studies'.replace(" ", "").lower(), 'Research and Graduate studies'.replace(" ", "").lower()]):            
                name = 'WonChoi'
            elif (assistant.value.replace(" ", "").lower() in ["faculty and staff".replace(" ", "").lower(), 'Associate dean for faculty and staff'.replace(" ", "").lower(), 'faculty affairs'.replace(" ", "").lower()]):
                name = 'EricaHoelscher'
            elif (assistant.value.replace(" ", "").lower() in ["advertisement".replace(" ", "").lower(), 'marketing'.replace(" ", "").lower(), 'advertising opportunities'.replace(" ", "").lower(),
            "undergraduate marketing".replace(" ", "").lower(), 'graduate marketing'.replace(" ", "").lower(), 'COH media relations'.replace(" ", "").lower(),
            "COH newsletter".replace(" ", "").lower(), 'social media for COH'.replace(" ", "").lower(), 'social media'.replace(" ", "").lower(),
            "Communications".replace(" ", "").lower(), 'advertising'.replace(" ", "").lower()]):
                name = 'ValeriePeters'
            elif (assistant.value.replace(" ", "").lower() in ["academic programs".replace(" ", "").lower(), 'Associate dean for academic programs'.replace(" ", "").lower(), 'MPH'.replace(" ", "").lower()]):
                name = 'MichaelGusmano'
            elif (assistant.value.replace(" ", "").lower() in ["college of health research".replace(" ", "").lower(), 'research opportunities'.replace(" ", "").lower(), 'on campus research for the college of health'.replace(" ", "").lower(), 'research expenses'.replace(" ", "").lower() ]):
                name = 'HeatherMessina'
            elif (assistant.value.replace(" ", "").lower() in ["funding research".replace(" ", "").lower(), 'sponsored research'.replace(" ", "").lower(), 'faculty research'.replace(" ", "").lower(), 'research in the college of health'.replace(" ", "").lower() ]):
                name = 'HollyHeather'
            elif (assistant.value.replace(" ", "").lower() in ["budget from college of health".replace(" ", "").lower(), 'expense reimbursements'.replace(" ", "").lower(), 'one card reimbursements'.replace(" ", "").lower(), 'paycheck'.replace(" ", "").lower() ]):
                name = 'SherryHeather'
            speak_output = name + " can help you. Let me know if you need to find " + name + "s location."
         # this assistant was not built
        else:
            speak_output = "Sorry, I don't know that"
            
        
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class MenuIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MenuIntent")(handler_input)
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        option = slots['option']
        speak_output = ""
        if (option == 'Way-Finding'):
            speak_output = "I can find way to ..."
        if (option == 'COH Desk Assistant'):
            speak_output = "Ask something like .."
        if (option == 'Staff Locator'):
            speak_output = "I can help you to find ..."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )





#####

# class AlbertLiuHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("AlbertLiu")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Albert Liu can help you. Let me know if you need to find Albert Liu's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

# class SherryBussHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("SherryBuss")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Sherry Buss can help you. Let me know if you need to find Sherry Buss's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

# class JenToppHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("JenTopp")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Jen Topp can help you. Let me know if you need to find Jen Topp's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class MichaelGusmanoHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("MichaelGusmano")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Michael Gusmano can help you. Let me know if you need to find Michael Gusmano's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class ValeriePetersHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("ValeriePeters")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Valerie Peters can help you. Let me know if you need to find Valerie Peters's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class EricaHoelscherHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("EricaHoelscher")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Erica Hoelscher can help you. Let me know if you need to find Erica Hoelscher's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class WonChoiHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("WonChoi")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Won Choi can help you. Let me know if you need to find Won Choi's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class JeanneHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("Jeanne")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Jeanne can help you. Let me know if you need to find Jeanne's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class HyunokChoiHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("HyunokChoi")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Hyunok Choi can help you. Let me know if you need to find Hyunok Choi's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class BilalKhanHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("BilalKhan")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Bilal Khan can help you. Let me know if you need to find Bilal Khan's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class SeanDaleyHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("SeanDaley")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Sean Daley can help you. Let me know if you need to find Sean Daley's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class HollyHeatherHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("HollyHeather")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Holly and Heather can help you. Let me know if you need to find Holly's or Heather's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )
# class SherryHeatherHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("SherryHeather")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Sherry and Heather can help you. Let me know if you need to find Sherry's or Heather's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

# class EdGomezHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("EdGomez")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Ed Gomez can help you. Let me know if you need to find Ed Gomez's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

# #### Stop here
# class HeatherMessinaHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("HeatherMessina")(handler_input)

#     def handle(self, handler_input):
#         speak_output = "Heather Messina can help you. Let me know if you need to find Heather Messina's location."

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hope this was useful. Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speak_output = "Sorry, I did not hear you properly. I can help you find someone or find your way in HST."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please reach out to our development team at echohawks.lehigh@gmail.com"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for our skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()

# Basic handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Custom handlers
sb.add_request_handler(hst_navigation.HSTNavigationIntentHandler())
sb.add_request_handler(hst_navigation.HSTAskDirectionsIntentHandler())
sb.add_request_handler(hst_name_locator.HSTStaffLocatorIntentHandler())

#Custom handlers for COH feature/skill
sb.add_request_handler(HSTAssistantIntentHandler())


# Make sure IntentReflectorHandler is the last request handler so it doesn't override the custom handlers
sb.add_request_handler(IntentReflectorHandler())

# Fallback for any exceptions
sb.add_exception_handler(CatchAllExceptionHandler())

# Create a lambda handler function that can be tagged to AWS Lambda handler.
lambda_handler = sb.lambda_handler()