"""
    Module contains the data classes used to handle data from the API
"""


class Agency:
    """
    Data class that stores the data of an agency in the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Agency
    """

    def __init__(self, attributes):
        # a tag used to identify this agency by the API
        self.tag = get_xml_atrribute_value(attributes, "tag")
        # the name of the agency
        self.title = get_xml_atrribute_value(attributes, "title")
        # the region served by the agency
        self.region = get_xml_atrribute_value(attributes, "regionTitle")
        # a shorter name for the agency (not always available)
        self.short = get_xml_atrribute_value(attributes, "shortTitle")


class Route:
    """
    Data class that stores the data of a route in the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Route
    is_detailed : bool, optional
        If is_detailed is True, it's a Route Config call i.e. a more detailed description
        of the route, by default False
    """

    def __init__(self, attributes, is_detailed=False):
        self.tag = get_xml_atrribute_value(
            attributes, "tag"
        )  # tag used to identify this route by the API
        self.title = get_xml_atrribute_value(
            attributes, "title"
        )  # the name of this route
        self.short = get_xml_atrribute_value(
            attributes, "shortTitle"
        )  # a shorter name for the route
        if is_detailed is True:
            self.color = get_xml_atrribute_value(
                attributes, "color"
            )  # the hex color associated with
            # this route by the API
            self.opposide_color = get_xml_atrribute_value(
                attributes, "oppositeColor"
            )  # the hex color that
            # contrasts most with the hex color of this route

            # the below cordinates express the boundaries of the route
            self.lat_min = get_xml_atrribute_value(attributes, "latMin")
            self.lat_max = get_xml_atrribute_value(attributes, "latMax")
            self.lon_min = get_xml_atrribute_value(attributes, "lonMin")
            self.lon_max = get_xml_atrribute_value(attributes, "lonMax")

            self.stops = []  # a list of stops associated with this route
            self.directions = []  # a list of directions associated with this route
            self.paths = []  # a list cordinates that the route follows

    def add_stop(self, attributes, add_to_direction=False):
        """
        Method to add a stop to a route

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Stop
        add_to_direction : bool, optional
            If add_to_direction is false, the stop is added
            to the list of stops associated in general with this route. Otherwise, the route is
            being associated specifically to the last direction that was added to this route.
            This is because of the structure of the XML tree, by default False
        """
        if add_to_direction:
            self.directions[-1].add_stop(attributes)
        else:
            self.stops.append(Stop(attributes))

    def add_direction(self, attributes):
        """
        Method to add a direction to the list of directions associated with this route

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Direction
        """
        self.directions.append(Direction(attributes))

    def add_path(self, attributes):
        """
        Method to add a path to the list of directions associated with this route

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Path
        """
        self.paths.append(Path(attributes))

    def add_point(self, attributes):
        """
        Method to add a point specifically to the last path that was added to this route.
        This is because of the structure of the XML tree

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Point
        """
        self.paths[-1].add_point(attributes)


class Stop:
    """
    Data class that stores the data of a specific bus stop in the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Stop
    """

    def __init__(self, attributes):
        self.tag = get_xml_atrribute_value(
            attributes, "tag"
        )  # a tag used to identify the bus stop by the API
        self.title = get_xml_atrribute_value(
            attributes, "title"
        )  # the name of the bus stop
        self.short_title = get_xml_atrribute_value(
            attributes, "shortTitle"
        )  # a shorter name of the bus stop
        self.stop_id = get_xml_atrribute_value(
            attributes, "stopId", "unknown"
        )  # the bus stop number
        self.lat = get_xml_atrribute_value(
            attributes, "lat"
        )  # geographical latitude of the bus stop
        self.lon = get_xml_atrribute_value(
            attributes, "lon"
        )  # geographical longitude of the bus stop


class Direction:
    """
    Data class that stores the data about the directions of a specific route in the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Direction
    """

    def __init__(self, attributes):
        self.tag = get_xml_atrribute_value(
            attributes, "tag"
        )  # a tag used to identify the route by the API
        self.title = get_xml_atrribute_value(
            attributes, "title"
        )  # the name of the route
        self.name = get_xml_atrribute_value(
            attributes, "name"
        )  # a simplified name of the route
        self.stops = []  # a list of stops associated with this route

    def add_stop(self, attributes):
        """
        Method to add a specific stop to this direction

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Stop
        """
        self.stops.append(Stop(attributes))


class Path:
    """
    Data class that stores the data about a Path associated with a specific route in the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Path
    """

    def __init__(self, attributes):
        self.points = []  # a list of points associated with this path
        self.attributes = attributes

    def add_point(self, point):
        """
        Method to add a specific point to this path

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Point
        """
        self.points.append(point)


