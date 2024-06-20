from enum import Enum


class LatLongAltRef(Enum):
    LAT_DEG = 0  # Latitude in degrees
    LON_DEG = 1  # Longitude in degrees
    ALT_DEG = 2  # Altitude in degrees (??? unit)
    ALT_FTAGL = 3  # Altitude in feet above ground level
    ON_RUNWAY = 4  # On runway (boolean 1 or 0)
    ALT_IND = 5  # Indicated altitude
    LAT_ORIGIN = 6  # Latitude of the origin
    LON_ORIGIN = 7  # Longitude of the origin


# Explains which index corresponds to what in the parsed udp data
class UDPSentenceRef(Enum):
    LatLongAlt = 20
