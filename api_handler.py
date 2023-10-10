'''
    This file contains the API handler class used in handling queries to
    the NextBus API
'''

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml_handlers import AgencyListHandler, RouteListHandler
from xml_handlers import RouteDetailsHandler, PredictionsHandler

class ApiHandler:
    '''
        A class designed to query the API for specific data and
        then parse the response using the appropriate XML handler.
        After parsing the XML response, the required object(s) will be returned.

        Note that the parameters passed to the API are always Tags
        e.g. if you want to pass a specific bus stop to the API, you'd pass
        the tag associated with that bus stop to the API query.
    '''
    domain = 'https://retro.umoiq.com/service/publicXMLFeed?' # root url for all API calls
    agencyListQuery = domain + 'command=agencyList' # API query string to get available agencies
    routeListQuery = domain + 'command=routeList&a={}' # API query string to get routes associated
    # with an agency
    routeDetailsQuery = domain +  'command=routeConfig&a={}&r={}' # API query string to get details
    # about route e.g. stops
    predictionQuery = domain + 'command=predictions&a={}&r={}&s={}' # API query string to get
    # predictions for a specific bus stop

    def __init__(self):
        # Initialize xml parser and attach it to the class
        self.parser = make_parser()
        self.parser.setFeature(feature_namespaces, 0)

    def get_agencies(self):
        "Make API call to get a list of available agencies"
        handler = AgencyListHandler()
        query = self.agencyListQuery
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.agencies if (handler.error is None) else handler.error

    def get_routes(self, agency):
        "Make API call to get a list of routes associated with an agency"
        handler = RouteListHandler()
        query = self.routeListQuery.format(agency)
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.routes if (handler.error is None) else handler.error

    def get_route_details(self, agency, route):
        "Make API call to get a detailed description of a specific route"
        handler = RouteDetailsHandler()
        query = self.routeDetailsQuery.format(agency, route)
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.route if (handler.error is None) else handler.error

    def get_predictions(self, agency, route, stop):
        "Make API call to get bus predictions for a specific bus stop associated with a route"
        handler = PredictionsHandler()
        query = self.predictionQuery.format(agency, route, stop)
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.predictions if (handler.error is None) else handler.error
