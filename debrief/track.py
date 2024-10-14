from typing import Optional, Tuple

class Track:
    def __init__(self):
        self.__segments = []
    
    def add_segment(self,
            coord_from: Tuple[float, Optional[float], float, float],
            coord_to: Tuple[float, Optional[float], float, float]
        ):

        self.__segments.append((coord_from, coord_to))

        if 3 < len(self.__segments) and (self.__segments[-2][0][1] is None or self.__segments[-2][1][1] is None):
            for i in range(2):
                if self.__segments[-2][i][1] is None:
                    self.__segments[-2] = (
                        *self.__segments[-2][:i],
                        (
                            *self.__segments[-2][i][:1],
                            (self.__segments[-3][i][1] + self.__segments[-1][i][1]) * 0.5,
                            *self.__segments[-2][i][2:]
                        ),
                        *self.__segments[-1][i+1:])
            print('Auto-Corrected Track Segments')
            print(self.__segments[-3])
            print(self.__segments[-2])
            print(self.__segments[-1])
    
    @property
    def data(self) -> Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float]]:
        return self.__segments

    @classmethod
    @property
    def headers(cls) -> Tuple[str]:
        """ForeFlight.CloudAhoy style headers associated with data
        """
        return (('seconds/t','feet/Alt (gps)','degrees/lat','degrees/lon'),) * 2
