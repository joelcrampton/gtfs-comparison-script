from enum import Enum, IntEnum

# trips.txt
class BikesAllowed(IntEnum):
    NO_INFORMATION = 0
    ALLOWED = 1
    NOT_ALLOWED = 2

# stop_times.txt
class CollectionType(IntEnum):
    REGULARY_SCHEDULED = 0
    NO_PICKUP = 1
    PHONE_AGENCY = 2
    COORDINATE_WITH_DRIVER = 3

# routes.txt, stop_times.txt
class Continuous(IntEnum):
    CONTINUOUS = 0
    NO_CONTINUOUS = 1
    PHONE_AGENCY = 2
    COORDINATE_WITH_DRIVER = 3

# trips.txt
class DirectionId(IntEnum):
    OUTBOUND = 0
    INBOUND = 1

class Emoji(Enum):
    TRAM = ':tram:'
    METRO = ':metro:'
    STEAM_LOCOMOTIVE = ':steam_locomotive:'
    BUS = ':bus:'
    FERRY = ':ferry:'
    LIGHT_RAIL = ':light_rail:'
    AERIAL_TRAMWAY = ':aerial_tramway:'
    MOUNTAIN_CABLEWAY = ':mountain_cableway:'
    TROLLEYBUS = ':trolleybus:'
    MONORAIL = ':monorail:'
    ARROW_UP = ':arrow_up:'
    ARROW_DOWN = ':arrow_down:'
    ARROW_LEFT = ':arrow_left:'
    ARROW_RIGHT = ':arrow_right:'
    WHITE_CHECK_MARK = ':white_check_mark:'
    X = ':x:'
    CALENDAR = ':calendar:'

# calendar_dates.txt
class ExceptionType(IntEnum):
    ADDED = 1
    REMOVED = 2

# stops.txt
class LocationType(IntEnum):
    STOP = 0
    STATION = 1
    ENTRANCE_EXIT = 2
    GENERIC_NODE = 3
    BOARDING_AREA = 4

# routes.txt
class RouteType(IntEnum):
    TRAM = 0
    METRO = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    LIGHT_RAIL = 5
    AERIAL_LIFT = 6
    FUNICULAR = 7
    TROLLEY_BUS = 11
    MONORAIL = 12
    SCHOOL_BUS = 712

    def get_emoji(self) -> str:
        match self:
            case RouteType.TRAM:
                return Emoji.TRAM
            case RouteType.METRO:
                return Emoji.METRO
            case RouteType.RAIL:
                return Emoji.STEAM_LOCOMOTIVE
            case RouteType.BUS | RouteType.SCHOOL_BUS:
                return Emoji.BUS
            case RouteType.FERRY:
                return Emoji.FERRY
            case RouteType.LIGHT_RAIL:
                return Emoji.LIGHT_RAIL
            case RouteType.AERIAL_LIFT:
                return Emoji.AERIAL_TRAMWAY
            case RouteType.FUNICULAR:
                return Emoji.MOUNTAIN_CABLEWAY
            case RouteType.TROLLEY_BUS:
                return Emoji.TROLLEYBUS
            case RouteType.MONORAIL:
                return Emoji.MONORAIL


# stop_times.txt
class Timepoint(IntEnum):
    APPROXIMATE = 0
    EXACT = 1

# stops.txt, trips.txt
class WheelchairAccess(IntEnum):
    NO_INFORMATION = 0
    ACCESSIBLE = 1
    NOT_ACCESSIBLE = 2