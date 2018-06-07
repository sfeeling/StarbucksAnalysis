import pandas as pd
import numpy as np
import matplotlib 
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geonamescache

#统计时区的店铺数量，显示柱状图

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

df=pd.read_csv('directory.csv')

timezone_dict = {}
for i in df['Timezone'].tolist():
	i = i.split()[0][3:]
	if not timezone_dict.__contains__(i):
		timezone_dict[i] = 1
	else:
		timezone_dict[i] += 1
#print(len(timezone_dict))
timezone_list = list(timezone_dict.keys())
timezone_list.sort()
timezone_val = list(timezone_dict.values())
plt.bar(timezone_list,timezone_val,width = 0.5)
plt.xlabel('时区(GTM)')
plt.ylabel('数量')
plt.title('时区密度分布图')
plt.show()

