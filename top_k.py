import heapq
import pandas as pd
import calculate_distance as cd
from csv_process import DataProcess


def list_str_to_float(str_list):
    float_list = []
    for item in str_list:
        float_list.append(float(item))
    return float_list


class TopK:

    def __init__(self):
        self._df = pd.read_csv('directory.csv')
        self._dp = DataProcess()
        self._lon = list_str_to_float(self._dp.lon())
        self._lat = list_str_to_float(self._dp.lat())

        dupdict = {}
        for item in self._dp.store_number():
            if not dupdict.__contains__(item):
                dupdict[item] = 1
            else:
                dupdict[item] += 1

        for k, v in dupdict.items():
            if v > 1:
                print(k)

        self._index_list = []
        self._top_lon_list = []
        self._top_lat_list = []

    def set_values(self, klon, klat, k):
        self._index_list.clear()
        self._top_lon_list.clear()
        self._top_lat_list.clear()
        distance_list = []

        for index in self._df.index:
            distance = {}
            lon = self._lon[index]
            lat = self._lat[index]
            dis = cd.haversine(klon, klat, lon, lat)

            # 设置字典的key-value
            distance['index'] = index
            distance['distance'] = dis

            distance_list.append(distance)

        smallest_list = heapq.nsmallest(k, distance_list, key=lambda s: s['distance'])
        for item in smallest_list:
            index = item['index']
            self._index_list.append(index)
            self._top_lon_list.append(self._lon[index])
            self._top_lat_list.append(self._lat[index])

    def index_list(self):
        return self._index_list

    def top_lon_list(self):
        return self._top_lon_list

    def top_lat_list(self):
        return self._top_lat_list