#
# 对csv进行处理，得到相应的数据，除了count为int类型，其他数据都是list
#

import pandas as pd


class DataProcess:

    def __init__(self, filename='directory.csv'):
        self._csv_file = pd.read_csv(filename)

        self._lon = self._csv_file['Longitude'].tolist()
        self._lat = self._csv_file['Latitude'].tolist()
        self._timezone = self._csv_file['Timezone'].tolist()
        self._country = self._csv_file['Country'].tolist()
        self._store_number = self._csv_file['Store Number'].tolist()
        self._store_name = self._csv_file['Store Name'].tolist()
        self._owner = self._csv_file['Ownership Type'].tolist()
        self._street = self._csv_file['Street Address'].tolist()
        self._city = self._csv_file['City'].tolist()
        self._state = self._csv_file['State/Province'].tolist()
        self._postcode = self._csv_file['Postcode'].tolist()
        self._phone = self._csv_file['Phone Number'].tolist()

        self._count = len(self._store_name)

        self._label = []
        for index in self._csv_file.index:
            self._label.append(str(self._store_name[index]) + '\n'
                               + str(self._street[index]) + '\n'
                               + 'Country: ' + str(self._country[index]) + '\n'
                               + 'State: ' + str(self._state[index]) + '\n'
                               + 'City: ' + str(self._city[index]) + '\n'
                               + 'Contact:' + str(self._phone[index]) + '\n'
                               + 'Lon: ' + str(self._lon[index]) + '  Lat: ' + str(self._lat[index]))

        self._word = []
        for index in self._csv_file.index:
            self._word.append(str(self._store_name[index]) + ' '
                               + str(self._street[index]) + ' '
                               + str(self._country[index]) + ' '
                               + str(self._state[index]) + ' '
                               + str(self._city[index]))

    def count(self):
        return self._count

    def label(self):
        return self._label

    def word(self):
        return self._word

    def lon(self):
        return self._lon

    def lat(self):
        return self._lat

    def country(self):
        return self._country

    def timezone(self):
        return self._timezone

    def store_number(self):
        return self._store_number

    def store_name(self):
        return self._store_name

    def owner(self):
        return self._owner

    def street(self):
        return self._street

    def city(self):
        return self._city

    def state(self):
        return self._state

    def postcode(self):
        return self._postcode

    def phone(self):
        return self._phone

