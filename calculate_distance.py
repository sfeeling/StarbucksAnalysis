from math import radians, cos, sin, asin, sqrt

def haversine(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians,[lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r #单位千米

'''
lon1,lat1 = (22.599578, 113.973129) #深圳野生动物园(起点）
lon2,lat2 = (22.6986848, 114.3311032) #深圳坪山站 (百度地图测距：38.3km)
d2 = haversine(lon1,lat1,lon2,lat2)
print(d2)
'''

