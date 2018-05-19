import sys
import heapq
import pandas as pd
import editdistance
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
        self._word = self._dp.word()

        self._index_list = []
        self._top_lon_list = []
        self._top_lat_list = []

    def set_values(self, klon, klat, k, word):
        self._index_list.clear()
        self._top_lon_list.clear()
        self._top_lat_list.clear()

        if word:
            self.word_topk_prs(klon, klat, k, word)
        else:
            self.topk_prs(klon, klat, k)

    def topk_prs(self, klon, klat, k):
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

    def word_topk_prs(self, klon, klat, k, word):
        matched_list = []
        sim_list = []
        matched = False
        for index in self._df.index:
            if self._word[index].find(word) != -1:
                matched_list.append(index)
                matched = True
            elif not matched:
                sim_dict = {}
                edit_dis = sys.maxsize
                for item in self._word[index].split():
                    tmp_dis = editdistance.eval(item, word)
                    if tmp_dis < edit_dis:
                        edit_dis = tmp_dis

                dis = cd.haversine(klon, klat, self._lon[index], self._lat[index])

                sim_dict['index'] = index
                sim_dict['edit_dis'] = edit_dis
                sim_dict['dis'] = dis
                sim_list.append(sim_dict)



        distance_list = []
        if matched:
            for index in matched_list:
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
        else:
            most_similar_list = heapq.nsmallest(k, sim_list, key=lambda s: s['edit_dis'] + s['dis'] / 100000)
            for item in most_similar_list:
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
