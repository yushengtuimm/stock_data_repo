from .endpoints import TimeSeriesEndpoint
from datetime import datetime

__all__ = ("TimeSeries",)


class TimeSeries:
    def __init__(self, ctx, endpoint=None):
        self.ctx = ctx
        self.endpoint = endpoint or TimeSeriesEndpoint(self.ctx, **self.ctx.params)

    def as_json(self):
        time_series_json = self.endpoint.as_json()
        out = []

        for row in time_series_json:
            out.append(self._to_dict(row))
        return out

    def _to_dict(self, value):
        dic = {}
        if self.ctx.params["interval"] in ["1day", "1week", "1month"]:
            dic["d"] = datetime.strptime(value["datetime"], "%Y-%m-%d")
        else:
            dic["d"] = datetime.strptime(value["datetime"], "%Y-%m-%d %H:%M:%S")
        dic["o"] = float(value["open"])
        dic["h"] = float(value["high"])
        dic["l"] = float(value["low"])
        dic["c"] = float(value["close"])
        dic["v"] = float(value["volume"])
        return dic