import heapq
import time
import pandas as pd
import calculate_distance as cd

# top-k查询

# 输入经纬度和k值
# while 1:
#     try:
#         lon1 = float(input('enter lon:'))
#         if not -180 <= lon1 <= 180:
#             continue
#         lat1 = float(input('enter lat:'))
#         if not -90 <= lat1 <= 90:
#             continue
#         k = int(input('enter the value of k:'))
#         break
#     except ValueError as e:
#         print(e)
#lon1 = float(input('enter lon:'))
#lat1 = float(input('enter lat:'))
#k = int(input('enter the value of k:'))

# 记录开始时间

# df = pd.read_csv('directory.csv')
# 创建列表，列表的元素为dict

# start = time.clock()
# distanceList = []
# for index in df.index:
#     distance = {}
#     lon2 = float(df.loc[index,'Longitude'])
#     lat2 = float(df.loc[index,'Latitude'])
#     dis = cd.haversine(lon1,lat1,lon2,lat2)
#     # 设置字典的key-value
#     distance['index'] = index
#     distance['distance'] = dis
#
#     distanceList.append(distance)
#
# smallestList = heapq.nsmallest(k, distanceList, key=lambda s: s['distance'])
# end = time.clock()  # 记录结束时间
# for item in smallestList:
#     print(item)  # item是字典，item['index']是对应的索引
# print("Running time : %s Seconds" % (end-start))

class TopK:

    def __init__(self):
        self.df = pd.read_csv('directory.csv')
        self.top_index_list = []
        self.top_lon_list = []
        self.top_lat_list = []

    def set_value(self, klon, klat, k):
        self.top_index_list.clear()
        self.top_lon_list.clear()
        self.top_lat_list.clear()
        start = time.clock()
        distanceList = []

        for index in self.df.index:
            distance = {}
            lon2 = float(self.df.loc[index, 'Longitude'])
            lat2 = float(self.df.loc[index, 'Latitude'])
            dis = cd.haversine(klon, klat, lon2, lat2)
            # 设置字典的key-value
            distance['index'] = index
            distance['distance'] = dis
            distance['Longitude'] = lon2
            distance['Latitude'] = lat2

            distanceList.append(distance)

        smallestList = heapq.nsmallest(k, distanceList, key=lambda s: s['distance'])
        end = time.clock()  # 记录结束时间
        for item in smallestList:
            self.top_index_list.append(item['index'])
            self.top_lon_list.append(item['Longitude'])
            self.top_lat_list.append(item['Latitude'])

    def get_top_index_list(self):
        return self.top_index_list

    def get_top_lon_list(self):
        return self.top_lon_list

    def get_top_lat_list(self):
        return self.top_lat_list