import pandas as pd
from pandas.io import json
import config as cg

class Transaction:

    def __init__(self,trans_type,trans_time):
        self.trans_type = trans_type
        self.trans_time = trans_time