from . positions import Positions
from . track import Track

from typing import Tuple


# RadarBox gives all data as AGL
ground_alt = 319.0


class FlightData:
    def __init__(self, timestamp: int, tail: str, track: Track, positions: Positions):
        self.__timestamp = timestamp
        self.__tail = tail
        self.__track = track
        self.__positions = positions
    
    @property
    def timestamp(self) -> int:
        return self.__timestamp

    @property
    def tail(self) -> str:
        return self.__tail
    
    @property
    def iter_track(self):
        return iter(self.__track.data)

    @property
    def iter_positions(self):
        return iter(self.__positions.data)

    @property
    def iter_points(self):
        for (coord_from, coord_to), position in zip(self.__track.data, self.__positions.data):
            coord_ts = coord_from[0] - self.__timestamp
            ts_diff = position[0] - coord_ts
            if abs(ts_diff) > 0.00001:
                print("ERROR: Track does not match Positions 1-to-1")
                break
            coord_alt, coord_lat, coord_lon = coord_from[1:]
            pos_alt, pos_lat, pos_lon, pos_hdg = position[1:]
            avg_alt = (pos_alt + coord_alt) * 0.5
            avg_lat = (coord_lat + pos_lat) * 0.5
            avg_lon = (coord_lon + pos_lon) * 0.5
            alt_gps = ground_alt + avg_alt
            yield (coord_ts, alt_gps, avg_lat, avg_lon, pos_hdg, avg_alt)
            
    @classmethod
    @property
    def headers(cls) -> Tuple[str]:
        """ForeFlight.CloudAhoy style headers associated with data
        """
        return ('seconds/t','feet/Alt (gps)','degrees/lat','degrees/lon','degrees/HDG', 'ft baro/AltB')
