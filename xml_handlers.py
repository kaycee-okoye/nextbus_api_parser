'''
    This file contains XML handlers used to parse the XML 
    feed from the API into appropriate data classes
'''

from xml.sax import ContentHandler
from data_classes import Agency, Error, Predictions, Route


class AgencyListHandler(ContentHandler):
    "A class designed to parse xml data for a list of Agencies from the API"
    def __init__(self):
        self.agencies = []
        self.error = None
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        '''
            In the xml tree, process tags that have start tags titled agency
            and convert them to an Agency data class. These xml tags contain 
            information about the specific agency 
        '''
        if name == "agency":
            self.agencies.append(Agency(attrs))

        elif name == "Error":
            # an error name only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        '''
            If the xml tree has been flagged as containing an error, collect 
            the error message in the body of the name
        '''
        if self.error is not None:
            self.error.set_message(content)

class RouteListHandler(ContentHandler):
    '''
        A class designed to parse xml data for a list of routes associated
        with a specific agency from the API
    '''
    def __init__(self):
        self.routes = []
        self.error = None
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        '''
            In xml tree, process tags that have start tags titled route
            and convert them to an Route data class. These xml tags contain 
            information about the specific route 
        '''
        if name == "route":
            self.routes.append(Route(attrs))

        elif name == "Error":
            # an error name only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        '''
            If the xml tree has been flagged as containing an error, 
            collect the error message in the body of the name
        '''
        if self.error is not None:
            self.error.set_message(content)

class RouteDetailsHandler(ContentHandler):
    '''
        A class designed to parse xml data for a detailed description of a specific route
        from the API
    '''

    def __init__(self):
        # this boolean indicates whether the tree has reached the part where it's listing Directions
        # and the stops associated with them
        self.is_in_direction_tag = False
        self.error = None
        self.route = None
        self.direction_tag = False
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        '''
            In xml tree, process tags that have start tags titled as seen below
            and convert them to a detailed Route data class. These xml tags contain 
            information that give a detailed description of a specific route 
        '''
        if name == "route":
            self.route = Route(attrs, True)

        elif name == "stop":
            if ~self.is_in_direction_tag:
                self.route.add_stop(attrs)
            else:
                self.route.add_stop(attrs, True)

        elif name == "direction":
            self.route.add_direction(attrs)
            self.direction_tag = True

        elif name == "path":
            self.route.add_path(attrs)

        elif name == "point":
            self.route.add_point(attrs)

        elif name == "Error":
            # an error name only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        '''
            If the xml tree has been flagged as containing an error, 
            collect the error message in the body of the name
        '''
        if self.error is not None:
            self.error.set_message(content)

class PredictionsHandler(ContentHandler):
    '''
        A class designed to parse xml data for a list of predictions associated
        with a specific bus stop from the API
    '''
    def __init__(self):
        self.error = None
        self.predictions = None
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if name == "predictions":
            self.predictions = Predictions(attrs)

        elif name == "direction":
            self.predictions.add_direction(attrs)

        elif name == "prediction":
            self.predictions.add_prediction(attrs)

        elif name == "Error":
            # an error name only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        '''
            If the xml tree has been flagged as containing an error, 
            collect the error message in the body of the name
        '''
        if self.error is not None:
            self.error.set_message(content)
            