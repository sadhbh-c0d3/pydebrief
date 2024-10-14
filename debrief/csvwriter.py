from .flightdata import FlightData
from .positions import Positions
from .interpolate import interpolate

def write_csv(path, flight_data, interpolation_steps=None):
    print('Writing {}...\n'.format(path))
    with open(path, 'w+') as fp:
        print('METADATA,CA_CSV.3', file=fp)
        print('GMT,{}'.format(flight_data.timestamp), file=fp)
        print('TAIL,{}'.format(flight_data.tail), file=fp)
        print('DATA,', file=fp)
        print(','.join(FlightData.headers), file=fp)
        points = flight_data.iter_points
        if interpolation_steps:
            points = interpolate(points, steps=interpolation_steps)
        for point in points:
            print(','.join(map('{:0.7}'.format, point)), file=fp)



