import pandas as pd
import geonamescache

stb_file=pd.read_csv('directory.csv')
gnc = geonamescache.GeonamesCache()
countries = gnc.get_countries()

counts=stb_file['Country'].value_counts()
country_dict = {}
for k, v in counts.iteritems():
	#print(k, round(v/countries[k]['areakm2']*1000000))
    country_dict[countries[k]['iso3']] = round(v/countries[k]['areakm2']*1000000)

print(country_dict['JPN'])
