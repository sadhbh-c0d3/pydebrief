from .flightdata import FlightData
from .positions import Positions
from .interpolate import interpolate

def write_csv(path, flight_data):
    print('Writing {}...\n'.format(path))
    with open(path, 'w+') as fp:
        print('METADATA,CA_CSV.3', file=fp)
        print('GMT,{}'.format(flight_data.timestamp), file=fp)
        print('TAIL,{}'.format(flight_data.tail), file=fp)
        print('DATA,', file=fp)
        print(','.join(FlightData.headers), file=fp)
        #points = interpolate(flight_data.iter_points, steps=4)
        points = flight_data.iter_points
        for point in points:
            print(','.join(map('{:0.7}'.format, point)), file=fp)



