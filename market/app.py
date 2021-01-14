import os
import json
from pymongo import MongoClient
from .twelvedata.service import TDClient
from .market_data import DataClient

dirname = os.path.dirname(__file__)
cred = os.path.join(dirname, "credentials.json")

with open(cred) as f:
    apikey = json.load(f)["apikey"]

client = MongoClient()
db = client.capiDB

td = TDClient(apikey=apikey)


def run():
    create_collections()
    meta = db.symbols.find_one({"symbol": "AAPL"})
    dc = DataClient(db, td)
    dc.update_hr(meta)


def create_collections():
    collections = db.list_collection_names()
    if "symbols" not in collections:
        col = db.symbols
        col.create_index([("symbol", 1)])
        col.create_index([("update_date", -1)])

    if "prices" not in collections:
        col = db.prices
        col.create_index([("symbol_id", 1), ("d", -1)])
