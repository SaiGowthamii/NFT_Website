import pandas as pd
from pandas.io import json
import config as cg
from flask import jsonify


class Home:

    def __init__(self) -> None:
        pass

    def getnftDataForHome(self,trader_id):
        conn = cg.connect_to_mySQL()
        query = f"SELECT * FROM test.nft WHERE owner_id <> {trader_id}"
        self.df1 = pd.read_sql(query,conn)
        if not self.df1.empty:
            json_nft_data = self.df1.to_json(orient = "index")
            parsed_json = json.loads(json_nft_data)
            return json.dumps(parsed_json)