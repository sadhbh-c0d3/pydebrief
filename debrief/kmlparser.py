import xml.etree.ElementTree as ET

from typing import Optional

from .flightdata import FlightData
from .positions import Positions
from .track import Track


ns = '{http://www.opengis.net/kml/2.2}'

one_meter_in_feet = 3.2808399


def parse_timestamp(timestamp: str) -> float:
    """Convert millisecond timestamp value into floating point seconds
    """
    return float(timestamp) * 0.001


def parse_feet(feet: Optional[str]) -> Optional[float]:
    """Strip feet floating point value from 'ft' unit, e.g. '750 ft' becomes 750.0
    """
    if feet and feet.endswith('ft'):
        return float(feet[:-2])


def parse_degrees(degrees: Optional[str]) -> Optional[float]:
    """Strip degrees floating point value from '°' character, e.g. '250°' becomes 250.0
    """
    if degrees and degrees.endswith('°'):
        return float(degrees[:-1])


def parse_latitude(lat_degrees: float) -> float:
    """Parse latitude as floating point value 
    """
    return float(lat_degrees)


def parse_longtitude(lon_degrees: float) -> float:
    """Parse longtitude as floating point value
    """
    return float(lon_degrees)


def parse_altitude(alt_gps: Optional[str]) -> Optional[float]:
    if alt_gps:
        return float(alt_gps) * one_meter_in_feet


def parse_coordinates(timestamp, coord):
    coord = coord.split(',')
    return (
        parse_timestamp(timestamp),
        parse_altitude(coord[2]),
        parse_latitude(coord[1]),
        parse_longtitude(coord[0])
    )


def parse_positions(xFolder):
    """Parse Positions Folder of KML in AirNav.RadarBox format
    """
    positions = Positions()

    for xPlacemark in xFolder.iter(ns + 'Placemark'):
        xName = next(xPlacemark.iter(ns + 'name'))
        timestamp = xName.text
        xExtendedData = next(xPlacemark.iter(ns + 'ExtendedData'))

        values = dict()
        for xData in xExtendedData.iter(ns + 'Data'):
            key = xData.attrib['name']
            xValue = next(xData.iter(ns + 'value'))
            value = xValue.text
            values[key] = value

        positions.add_position(
            parse_timestamp(timestamp),
            parse_feet(values.get('fal')),
            parse_latitude(values['lat']),
            parse_longtitude(values['lon']),
            parse_degrees(values.get('fhd'))
        )

    return positions


def parse_track(xFolder):
    """Parse Track Folder of KML in AirNav.RadarBox format
    """
    track = Track()
    
    for xPlacemark in xFolder.iter(ns + 'Placemark'):
        xName = next(xPlacemark.iter(ns + 'name'))
        t_from, t_to = xName.text.split('-')

        xLineString = next(xPlacemark.iter(ns + 'LineString'))
        xCoordinates = next(xLineString.iter(ns + 'coordinates'))
        coord_from, coord_to = xCoordinates.text.split(' ')
        coord_from = parse_coordinates(t_from, coord_from)
        coord_to = parse_coordinates(t_to, coord_to)

        track.add_segment(coord_from, coord_to)

    return track

def parse_kml(path):
    """Parse KML in AirNav.RadarBox format
    """
    tree = ET.parse(path)
    root = tree.getroot()
    xDocument = next(root.iter(ns + 'Document'))

    xTail = next(xDocument.iter(ns + 'name'))
    tail = xTail.text.split()[0]
    print('Found flight {}'.format(tail))

    for xFolder in xDocument.iter(ns + 'Folder'):
        xName = next(xFolder.iter(ns + 'name'))

        if xName.text == 'Track':
            print('Parsing track...')
            track = parse_track(xFolder)

        if xName.text == 'Positions':
            print('Parsing positions...')
            positions = parse_positions(xFolder)

    return FlightData(positions.start, tail, track, positions)

