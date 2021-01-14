import time
import itertools
from datetime import datetime, date, timedelta


class DataClient:
    def __init__(self, database, twelvedata):
        self.db = database
        self.td = twelvedata

    def update_ark_symbols(self):
        tickers = self.db.ark.trades.find({}, {"ticker": 1}).distinct("ticker")
        [self.add_symbol(ob) for ob in tickers]

    def update_index_comps_symbols(self):
        query = [
            {"$unwind": {"path": "$components"}},
            {"$group": {"_id": "$components", "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "component": "$_id"}},
        ]
        indice = self.db.index.components.aggregate(query)
        [self.add_symbol(ob["component"]) for ob in indice]

        self.add_symbol("EXC", exchange="NASDAQ")
        self.add_symbol("INFO", exchange="NYSE")
        self.add_symbol("LUMN", name="Lumen Technologies, Inc.")

    def check_symbol_exist(self, symbol):
        return True if self.db.symbols.count_documents({"symbol": symbol}) > 0 else False

    def search_symbol(self, symbol, name=None, exchange=None, country=None, type=None):
        exclude_exchanges = ["OTC", "IEX"]
        symbols = self.td.symbol_search(symbol=symbol, outputsize=5).as_json()
        matches = [
            ob
            for ob in symbols
            if (
                ob["symbol"] == symbol
                and (ob["country"] == (country or "United States"))
                and ob["exchange"] not in exclude_exchanges
                and (exchange is None or exchange == ob["exchange"])
                and (name is None or name == ob["instrument_name"])
                and (type is None or type == ob["instrument_type"])
            )
        ]

        if len(matches) == 2 and matches[0] == matches[1]:
            return matches[0]
        elif len(matches) > 1:
            print(f"multiple match for {symbol}")
            [print(f"\t\t{ob}") for ob in matches]
            return None
        elif len(matches) == 0:
            print(f"no match for {symbol}")
            return None
        else:
            return matches[0]

    def add_symbol(self, symbol, name=None, exchange=None, country=None, type=None):
        if self.check_symbol_exist(symbol):
            print(f"{symbol} already exist in collection.")
            return

        symbol_meta = self.search_symbol(symbol, name, exchange, country, type)
        if symbol_meta is None:
            return

        res = self.db.symbols.insert_one(self.to_symbol(symbol_meta))
        if res is not None:
            print(f'{symbol} : {symbol_meta["instrument_name"]} added to symbol collection.')

    @staticmethod
    def to_symbol(meta):
        return {
            "symbol": meta["symbol"],
            "name": meta["instrument_name"],
            "exchange": meta["exchange"],
            "timezone": meta["exchange_timezone"],
            "country": meta["country"],
            "type": meta["instrument_type"],
            "update_date": None,
        }

    def check_usage(self):
        resp = self.td.get_usage().as_json()
        return resp["current_usage"] < resp["plan_limit"]

    def get_start_date(self, symbol, interval):
        earliest_ts = self.td.get_earliest_timestamp(symbol=symbol, interval=interval).as_json()
        return (
            datetime.strptime(earliest_ts["datetime"], "%Y-%m-%d")
            if interval in ["1day", "1week", "1month"]
            else datetime.strptime(earliest_ts["datetime"], "%Y-%m-%d %H:%M:%S")
        )

    def full_update_daily(self):
        symbols = self.db.symbols.find()
        for meta in symbols:
            while not self.check_usage():
                time.sleep(30)
            self.update_daily(meta)

    def update_daily(self, meta):
        latest_p = self.db.prices.find_one({"symbol_id": meta["_id"]}, sort=[("d", -1)])
        if latest_p is None:
            start_d = self.get_start_date(meta["symbol"], "1day")
        else:
            start_d = latest_p["d"] + timedelta(1)
            if start_d > datetime.today():
                return
        prices = []
        while True:
            try:
                resq = list(
                    self.td.time_series(
                        symbol=meta["symbol"],
                        interval="1day",
                        exchange=meta["exchange"],
                        start_date=start_d.strftime("%Y-%m-%d"),
                        outputsize=5000,
                        order="asc",
                    ).as_json()
                )
            except Exception as e:
                if "No data is available" in str(e):
                    break
                elif "You have reached the API calls limit." in str(e):
                    time.sleep(30)
                    continue

            if 0 < len(resq) or len(resq) == 5000:
                prices.extend(resq)
            else:
                break
            start_d = resq[-1]["d"] + timedelta(1)

        if len(prices) == 0:
            return

        for ob in prices:
            ob["symbol_id"] = meta["_id"]
            ob["p"] = {}

        inserts = self.db.prices.insert_many(prices)
        print(f'{meta["symbol"]} price {len(inserts.inserted_ids)} documents updated.')

    def full_update_hr(self):
        symbols = self.db.symbols.find()
        for meta in symbols:
            while not self.check_usage():
                time.sleep(30)
            self.update_hr(meta)

    def update_hr(self, meta):
        if meta["update_date"] is None:
            start_d = self.get_start_date(meta["symbol"], "1h")
        else:
            start_d = meta["update_date"] + timedelta(minutes=1)
        prices = []
        while True:
            try:
                resq = list(
                    self.td.time_series(
                        symbol=meta["symbol"],
                        interval="1h",
                        exchange=meta["exchange"],
                        start_date=start_d.strftime("%Y-%m-%d %H:%M:%S"),
                        outputsize=5000,
                        order="asc",
                    ).as_json()
                )
            except Exception as e:
                if "No data is available" in str(e):
                    break
                elif "You have reached the API calls limit." in str(e):
                    time.sleep(30)
                    continue

            if 0 < len(resq) or len(resq) == 5000:
                prices.extend(resq)
            else:
                break
            start_d = resq[-1]["d"] + timedelta(1)

        if len(prices) == 0:
            return
        upd_date = prices[-1]["d"]
        func = lambda x: x["d"].toordinal()
        for key, group in itertools.groupby(prices, func):
            tdate = datetime.fromordinal(key)
            record = self.db.prices.find_one({"symbol": meta["_id"], "d": tdate})
            p = {} if record is None else record["p"]
            for ob in group:
                mins = str(int((ob["d"] - tdate).total_seconds() / 60))
                p[mins] = {
                    "o": ob["o"],
                    "h": ob["h"],
                    "l": ob["l"],
                    "c": ob["c"],
                    "v": ob["v"],
                }

            temp = list(p.values())
            new_record = {
                "d": tdate,
                "o": temp[0]["o"],
                "h": max([x["h"] for x in temp]),
                "l": min([x["l"] for x in temp]),
                "c": temp[-1]["o"],
                "v": sum([x["v"] for x in temp]),
                "symbol_id": meta["_id"],
                "p": p,
            }
            if record is None:
                self.db.prices.insert(new_record)
            else:
                self.db.prices.replace_one({"_id": record["_id"]}, {"$set": new_record})
        self.db.symbols.update_one({"_id": meta["_id"]}, {"$set": {"update_date": upd_date}})
        print(f'{meta["symbol"]} prices documents updated.[{upd_date}]')