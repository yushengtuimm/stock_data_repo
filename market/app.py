import os
import json
import requests
import time
import itertools
import concurrent.futures
from datetime import datetime, timedelta, date
from pymongo import MongoClient
from .twelvedata.service import TDClient
from .market_data import DataClient
from .algorithm import VolatilityIndicator

import pandas as pd
import numpy as np
from pprint import pprint

dirname = os.path.dirname(__file__)
cred = os.path.join(dirname, "credentials.json")

with open(cred) as f:
    apikey = json.load(f)["apikey"]

client = MongoClient()
db = client.capiDB
finance = client.finance

td = TDClient(apikey=apikey)
api_limit = 55

john = ["XONE", "NNDM", "IPOE", "PLTR", "MU", "BABA", "TSM", "GOOG"]
jen = [
    "AAPL",
    "AMD",
    "ARKG",
    "ARKK",
    "ARKQ",
    "CGC",
    "COUP",
    "ETSY",
    "FB",
    "IPOE",
    "JD",
    "JMIA",
    "MJ",
    "MSFT",
    "NIO",
    "NNDM",
    "OKTA",
    "PINS",
    "PLTR",
]


def run():
    create_collections()

    # full_update_hr()


def create_collections():
    collections = db.list_collection_names()
    if "symbols" not in collections:
        col = db.symbols
        col.create_index([("symbol", 1)])
        col.create_index([("update_date", -1)])

    if "prices" not in collections:
        col = db.prices
        col.create_index([("symbol_id", 1), ("d", -1)])


def full_update_hr():
    symbols = list(db.symbols.find().sort("symbol", 1))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(0, len(symbols), api_limit):
            t1 = time.perf_counter()
            results = executor.map(worker, symbols[i : i + api_limit])
            for ob in results:
                print(ob)
            t2 = time.perf_counter()
            time.sleep(60 - int(t2 - t1))


def worker(meta):
    dc = DataClient(db, td)
    return dc.update_hr(meta)


def get_tech_indicator(self, type):
    res = db.indicator.find({"type": type})
    for ob in res:
        print(ob["full_name"])


def search_symbol(symbol):
    meta = db.symbols.find_one({"symbol": symbol})
    if meta:
        return meta
    else:
        print(f"no symbol : {symbol} in database.")
        return None


def add_symbol(symbol):
    dc = DataClient(db, td)
    dc.add_symbol(symbol)
    meta = db.symbols.find_one({"symbol": symbol})
    dc.update_daily(meta)
    dc.update_hr(meta)


def update_natr(date):
    df = h_volatiliy(n=14)
    records = df.to_dict("records")
    data = {"d": date, "r": records}
    if db.natr.count_documents({"d": date}) > 0:
        db.natr.insert_one(data)


def h_volatiliy(symbols=None, n=14, date=datetime.today()):
    symbols = symbols or list(db.symbols.find())

    natr_coll = []
    vi = VolatilityIndicator()
    for meta in symbols:
        data = list(
            db.prices.find({"symbol_id": meta["_id"], "d": {"$lte": date}}, {"_id": 0, "symbol_id": 0, "p": 0}).limit(
                n * 2
            )
        )[::-1]
        if len(data) < n * 2:
            continue
        df = pd.DataFrame(data)
        df["gain"] = df["c"] - df["c"].shift(1)
        natr_perc_mean = vi.natr(df, n).mean()
        natr_coll.append((meta["symbol"], meta["name"], df["gain"].head(n).sum().round(2), natr_perc_mean.round(2)))
    natr_coll.sort(key=lambda tup: tup[-1], reverse=True)
    return pd.DataFrame(natr_coll, columns=["Ticker", "Name", "Gain", "Atr"])