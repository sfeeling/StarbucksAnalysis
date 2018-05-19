import pandas as pd
import calculate_distance as cd
from csv_process import DataProcess


def list_str_to_float(str_list):
    float_list = []
    for item in str_list:
        float_list.append(float(item))
    return float_list


class Radius:

    def __init__(self):
        self._radius = float()
        self._df = pd.read_csv('directory.csv')
        self._dp = DataProcess()
        self._lon = list_str_to_float(self._dp.lon())
        self._lat = list_str_to_float(self._dp.lat())

        self._radius_index_list = []
        self._radius_lon_list = []
        self._radius_lat_list = []

    def set_values(self, rlon, rlat, radius):
        self._radius_index_list.clear()
        self._radius_lon_list.clear()
        self._radius_lat_list.clear()

        for index in self._df.index:
            lon = self._lon[index]
            lat = self._lat[index]
            dis = cd.haversine(rlon, rlat, lon, lat)

            if dis < radius:
                self._radius_index_list.append(index)
                self._radius_lon_list.append(lon)
                self._radius_lat_list.append(lat)

    def index_list(self):
        return self._radius_index_list

    def radius_lon_list(self):
        return self._radius_lon_list

    def radius_lat_list(self):
        return self._radius_lat_list