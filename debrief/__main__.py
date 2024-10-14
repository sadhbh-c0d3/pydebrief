import sys

from . kmlparser import parse_kml
from . csvwriter import write_csv

_, inFile, outFile = sys.argv
print('Will process {} to {}'.format(inFile, outFile))
flight_data = parse_kml(inFile)
write_csv(outFile, flight_data)
