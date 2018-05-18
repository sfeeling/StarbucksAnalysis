import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#统计各个国家星巴克的数量，显示柱状图

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

Location = r'./directory.csv'
df = pd.read_csv(Location)
#为每一个记录添加数值为1的的项，方便统计数量
num = [ 1 for i in range(len(df['Country']))]
df['num'] = pd.Series(num,index = df.index)
#将国家名相同的记录分组并统计总数，创建一个groupby对象
country = df.groupby('Country')
df = country['num'].sum()


#设置条形图的x轴和y轴的序列值，以及条形的宽度
plt.bar(df.index,df,width = 0.5)
#设置x，y轴的标签
plt.xlabel('国家')
plt.ylabel('数量')
#plt.ylim((0,np.max(df)))
#设置y轴的范围和刻度
plt.yticks(np.arange(0,np.max(df)+500,500))
plt.title('国家分布数量图')
plt.show()