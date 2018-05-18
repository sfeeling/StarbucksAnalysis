import pandas as pd

df = pd.read_csv('directory.csv')
timezone = df['Timezone'].tolist()

time_dict = {}

for item in timezone:
    if not time_dict.__contains__(item.split()[0]):
        time_dict[item.split()[0]] = 1
    else:
        time_dict[item.split()[0]] += 1

count = []
for item in time_dict:
    count.append(time_dict[item])

print(time_dict.keys())
print(count)