class Point:
    """
    Data class that stores the data of a specific geographical cordinate in the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Point
    """

    def __init__(self, attributes):
        self.lat = get_xml_atrribute_value(
            attributes, "lat"
        )  # geographical latitude of this point
        self.lon = get_xml_atrribute_value(
            attributes, "lon"
        )  # geographical longitude of this point


class Predictions:
    """
    Data class that stores header data and a list of bus predictions at a bus stop from the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Predictions
    """

    def __init__(self, attributes):
        self.agency_title = get_xml_atrribute_value(
            attributes, "agencyTitle"
        )  # specific agency associated
        # with this stop
        self.route_tag = get_xml_atrribute_value(
            attributes, "routeTag"
        )  # tag used to identify a specific
        # croute associated with this stop by the API
        self.route_title = get_xml_atrribute_value(
            attributes, "routeTitle"
        )  # name of the specific route
        # associated with this stop
        self.stop_title = get_xml_atrribute_value(
            attributes, "stopTitle"
        )  # name of the specific bus stop
        self.stop_tag = get_xml_atrribute_value(
            attributes, "stopTag"
        )  # tag associated with a specific bus
        # stop by the API
        self.dir_title = get_xml_atrribute_value(
            attributes, "dirTitleBecauseNoPredictions"
        )  # name of the
        # direction (only available if there's no predictions)
        self.directions = []

    def add_direction(self, attributes):
        """
        Method to add a direction which contains bus predictions pertaining to that
            direction for a specific bus stop

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Direction
        """
        self.directions.append(Directions(attributes))

    def add_predictions(self, attributes):
        """
        Method to add a bus prediction for a specific direction pertaining to a specific bus stop

        Parameters
        ----------
        attributes : dict
            XML attributes describing the Direction
        """
        self.directions[-1].add_predictions(attributes)


class Directions:
    """
    Data class that stores bus predictions for a direction serviced by a stop

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Directions
    """

    def __init__(self, attributes):
        self.title = get_xml_atrribute_value(
            attributes, "title"
        )  # name of the direction for the specific bus
        # stop
        self.predictions = []  # list of predictions pertaining to this direction

    def add_predictions(self, attributes):
        "Method to add a prediction for this specific direction"
        self.predictions.append(Prediction(attributes))


class Prediction:
    """
    Data class that stores data about specific bus prediction from the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Prediction
    """

    def __init__(self, attributes):
        self.seconds = get_xml_atrribute_value(
            attributes, "seconds"
        )  # arrival time in seconds
        self.minutes = get_xml_atrribute_value(
            attributes, "minutes"
        )  # arrival time in minutes
        self.epoch_time = get_xml_atrribute_value(
            attributes, "epochTime"
        )  # arrival time in epoch
        self.is_departure = get_xml_atrribute_value(attributes, "isDepature")
        self.block = get_xml_atrribute_value(
            attributes, "block"
        )  # block number assigned to a vehicle
        self.dir_tag = get_xml_atrribute_value(
            attributes, "dirTag"
        )  # tag associated with specific direction
        # by the API
        self.trip_tag = get_xml_atrribute_value(attributes, "tripTag")  # id of the trip
        self.branch = get_xml_atrribute_value(
            attributes, "branch"
        )  # only for toronto TTC agency
        self.affected_by_layover = get_xml_atrribute_value(
            attributes, "affectedByLayover"
        )
        self.is_schedule_based = get_xml_atrribute_value(attributes, "isScheduleBased")
        self.delayed = get_xml_atrribute_value(attributes, "delayed")


class Error:
    """
    Data class that stores data about error messages recieved from the API

    Parameters
    ----------
    attributes : dict
        XML attributes describing the Error
    """

    def __init__(self, attributes):
        self.message = ""
        self.should_retry = get_xml_atrribute_value(attributes, "shouldRetry")
        # shouldRetry represents if the user should try making the call again after 10 seconds

    def set_message(self, chars):
        """
        Method to set the error message provided by the API

        Parameters
        ----------
        chars : str
            Error message provided by the API, defaults to
            'There was an error processing your request' if None was provided.
        """
        self.message = (
            chars if chars is not None else "There was an error processing your request"
        )


def get_xml_atrribute_value(attribute, key, default_text=""):
    """
    Funtion to safely extract a value from an xml attribute dict based on the attribute name.

    Parameters
    ----------
    attribute : dict
        XML attributes to extract value from
    key : any
        desired attribute name
    default_text : str, optional
        _description_, by default ""

    Returns
    -------
    any
        If the attribute doesn't exist in the attribute dict, a default string is returned.
        If the default string wasn't provided; a blank string will be returned
    """
    return attribute[key] if key in attribute else default_text
