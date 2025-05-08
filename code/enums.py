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
    TRAM = chr(0x1F68B) # :tram:
    METRO = chr(0x1F687) # :metro:
    STEAM_LOCOMOTIVE = chr(0x1F682) # :steam_locomotive:
    BUS = chr(0x1F68C) # :bus:
    FERRY = chr(0x26F4) # :ferry:
    LIGHT_RAIL = chr(0x1F688) # :light_rail:
    AERIAL_TRAMWAY = chr(0x1F6A1) # :aerial_tramway:
    MOUNTAIN_CABLEWAY = chr(0x1F6A0) # :mountain_cableway:
    TROLLEYBUS = chr(0x1F68E) # :trolleybus:
    MONORAIL = chr(0x1F69D) # :monorail:
    ARROW_UP = chr(0x2B06) + chr(0xFE0F) # :arrow_up:
    ARROW_DOWN = chr(0x2B07) + chr(0xFE0F) # :arrow_down:
    WHITE_CHECK_MARK = chr(0x2705) # :white_check_mark:
    X = chr(0x274C) # :x:
    CALENDAR = chr(0x1F4C5) # :calendar:

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

class TripDifference(IntEnum):
    SEQUENCE = 0
    NO_DIFFERENCE = 1
    DURATION = 2
    DEPARTURE_TIME = 3

# stops.txt, trips.txt
class WheelchairAccess(IntEnum):
    NO_INFORMATION = 0
    ACCESSIBLE = 1
    NOT_ACCESSIBLE = 2