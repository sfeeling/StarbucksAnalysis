import pandas as pd
import numpy as np
import matplotlib 
import numpy as np
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geonamescache

#统计不同密度区间的国家数量，显示柱状图

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

df=pd.read_csv('directory.csv')
gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
# print countries dictionary
# you really wanna do something more useful with the data...

country_num_dict = {}
country_num_dict['CN'] = 0
counts=df['Country'].value_counts()#统计每一个国家出现的次数
for k, v in counts.iteritems():
	#print(k,round(v/countries[k]['areakm2']*1000000))
	#将CN和TW的星巴克数量合在一起
	if k == 'CN' or k == 'TW':
		country_num_dict['CN'] += v
	elif not country_num_dict.__contains__(k):
		country_num_dict[k] = v


#计算每一个国家的星巴克商店分布的密度
country_den_dict = {}
for k, v in country_num_dict.items():
	if k != 'CN':
		country_den_dict[k] = round(v /countries[k]['areakm2'] * 1000000)
	else:
		country_den_dict['CN'] = round(v / (countries['CN']['areakm2'] + countries['TW']['areakm2']) * 1000000)

#print(country_den_dict)

den_levels = [0, 0, 0, 0, 0]

for k, v in country_den_dict.items():
	if v < 10:
		den_levels[0] += 1
	elif v < 100:
		den_levels[1] += 1
	elif v < 1000:
		den_levels[2] += 1
	elif v < 10000:
		den_levels[3] += 1
	else:
		den_levels[4] += 1


den_levels_x = ['0-10', '10-100', '100-1000', '1000-10000', '10000以上']
plt.bar(den_levels_x,den_levels,width = 0.5)
plt.xlabel('(数量/平方千米)*1000000')
plt.ylabel('国家数量')
plt.yticks(np.linspace(0,max(den_levels),(max(den_levels)/2)+1,endpoint = True))
plt.title('密度统计图')
plt.show()