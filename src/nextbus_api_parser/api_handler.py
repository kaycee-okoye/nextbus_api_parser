"""
    Module contains the API handler class used in handling queries to
    the NextBus API
"""

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from nextbus_api_parser.xml_handlers import (
    AgencyListHandler,
    RouteListHandler,
    RouteDetailsHandler,
    PredictionsHandler,
)


class ApiHandler:
    """
    Class designed to query and parse the API for specific data.

    NOTE
    The parameters passed to the API are always Tags e.g. if you want
    to pass a specific bus stop to the API, you'd pass
    the tag associated with that bus stop to the API query.
    """

    DOMAIN = (
        "https://retro.umoiq.com/service/publicXMLFeed?"  # root url for all API calls
    )
    AGENCY_LIST_QUERY = (
        DOMAIN + "command=agencyList"
    )  # API query string to get available agencies
    ROUTE_LIST_QUERY = (
        DOMAIN + "command=routeList&a={}"
    )  # API query string to get routes associated
    # with an agency
    ROUTE_DETAILS_QUERY = (
        DOMAIN + "command=routeConfig&a={}&r={}"
    )  # API query string to get
    # details about route e.g. stops
    PREDICTIONS_QUERY = (
        DOMAIN + "command=predictions&a={}&r={}&s={}"
    )  # API query string to get
    # predictions for a specific bus stop

    def __init__(self):
        # Initialize xml parser and attach it to the class
        self.parser = make_parser()
        self.parser.setFeature(feature_namespaces, 0)

    def get_agencies(self):
        """
        Method to make an API call to get a list of available agencies

        Returns
        -------
        list[Agency]
            Available agencies
        """
        handler = AgencyListHandler()
        query = self.AGENCY_LIST_QUERY
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.agencies if (handler.error is None) else handler.error

    def get_routes(self, agency_tag):
        """
        Method to make an API call to get a list of routes associated with an agency

        Parameters
        ----------
        agency_tag : str
            NextBus API tag of the agency being queried

        Returns
        -------
        list[Route]
            Routes associated with the agency
        """
        handler = RouteListHandler()
        query = self.ROUTE_LIST_QUERY.format(agency_tag)
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.routes if (handler.error is None) else handler.error

    def get_route_details(self, agency_tag, route_tag):
        """
        Method to make an API call to get a detailed description of a specific route

        Parameters
        ----------
        agency_tag : str
            NextBus API tag of the agency being queried
        route_tag : str
            NextBus API tag of the route being queried

        Returns
        -------
        Route
            Detailed description of the queried route
        """
        handler = RouteDetailsHandler()
        query = self.ROUTE_DETAILS_QUERY.format(agency_tag, route_tag)
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.route if (handler.error is None) else handler.error

    def get_predictions(self, agency_tag, route_tag, stop_tag):
        """
        Method to make an API call to get bus predictions for a specific stop on a route

        Parameters
        ----------
        agency_tag : str
            NextBus API tag of the agency being queried
        route_tag : str
            NextBus API tag of the route being queried
        stop_tag : str
            NextBus API tag of the stop being queried

        Returns
        -------
        Predictions
            Header data and a list of bus predictions at a bus stop from the API
        """
        handler = PredictionsHandler()
        query = self.PREDICTIONS_QUERY.format(agency_tag, route_tag, stop_tag)
        self.parser.setContentHandler(handler)
        self.parser.parse(query)
        # if an error was flagged, return the error instead
        return handler.predictions if (handler.error is None) else handler.error
