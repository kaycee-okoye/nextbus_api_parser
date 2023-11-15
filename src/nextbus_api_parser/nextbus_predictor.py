"""
    Module implements a command-line interface which uses the other modules
    to query specific bus predictions from the NextBus API
"""

from datetime import datetime
from nextbus_api_parser.api_handler import ApiHandler
from nextbus_api_parser.data_classes import Error

class NextBusPredictor:
    """Class that handles user interactions to get specific predictions from the api"""

    # Below are strings used to describe different stages in the program flow"
    AGENCY_SELECTION = "agencies" # level 1, the user is selecting from a list of agencies
    ROUTE_SELECTION = "routes" # level 2, the user is selecting from a list of routes in an agency
    STOP_SELECTION = "stops" # level 3, the user is selecting from a list of stops in a route
    PREDICTIONS_DISPLAY = "predictions" # level 4, the user is viewing the predictions

    def __init__(self):
        self.routes = []
        self.stops = []
        self.route = None
        self.predictions = None
        self.active = True # if active is true, the script will not terminate
        self.api_handler = ApiHandler() # initialize the API Handler that'll be used to make
        # API calls and parse the xml feed
        self.agencies = self.api_handler.get_agencies() # get a list of available agencies
        # from the api
        self.selections = [] # whenever a user selects an agency, route .etc. to expand on,
        # the number representing the selected category will be appended
        self.level = 0 # this integer will continually be the length of the list of selections,
        # it gives an idea of what category the user is narrowed in on
        self.max = len(self.agencies) # this tracks the maximum number of categories in the
        # current level i.e the highest value a user can input for a selection
        self.error_message = ""
        self.begin()

    def begin(self):
        """Method to display welcome message and then begin the script's flow"""
        print(
            "\nWelcome to my script. It handles user input to make and interprete" +
            "NextBus API calls to get bus predictions"
        )
        self.handle_prompt_and_input()

    def handle_prompt_and_input(self):
        """Method that handles main flow of the script"""
        user_input = self.get_number_input(self.get_prompt()) # display the appropriate
        # prompt and collect user input
        if user_input == -1:
            # -1 is the entry for if the user wants to go back to previous level
            # or close the app if they're just starting
            self.go_back()
        elif user_input == -2:
            # -2 is the entry for if the user wants to exit the script
            self.close()
        elif user_input == -3:
            # -3 represents an input error, this will repeat the current level
            print("\nSorry, your input was not recognized. Please try again")
        else:
            # any positive integer input 0 implies that the user made a
            # selection that needs to be handled
            if user_input < self.max: # there is a maximum number of choices a
                # user can select from, this needs to be enforced
                if self.get_current_level() == self.PREDICTIONS_DISPLAY or (
                    len(self.error_message) > 0):
                    if user_input == 0:
                        # when displaying predictions, an input of 0 implies
                        # that the user opted to go back to the very first level
                        self.selections = []
                    elif user_input == 1:
                        if len(self.error_message) > 0:
                            # if there was an error and the user opted to refresh,
                            # refresh and restart the method
                            self.update_level()
                            self.handle_prompt_and_input()
                        # when displaying predictions, an input of 1 implies that the user
                        # opted to refresh the predictions
                        # there is no need to do anything, when the code escapes these
                        # conditional statements and self.update_level() and then
                        # self.handle_prompt_and_input() are called, the predictions will refresh
                else:
                    self.selections.append(user_input)
                self.update_level()
            else:
                # if the users enters a number choice that is higher than the
                # maximum number of available choices
                # display error and allow them try again
                print(f"Incorrect input, please select an int ranging from -2 - {self.max - 1}")
        self.handle_prompt_and_input() # restart the method at the new level


    def get_prompt(self):
        """
        Method to provide appropriate prompt for user input

        level_name is what category (e.g. Agencies or bus stops)
        the user is making a selection for i.e. their current level
        back_action is what will happen if the user inputs -1

        Returns
        -------
        str
            appropriate prompt
        """
        if len(self.error_message) > 0: # if there is was an error from the API call
            prompt = f"\nError!\n{self.error_message}\nPlease input 1 to refresh\nInput 0 to go back to the list of Agencies\nInput -1 to go back\nInput -2 to exit\n\n"
        # if they are currently viewing predictions
        elif self.get_current_level() == self.PREDICTIONS_DISPLAY:
            prompt = f"\nPlease input 1 to refresh\nInput 0 to go back to the list of Agencies\nInput -1 to go back to the list of routes\nInput -2 to exit\n\n{self.predictions_to_string()}"
        else:
            level_name = "agency"
            back_action = "exit"
            if self.get_current_level() == self.ROUTE_SELECTION:
                level_name = "route"
                back_action = "go back to the list of agencies"
            elif self.get_current_level() == self.STOP_SELECTION:
                level_name = "stop"
                back_action = "go back to the list of routes"
            prompt = f"\nPlease input the number corresponding to the {level_name} you are interested in.\nInput -1 to {back_action}\nInput -2 to exit\n\n{self.get_options()}"
        return f"{prompt}\nInput your selection: "

    def get_options(self):
        """
        Method to check current level
            
        Returns
        -------
        str
            available options appropriate to current level based on users previous selections
        """
        options = "" # available options to select from based on current level
        # and previous e.g. bus routes in a specific agency
        index = 0 # the number the user would input to represent a specific
        # option i.e. the index of the option
        if self.get_current_level() == self.AGENCY_SELECTION:
            for agency in self.agencies:
                options += f"{index} {agency.title}\n"
                index += 1
        elif self.get_current_level() == self.ROUTE_SELECTION:
            for route in self.routes:
                options += f"{index} {route.title}\n"
                index += 1
        elif self.get_current_level() == self.STOP_SELECTION:
            for stop in self.stops:
                # not all stops have a title (their tag value will be empty),
                # those can just be listed as their tag
                stop_name = stop.title if(stop.title) else "Stop No: " + stop.tag
                options += f"{index} {stop_name}\n"
                index += 1

        return options

    def predictions_to_string(self):
        """
        Method to gather prediction data for a specific stop into a multiline string

        Returns
        -------
        str
            prepared predictions
        """
        now = datetime.now() # time the predictions were displayed (current time)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        prediction_data = "\nNext Buses Available"
        directions = self.predictions.directions
        if self.predictions.dir_title:
            # This attribute is only provided by the API when there are no
            # predictions available for that stop
            # Therefore, if it's not empty, let the user know that there
            # are no available predictions
            prediction_data = "\nNo Predictions Available"
        else:
            for direction in directions:
                prediction_data += f"\n\tDirection: {direction.title}"
                prediction_list = direction.predictions
                for prediction in prediction_list:
                    eta = prediction.minutes + " minutes"
                    prediction_data += f"\n\t\t{eta}"
        prediction_data += f"\n\nInformation as of {dt_string}\n"
        return prediction_data

    def get_number_input(self, prompt):
        """
        Method to safely collect user input without errors or crashing.

        Parameters
        ----------
        prompt : str
            input prompt to be shown to the user

        Returns
        -------
        int
            User input. A value of -3 is returned if an input error is detected
        """
        try:
            user_input = int(input(prompt)) # display desired prompt and wait for user input
            return user_input if user_input > -3 else -3 # if the number is less than -2,
            # there is an issue
        except ValueError:
             # the only input the user should give should be integer number selections
            return -3 # an input of -3 signifies an input error,
            # return this if the user enters a non-numeric value

    def go_back(self):
        """Method to go back to previous level"""
        if self.get_current_level() != self.AGENCY_SELECTION: # check if user is not
            # still on the first level
            del self.selections[-1] # delete most recent selection (which was what
            # got the app to the currnt level)
            self.update_level() # update the level
        else:
            self.close() # if the user is still on the first level, terminate the script

    def update_level(self):
        """
            Method to make and process API call based on previous selections and the current level
        """
        self.error_message = "" # clear error message each time before updating

        if self.get_current_level() != self.AGENCY_SELECTION:
            # get the tag of the agency the user expanded on (if any)
            current_agency = self.agencies[self.selections[0]].tag
        if self.get_current_level() in [self.STOP_SELECTION, self.PREDICTIONS_DISPLAY]:
            # get the tag of the route the user expanded on (if any)
            current_route = self.routes[self.selections[1]].tag
        if self.get_current_level() == self.PREDICTIONS_DISPLAY:
            # get the tag of the stop the user expanded on (if any)
            current_stop = self.stops[self.selections[2]].tag

        if self.get_current_level() == self.AGENCY_SELECTION:
            # get the list of available agencies and update the maximum number
            # of options to the number of available agencies
            self.agencies = self.api_handler.get_agencies()
            if self.agencies is Error:
                # if the api handler returned an error, set the error message and
                # update the maximum number of options
                # to the available options displayed in the prompt (see method get_prompt)
                # then end the method without doing anything else
                self.error_message = self.agencies.message
                self.max = 2
                return
            self.max = len(self.agencies)
        elif self.get_current_level() == self.ROUTE_SELECTION:
            # get the list of routes associated with the agency the user selected
            # and updated the maximum number of options
            # to the number of available routes
            self.routes = self.api_handler.get_routes(current_agency)
            if self.routes is Error:
                # if the api handler returned an error, set the error message and update the
                # maximum number of options
                # to the available options displayed in the prompt (see method get_prompt)
                # then end the method without doing anything else
                self.error_message = self.routes.message
                self.max = 2
                return
            self.max = len(self.routes)
        elif self.get_current_level() == self.STOP_SELECTION:
            # get a detailed description of the route the user selected and updated the maximum
            # number of options to the number of
            # stops associated with that route
            self.route = self.api_handler.get_route_details(current_agency, current_route)
            if self.route is Error:
                # if the api handler returned an error, set the error message and update the
                # maximum number of options
                # to the available options displayed in the prompt (see method get_prompt)
                # then end the method without doing anything else
                self.error_message = self.route.message
                self.max = 2
                return
            self.stops = self.route.stops
            self.max = len(self.stops)
        elif self.get_current_level() == self.PREDICTIONS_DISPLAY:
            # get the list of routes associated with the agency the user selected
            # and update the maximum number of options
            # to the available options displayed in the prompt (see method get_prompt)
            self.predictions = self.api_handler.get_predictions(
                current_agency, current_route, current_stop)
            if self.predictions is Error:
                # if the api handler returned an error, set the error message and
                # update the maximum number of options
                # to the available options displayed in the prompt (see method get_prompt)
                # then end the method without doing anything else
                self.error_message = self.predictions.message
                self.max = 2
                return
            self.max = 2

    def close(self):
        """Method to terminate the script"""
        print("Thank you for using my script")
        quit() # terminate script

    def get_current_level(self):
        """
        Method to get the title/tag of the current level in the script

        This is based on the number of selections the user has made

        Returns
        -------
        str
            constant values representing the current level. These are used throughout
            script to identify the levels
        """
        self.level = len(self.selections)
        if self.level == 0:
            return self.AGENCY_SELECTION
        elif self.level == 1:
            return self.ROUTE_SELECTION
        elif self.level == 2:
            return self.STOP_SELECTION
        elif self.level == 3:
            return self.PREDICTIONS_DISPLAY
NextBusPredictor()
