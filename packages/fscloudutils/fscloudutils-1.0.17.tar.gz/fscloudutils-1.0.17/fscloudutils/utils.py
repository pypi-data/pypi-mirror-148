"""
This module holds various useful tools
"""

import traceback
from datetime import datetime
import pandas as pd
from typing import Tuple
import exceptions


class NavRowData:
    def __init__(self, lat, long):
        self._lat = lat
        self._long = long
        self._satellites_count = 0
        self._speed_kmh = 0
        self._direction_mag = None
        self._direction_true = None
        self._talkerID = None

    def get_lat(self):
        return self._lat

    def get_long(self):
        return self._long

    def set_talkerID(self, talkerID):
        self._talkerID = talkerID

    def get_talkerID(self):
        return self._talkerID

    def set_direction_true(self, direction_true):
        self._direction_true = direction_true

    def get_direction_true(self):
        return self._direction_true

    def set_direction_mag(self, direction_mag):
        self._direction_mag = direction_mag

    def get_direction_mag(self):
        return self._direction_mag

    def set_speed_kmh(self, speed_kmh):
        self._speed_kmh = speed_kmh

    def get_speed_kmh(self):
        return self._speed_kmh

    def set_satellites_count(self, satellites_count):
        self._satellites_count = satellites_count

    def get_satellites_count(self):
        return self._satellites_count


class NavParser:
    """ nav_reader is a class implementing methods to read .nav files in NMEA format """

    def __init__(self, path):
        """
        :param path:
        """
        super()
        self._points = dict()
        self.read_file(path)

    @staticmethod
    def get_final_lat_long(lat_before_conversion, long_before_conversion, lat_dir, long_dir) -> Tuple[float, float]:
        lat_dec = lat_before_conversion // 100
        long_dec = long_before_conversion // 100
        lat_partial = ((lat_before_conversion / 100 - lat_dec) * 100) / 60
        long_partial = ((long_before_conversion / 100 - long_dec) * 100) / 60
        final_lat = lat_dec + lat_partial
        final_long = long_dec + long_partial
        if lat_dir == 'S':
            final_lat = final_lat * -1
        if long_dir == 'W':
            final_long = final_long * -1
        return final_lat, final_long

    def read_file(self, path: str) -> None:
        if not path.split('.')[-1] == 'nav':
            print('you should only use .nav file formats, please try again')
            raise exceptions.FileExtensionError('nav')
        else:
            with open(path, 'r') as f:
                read_data = f.readlines()
                lat, long = None, None
                for line in read_data:
                    data = line.split(',')
                    if len(data) <= 6:
                        continue

                    talkerID = data[0][1:3]  # $GPGGA -> GP
                    sentenceID = data[0][3:]  # $GPGGA -> GGA

                    if sentenceID == "GGA":
                        lat_before_conversion = float(data[2])
                        long_before_conversion = float(data[4])
                        lat_dir, long_dir = data[3], data[5]
                        lat, long = NavParser.get_final_lat_long(lat_before_conversion, long_before_conversion,
                                                                 lat_dir, long_dir)
                        if (lat, long) not in self._points:
                            self._points[lat, long] = NavRowData(lat, long)
                            self._points[lat, long].set_talkerID(talkerID)

                        self._points[lat, long].set_satellites_count(int(data[7]))

                    elif sentenceID == "RMC":
                        lat_before_conversion = float(data[3])
                        long_before_conversion = float(data[5])
                        speed_kmh = 1.852 * float(data[7])
                        lat_dir, long_dir = data[4], data[6]
                        lat, long = NavParser.get_final_lat_long(lat_before_conversion, long_before_conversion,
                                                                 lat_dir, long_dir)
                        if (lat, long) not in self._points:
                            self._points[lat, long] = NavRowData(lat, long)
                            self._points[lat, long].set_talkerID(talkerID)

                        self._points[lat, long].set_speed_kmh(speed_kmh)

                    if lat is None or long is None:
                        continue
                    if (lat, long) not in self._points:
                        self._points[lat, long] = NavRowData(lat, long)
                        self._points[lat, long].set_talkerID(talkerID)

                    if sentenceID == "VTG":
                        self._points[lat, long].set_direction_true(data[1])
                        self._points[lat, long].set_direction_mag(data[3])
                        self._points[lat, long].set_speed_kmh(float(data[7]))

    def get_points(self) -> dict:  # getter function
        return self._points

    def get_most_accurate_point(self):
        return max(self._points, key=lambda s: self._points[s].get_satellites_count())