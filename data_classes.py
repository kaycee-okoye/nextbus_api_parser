'''
    This file contains all the data classes used to handle data from the API
'''

class Agency:
    "This is a class that stores the data of a specific agency in the API"
    def __init__(self, attributes):
        self.tag = get_value(attributes, 'tag') # a tag used to identify this agency by the API
        self.title = get_value(attributes, 'title') # the name of the agency
        self.region = get_value(attributes, 'regionTitle') # the region served by the agency
        self.short = get_value(attributes, 'shortTitle') # a shorter name for the agency
        # (not always available)

class Route:
    "This is a class that stores the data of a specific route in the API"
    def __init__(self, attributes, is_detailed = False):
        # If is_detailed is true, it's a Route Config call
        # i.e. a more detailed description of the route
        self.tag = get_value(attributes, 'tag') # tag used to identify this route by the API
        self.title = get_value(attributes, 'title') # the name of this route
        self.short = get_value(attributes, 'shortTitle') # a shorter name for the route
        if is_detailed is True:
            self.color = get_value(attributes, 'color') # the hex color associated with
            # this route by the API
            self.opposide_color = get_value(attributes, 'oppositeColor') # the hex color that
            # contrasts most with the hex color of this route

            # the below cordinates express the boundaries of the route
            self.lat_min = get_value(attributes, 'latMin')
            self.lat_max = get_value(attributes, 'latMax')
            self.lon_min = get_value(attributes, 'lonMin')
            self.lon_max = get_value(attributes, 'lonMax')

            self.stops = [] # a list of stops associated with this route
            self.directions = [] # a list of directions associated with this route
            self.paths = [] # a list cordinates that the route follows


    def add_stop(self, attributes, add_to_direction = False):
        '''
            A method to add a stop to a route. If add_to_direction is false, the stop is added
            to the list of stops associated in general with this route. Otherwise, the route is 
            being associated specifically to the last direction that was added to this route. 
            This is because of the structure of the XML tree
        '''
        if add_to_direction:
            self.directions[-1].add_stop(attributes)
        else:
            self.stops.append(Stop(attributes))

    def add_direction(self, attributes):
        "A method to add a direction to the list of directions associated with this route"
        self.directions.append(Direction(attributes))

    def add_path(self, attributes):
        "A method to add a path to the list of directions associated with this route"
        self.paths.append(Path(attributes))

    def add_point(self, attributes):
        '''
            A method to add a point specifically to the last path that was added to this route. 
            This is because of the structure of the XML tree
        '''
        self.paths[-1].add_point(attributes)

class Stop:
    "This is a class that stores the data of a specific bus stop in the API"
    def __init__(self, attributes):
        self.tag = get_value(attributes, 'tag') # a tag used to identify the bus stop by the API
        self.title = get_value(attributes, 'title') # the name of the bus stop
        self.short_title = get_value(attributes, 'shortTitle') # a shorter name of the bus stop
        self.stop_id = get_value(attributes, 'stopId', "unknown") # the bus stop number
        self.lat = get_value(attributes, 'lat') # geographical latitude of the bus stop
        self.lon = get_value(attributes, 'lon') # geographical longitude of the bus stop


class Direction:
    "This is a class that stores the data about the directions of a specific route in the API"
    def __init__(self, attributes):
        self.tag = get_value(attributes, 'tag') # a tag used to identify the route by the API
        self.title = get_value(attributes, 'title') # the name of the route
        self.name = get_value(attributes, 'name') # a simplified name of the route
        self.stops = [] # a list of stops associated with this route

    def add_stop(self, attributes):
        "Method to add a specific stop to this direction"
        self.stops.append(Stop(attributes))

class Path:
    "This is a class that stores the data about a Path associated with a specific route in the API"
    def __init__(self, attributes):
        self.points = [] # a list of points associated with this path
        self.attributes = attributes

    def add_point(self, point):
        "Method to add a specific point to this path"
        self.points.append(point)
       
class Point:
    "This is a class that stores the data of a specific geographical cordinate in the API"
    def __init__(self, attributes):
        self.lat = get_value(attributes, 'lat') # geographical latitude of this point
        self.lon = get_value(attributes, 'lon') # geographical longitude of this point

class Predictions:
    '''
        This is a class that stores header data along with a list of bus predictions
        at a specific bus stop from the API
    '''
    def __init__(self, attributes):
        self.agency_title = get_value(attributes, 'agencyTitle') # specific agency associated
        # with this stop
        self.route_tag = get_value(attributes, 'routeTag') # tag used to identify a specific
        #croute associated with this stop by the API
        self.route_title = get_value(attributes, 'routeTitle') # name of the specific route
        # associated with this stop
        self.stop_title = get_value(attributes, 'stopTitle') # name of the specific bus stop
        self.stop_tag = get_value(attributes, 'stopTag') # tag associated with a specific bus
        # stop by the API
        self.dir_title = get_value(attributes, 'dirTitleBecauseNoPredictions') # name of the
        # direction (only available if there's no predictions)
        self.directions = []

    def add_direction(self, attributes):
        '''
            Method to add a direction which contains bus predictions pertaining to that 
            direction for a specific bus stop
        '''
        self.directions.append(Directions(attributes))

    def add_predictions(self, attributes):
        "Add a bus prediction for a specific direction pertaining to a specific bus stop"
        self.directions[-1].add_predictions(attributes)

class Directions:
    "This a class that stores bus predictions for a direction serviced by a stop"
    def __init__(self, attributes):
        self.title = get_value(attributes, 'title') # name of the direction for the specific bus stop
        self.predictions = [] # list of predictions pertaining to this direction

    def add_predictions(self, attributes):
        "Method to add a prediction for this specific direction"
        self.predictions.append(Prediction(attributes))

class Prediction:
    "This is a class that stores data about specific bus prediction from the API"
    def __init__(self, attributes):
        self.seconds = get_value(attributes, 'seconds') # arrival time in seconds
        self.minutes = get_value(attributes, 'minutes') # arrival time in minutes
        self.epoch_time = get_value(attributes, 'epochTime') # arrival time in epoch
        self.is_departure = get_value(attributes, 'isDepature')
        self.block = get_value(attributes, 'block') # block number assigned to a vehicle
        self.dir_tag = get_value(attributes, 'dirTag') # tag associated with specific direction
        # by the API
        self.trip_tag = get_value(attributes, 'tripTag') # id of the trip
        self.branch = get_value(attributes, 'branch') # only for toronto TTC agency
        self.affected_by_layover = get_value(attributes, 'affectedByLayover')
        self.is_schedule_based = get_value(attributes, 'isScheduleBased')
        self.delayed = get_value(attributes, 'delayed')

class Error:
    "This is a class that stores data about error messages recieved from the API"
    def __init__(self, attributes):
        self.message = ""
        self.should_retry = get_value(attributes, "shouldRetry")
        # shouldRetry represents if the user should try making the call again after 10 seconds

    def set_message(self, chars):
        '''Method to set the actual error message provided by the API'''
        self.message = chars if chars is not None else "There was an error processing your request"

def get_value(attribute, key, default_text = ""):
    '''
        This funtion is used to extract a specific value from an xml attribute based on its key.
        If the key doesn't exist in the attribute, a default string is assigned. If the default
        string isn't provided; a blank string will be used
    '''
    return attribute[key] if key in attribute else default_text
