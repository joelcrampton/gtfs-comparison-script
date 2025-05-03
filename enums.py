from enum import Enum

# trips.txt
class BikesAllowed(Enum):
    NO_INFORMATION = 0
    ALLOWED = 1
    NOT_ALLOWED = 2

# stop_times.txt
class CollectionType(Enum):
    REGULARY_SCHEDULED = 0
    NO_PICKUP = 1
    PHONE_AGENCY = 2
    COORDINATE_WITH_DRIVER = 3

# routes.txt, stop_times.txt
class Continuous(Enum):
    CONTINUOUS = 0
    NO_CONTINUOUS = 1
    PHONE_AGENCY = 2
    COORDINATE_WITH_DRIVER = 3

# calendar.txt
class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    def get_short_name(self) -> str:
        match self:
            case Day.MONDAY:
                return 'mon'
            case Day.TUESDAY:
                return 'tues'
            case Day.WEDNESDAY:
                return 'weds'
            case Day.THURSDAY:
                return 'thurs'
            case Day.FRIDAY:
                return 'fri'
            case Day.SATURDAY:
                return 'sat'
            case Day.SUNDAY:
                return 'sun'

    @classmethod
    def get_week(self) -> list:
        return [Day(i) for i in range(Day.MONDAY.value, Day.SUNDAY.value + 1)]
    
    @classmethod
    def get_weekdays(self) -> list:
        return self.get_week()[:5]
    
    @classmethod
    def get_weekends(self) -> list:
        return self.get_week()[5:]

# trips.txt
class DirectionId(Enum):
    OUTBOUND = 0
    INBOUND = 1

class Emoji(Enum):
    CALENDAR = chr(0x1F4C5)
    STEAM_LOCOMOTIVE = chr(0x1F682)
    METRO = chr(0x1F687)
    LIGHT_RAIL = chr(0x1F688)
    TRAM = chr(0x1F68A)
    BUS = chr(0x1F68C)
    TROLLEYBUS = chr(0x1F68E)
    MONORAIL = chr(0x1F69D)
    MOUNTAIN_CABLEWAY = chr(0x1F6A0)
    AERIAL_TRAMWAY = chr(0x1F6A1)
    FERRY = chr(0x26F4)
    WHITE_CHECK_MARK = chr(0x2705)
    X = chr(0x274C)
    ARROW_UP = chr(0x2B06) + chr(0xFE0F)
    ARROW_DOWN = chr(0x2B07) + chr(0xFE0F)

# calendar_dates.txt
class ExceptionType(Enum):
    ADDED = 1
    REMOVED = 2

# stops.txt
class LocationType(Enum):
    STOP = 0
    STATION = 1
    ENTRANCE_EXIT = 2
    GENERIC_NODE = 3
    BOARDING_AREA = 4

# routes.txt
class RouteType(Enum):
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
class Timepoint(Enum):
    APPROXIMATE = 0
    EXACT = 1

# stops.txt, trips.txt
class WheelchairAccess(Enum):
    NO_INFORMATION = 0
    ACCESSIBLE = 1
    NOT_ACCESSIBLE = 2