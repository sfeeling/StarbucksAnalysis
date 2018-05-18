import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geonamescache

#统计国家数量，绘制饼状图

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

Location = r'./directory.csv'
df = pd.read_csv(Location)

#为每一个记录添加数值为1的的项，方便统计数量
#num = [ 1 for i in range(len(df['Country']))]
df['num'] = pd.Series(1,index = df.index)
#将国家名相同的记录分组并统计总数，创建一个groupby对象
country = df.groupby('Country',as_index = False)
coun_list = country['num'].sum()



Sorted = coun_list.sort_values(by = 'num',ascending = False)
#前五个最多的国家
Result = Sorted.head()



last = sum(coun_list['num']) - sum(Result['num'])
r = Result.append({'Country' : 'Others','num' : last},ignore_index = True)

num_list = list(r['num'])
country_list = list(r['Country'])

i = 0
while i < 5:
	country_list[i] = countries[country_list[i]]['name']
	i += 1

plt.pie(num_list,labels = country_list,startangle = 90,autopct = '%1.1f%%')
plt.title('数量分布饼状图')
plt.show()