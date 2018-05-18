import pandas as pd

class DataProcess:
    def __init__(self, filename):
        self.stb_file = pd.read_csv('directory.csv')

    def col_list(self, col):
        return self.stb_file[col].tolist()
