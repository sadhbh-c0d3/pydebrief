from typing import Optional, Tuple

class Positions:
    def __init__(self):
        self.__points = []
        self.__start = None

    def add_position(self,
            time_seconds: float,
            alt_feet: Optional[float],
            lat_degrees: float,
            lon_degrees: float,
            hdg_degrees: Optional[float]):

        # Record timestamp of initial point
        if self.__start is None:
            self.__start = int(time_seconds)

        if alt_feet is None:
            print('Warning: Missing altitude for: {}'.format(time_seconds))

        if hdg_degrees is None:
            print('Warning: Missing heading for: {}'.format(time_seconds))

        self.__points.append((time_seconds - self.__start, alt_feet, lat_degrees, lon_degrees, hdg_degrees))
        
        # Auto-correct missing altitude or heading
        if 3 < len(self.__points) and (None in self.__points[-2]):

            if self.__points[-2][1] is None:
                self.__points[-2] = (
                     self.__points[-2][0], 
                    (self.__points[-3][1] + self.__points[-1][1]) * 0.5,
                    *self.__points[-2][2:])

            if self.__points[-2][4] is None:
                self.__points[-2] = (
                    *self.__points[-2][:4], 
                    (self.__points[-3][4] + self.__points[-1][4]) * 0.5)
            
            print('Auto-Corrected Positions')
            print(self.__points[-3])
            print(self.__points[-2])
            print(self.__points[-1])

    @property
    def start(self) -> int:
        return self.__start

    @property
    def data(self) -> Tuple[float, float, float, float, float]:
        return self.__points

    @classmethod
    @property
    def headers(cls) -> Tuple[str]:
        """ForeFlight.CloudAhoy style headers associated with data
        """
        # It's actually AGL and not GPS alt 'feet/Alt (gps)'
        return ('seconds/t','ft baro/AltB','degrees/lat','degrees/lon','degrees/HDG')


