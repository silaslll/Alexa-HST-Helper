# -*- coding: utf-8 -*-

# All code contained within this file is for navigation between two "nodes" in HST
# Please do not move HST navigation code out of this file (aside from importing and adding the intent handler in lambda_function.py)

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

# igraph library
import igraph

def convert_aliases_to_dict(list):
    dict = {}
    for row in list:
        if row[0] == "Destination (ALL LOWERCASE)":
            continue
        dict[row[0]] = row[1]
    return dict

def load_sheet_into_session(handler_input):
    # Open the HST Navigation sheet using the gspread API
    gc = gspread.service_account(filename = 'credentials.json')
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1TB3hWNmYk_llNPOU0Gg30OPY3llB5wLHGKZ6bhXQglQ")
    # This selects the specific worksheet within the overall google sheet
    worksheet = sh.get_worksheet(0)
    
    # Read in sheet data as a list of lists and store this structure in the session attributes
    handler_input.attributes_manager.session_attributes["connections"] = worksheet.get_all_values()
    
    # Get the aliases and store as a dictionary
    worksheet = sh.get_worksheet(1)
    handler_input.attributes_manager.session_attributes["aliases"] = convert_aliases_to_dict(worksheet.get_all_values())

def create_graph(connections_list):
    graph = igraph.Graph()
    
    # Loop once for each row on the sheet
    num_vertices = 0
    weights = []
    for row in connections_list:
        # Each row is one connection on the graph, so we extract the node names and the distance of this connection
        start_node = row[0]
        # This skips over the labeling row
        if start_node == "Node A":
            continue
        
        # This should skip over empty rows
        if row[2] == '':
            continue
        
        end_node = row[1]
        distance = int(row[2])
        
        try:
            start_vertex = graph.vs.find(name = start_node)
        except:
            graph.add_vertices(1)
            graph.vs[num_vertices]["name"] = start_node
            num_vertices += 1
            start_vertex = graph.vs.find(name = start_node)
            
        try:
            end_vertex = graph.vs.find(name = end_node)
        except:
            graph.add_vertices(1)
            graph.vs[num_vertices]["name"] = end_node
            num_vertices += 1
            end_vertex = graph.vs.find(name = end_node)
        
        graph.add_edges([(start_node, end_node)])
        weights.append(distance)
    
    graph.es["weight"] = weights
        
    return graph

def shortest_path(graph, src, dest):
    results = graph.get_shortest_paths(src, to=dest, weights=graph.es["weight"], output="vpath")
    nodes = []
    for i in range(len(results[0])):
        nodes.append(graph.vs[results[0][i]]["name"])
    return nodes


def dest_to_node(dict, location):
    try:
        return dict[location]
    except KeyError:
        return "Sorry, I couldn't find that place."
    
# # Select the destination to node mapping sheet and find the row with the destination -> use to get node
# worksheet = google_sheet.get_worksheet(1)
# dest_cell = worksheet.find(dest)
# node = worksheet.cell(dest_cell.row, 2).value

def path_to_dir(path, connections):
    # The path is a list of connected nodes, get the directions corresponding to these connections
    directions = ""
    
    # Loop over each node except the last because in each iteration we need to access the next node
    for i in range(len(path) - 1):
        #row = -1
        
        for row in connections:
            if row[0] == path[i]:
                if row[1] == path[i + 1]:
                    directions += row[3] + " "
                    break
            if row[1] == path[i]:
                if row[0] == path[i + 1]:
                    directions += row[4] + " "
                    break
                
        # Get a list of cells that contain the starting node in this pair
        #src_cells = worksheet.findall(path[i])
        
        # We begin looking for the row containing both the starting and ending node
        #for cell in src_cells:
            # If the starting cell is in column 2 on the sheet, the ending cell is in column 1
            # We also need to get the directions in the reverse direction
            #dest_col = 2
            #dir_col = 4
            #if cell.col == 2:
               # dest_col = 1
                #dir_col = 5
            
            # This will check if the correct row has been found and add to directions if so
            #if path[i + 1] == worksheet.cell(cell.row, dest_col).value:
                #directions += worksheet.cell(cell.row, dir_col).value + " "
    return directions

class HSTAskDirectionsIntentHandler(AbstractRequestHandler):
    """Handler for the HST Ask Directions Intent - Confirm that the user wants directions within HST"""
        
    def can_handle(self, handler_input):
        """Determine if this Intent was requested by the user"""
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HSTAskDirectionsIntent")(handler_input)

    def handle(self, handler_input):
        """The function to be executed upon a request to the HSTAskDirectionsIntent"""
        # type: (HandlerInput) -> Response
        
        # Get any existing session attributes - look in this dict for sheet data
        session_attr = handler_input.attributes_manager.session_attributes
        if "connections" not in session_attr:
            load_sheet_into_session(handler_input)
        
        speak_output = "I can give you directions within HST! Tell me where you are and where you want to go."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HSTNavigationIntentHandler(AbstractRequestHandler):
    """Handler for the HST Navigation Intent - Lead the user from an entrance to a location in the building"""
        
    def can_handle(self, handler_input):
        """Determine if this Intent was requested by the user"""
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HSTNavigationIntent")(handler_input)

    def handle(self, handler_input):
        """The function to be executed upon a request to the HSTNavigationIntent"""
        # type: (HandlerInput) -> Response
        
        # Get any existing session attributes - look in this dict for sheet data (must be here - exit otherwise)
        session_attr = handler_input.attributes_manager.session_attributes
        if "connections" not in session_attr:
            speak_output = "Please let me know if you need directions, before telling me where you want to go."
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
            )
        
        # Get the user's source and their desired destination from the slots
        slots = handler_input.request_envelope.request.intent.slots
        source = slots["source"].value
        destination = slots["destination"].value
        
        # Convert the session attribute into a graph
        graph = create_graph(session_attr["connections"])
        
        # Convert the destination and source to valid nodes
        src_node = dest_to_node(session_attr["aliases"], destination)
        dest_node = dest_to_node(session_attr["aliases"], source)
        
        speak_output = path_to_dir(shortest_path(graph, src_node, dest_node), session_attr["connections"])
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )