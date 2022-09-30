# -*- coding: utf-8 -*-

# All code contained within this file is for getting feedback on the user's experience
# Please do not move review code out of this file (aside from importing and adding the intent handler in lambda_function.py)

# Default imports from lambda_function.py
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

# Google Sheets API
import gspread

def find_open_cell(handler_input):
    # Open the Review sheet using the gspread API
    gc = gspread.service_account(filename = 'credentials.json')
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1UBS-apn-lkSOZPgEd3KOawlVfY2k_iVIb-qEEZjAKiI")
    # This selects the specific worksheet within the overall google sheet
    worksheet = sh.get_worksheet(0)
    
    #num_reviews = len(worksheet.get_all_values())
    #worksheet.update_cell(num_reviews + 1, 1)
    
    
def convert_list_to_dict(list):
    # This list (initially empty) will be returned when filled with the important info for locating staff
    big_list = []
    
    # Convert each row in the 2D list, skipping over the first 3 rows which are just labels and any rows with empty first or last names
    for row in list:
        if row[0].strip() == "HST Residents":
            continue
        elif row[1].strip() == "Name":
            continue
        elif row[0].strip() == "Floor":
            continue
        elif row[1].strip() == "":
            continue
        elif row[2].strip() == "":
            continue
        elif row[6].strip() == "":
            continue
        
        # Set the mapping for this name (column 1) to a room (column 6), stripping away any extra space
        small_list = []
        small_list.append(row[1].strip().lower())
        small_list.append(row[2].strip().lower())
        small_list.append(row[6].strip())
        big_list.append(small_list)
        
    return big_list

def load_sheet_into_session(handler_input):
    # Open the HST Residents sheet using the gspread API
    gc = gspread.service_account(filename = 'credentials.json')
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1EyvrGtERR_NuZ90oOmMiXb2VzfJcHczJSNfTpO-MzxA")
    # This selects the specific worksheet within the overall google sheet
    worksheet = sh.get_worksheet(0)
    
    # Read in sheet data as a list of lists , convert to a dictionary, and store in the session attributes
    handler_input.attributes_manager.session_attributes["office_data"] = convert_list_to_dict(worksheet.get_all_values())

def get_similar_names(office_data, name):
    lev_results = {}
    for row in office_data:
        # row[0] is the last name
        curr_lev = levenshtein_distance(name, row[0])
        if lev_results.get(curr_lev) is None:
            lev_results[curr_lev] = []
        lev_results[curr_lev].append(row)
    
    distance = 0
    while True:
        names = lev_results.get(distance)
        if names is not None:
            return names
        distance += 1
    
    
    #try:
        #return office_data[name]
    #except KeyError:
        #return "Sorry, I can't find that person."

def get_office_from_names(office_data, names):
    output = ""
    for name in names:
        output += name[1] + " " + name[0] + "'s office is in room " + name[2] + ". "
    output += "Let me know if you need direction in HST. Or you can stop."
    return output

class ReviewIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ReviewIntent")(handler_input)

    def handle(self, handler_input):
        # Get any existing session attributes - look in this dict for sheet data
        session_attr = handler_input.attributes_manager.session_attributes
        if "office_data" not in session_attr:
            load_sheet_into_session(handler_input)
        
        # Pull the requested name from the slot
        slots = handler_input.request_envelope.request.intent.slots
        name = slots["name"].value.strip().lower()
        
        speak_output = get_office_from_names(session_attr["office_data"], get_similar_names(session_attr["office_data"], name))
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
