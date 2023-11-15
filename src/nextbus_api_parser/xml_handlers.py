"""
    Module contains XML handlers used to parse the XML 
    feed from the API into appropriate data classes
"""

from xml.sax import ContentHandler
from nextbus_api_parser.data_classes import Agency, Error, Predictions, Route


class AgencyListHandler(ContentHandler):
    """Class to parse XML data for a list of Agencies from the API"""
    def __init__(self):
        self.agencies = []
        self.error = None
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        """
        Method to process 'agency' tags in the xml tree

        Parameters
        ----------
        name : str
            title of XML element
        attrs : dict
            XML attributes describing the Agency
        """
        if name == "agency":
            self.agencies.append(Agency(attrs))

        elif name == "Error":
            # an error element only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        """
        Method to collect the error message, if the xml tree has been flagged as containing an error

        Parameters
        ----------
        content : any
            content of XML element
        """
        if self.error is not None:
            self.error.set_message(content)

class RouteListHandler(ContentHandler):
    """Class to parse XML data for a list of an Agency's Routes from the API"""
    def __init__(self):
        self.routes = []
        self.error = None
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        """
        Method to process 'route' tags in the xml tree

        Parameters
        ----------
        name : str
            title of XML element
        attrs : dict
            XML attributes describing the Route
        """
        if name == "route":
            self.routes.append(Route(attrs))

        elif name == "Error":
            # an error element only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        """
        Method to collect the error message, if the xml tree has been flagged as containing an error

        Parameters
        ----------
        content : any
            content of XML element
        """
        if self.error is not None:
            self.error.set_message(content)

class RouteDetailsHandler(ContentHandler):
    """Class to parse XML data for a detailed description of a Route from the API"""

    def __init__(self):
        # this boolean indicates whether the tree has reached the part where it's listing Directions
        # and the stops associated with them
        self.is_in_direction_tag = False
        self.error = None
        self.route = None
        self.direction_tag = False
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        """
        Method to process appropriate tags in the xml tree

        Parameters
        ----------
        name : str
            title of XML element
        attrs : dict
            XML attributes describing the Route
        """
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
            # an error element only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        """
        Method to collect the error message, if the xml tree has been flagged as containing an error

        Parameters
        ----------
        content : any
            content of XML element
        """
        if self.error is not None:
            self.error.set_message(content)

class PredictionsHandler(ContentHandler):
    """Class to parse XML data for a list of a Stop's Predictions from the API"""
    def __init__(self):
        self.error = None
        self.predictions = None
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        """
        Method to process appropriate tags in the xml tree

        Parameters
        ----------
        name : str
            title of XML element
        attrs : dict
            XML attributes describing the Agency
        """
        if name == "predictions":
            self.predictions = Predictions(attrs)

        elif name == "direction":
            self.predictions.add_direction(attrs)

        elif name == "prediction":
            self.predictions.add_predictions(attrs)

        elif name == "Error":
            # an error element only exists if there's an error, initialize the error object if so
            self.error = Error(attrs)

    def characters(self, content):
        """
        Method to collect the error message, if the xml tree has been flagged as containing an error

        Parameters
        ----------
        content : any
            content of XML element
        """
        if self.error is not None:
            self.error.set_message(content)
            