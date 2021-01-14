import pandas as pd
from pymongo import MongoClient

client = MongoClient()
db = client.capiDB


def get_tech_indicator(type):
    res = db.indicator.find({"type": type})
    for ob in res:
        print(ob["full_name"])


def avg_true_range(meta, interval, time_period):
    if interval == "1day":
        trs = []
        data = list(db.price.find({"symbol_id": meta["_id"]}, {"p": 0}).limit(time_period))
        for x in range(len(data) - 1):
            print(data[x])
            tr = max(
                data[x]["h"] - data[x]["l"], abs(data[x]["h"] - data[x + 1]["c"]), abs(data[x]["l"] - data[x + 1]["c"])
            )
            trs.append(tr)
        # atr = sum(trs) / time_period
        # print(atr)
    pass


if __name__ == "__main__":
    # get_tech_indicator("Volatility Indicators")

    meta = db.symbol.find_one({"symbol": "AAPL"})
    avg_true_range(meta, "1day", 14)
    pass