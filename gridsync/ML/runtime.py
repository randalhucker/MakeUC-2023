import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import DataBase as db

class Model:
    def __init__(self):
        self.data = pd.DataFrame()

    def load_data(self, data):
        entry = 0
        while (entry != None):
            entry = db.get_records(data)
            if (entry != None):
                self.data = self.data.append(entry, ignore_index=True)
