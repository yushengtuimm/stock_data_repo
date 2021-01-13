from .mixin import Mixin

__all__ = (
    "CryptoListEndpoint",
    "CryptoExchangeListEndpoint",
    "CurrencyConversionEndpoint",
    "EarliestTimestampEndpoint",
    "EarningsCalendarEndpoint",
    "EarningsEndpoint",
    "ETFListEndpoint",
    "ExchangeListEndpoint",
    "ExchangeRateEndpoint",
    "ForexPairListEndpoint",
    "IndexListEndpoint",
    "QuoteEndpoint",
    "RealTimePriceEndpoint",
    "StockListEndpoint",
    "SymbolSearchEndpoint",
    "TechnicalIndicatorListEndpoint",
    "TimeSeriesEndpoint",
    "UsageEndpoint",
)


class CryptoListEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, exchange=None, currency_base=None, currency_quote=None):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.currency_base = currency_base
        self.currency_quote = currency_quote

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.currency_base is not None:
            params["currency_base"] = self.currency_base
        if self.currency_quote is not None:
            params["currency_quote"] = self.currency_quote

        params["format"] = format
        return self.ctx.http_client.get("/cryptocurrencies", params=params)


class CryptoExchangeListEndpoint(Mixin):
    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):
        params = {}
        params["format"] = format
        return self.ctx.http_client.get("/cryptocurrency_exchanges", params=params)


class CurrencyConversionEndpoint(Mixin):
    def __init__(self, ctx, symbol, amount):
        self.ctx = ctx
        self.symbol = symbol
        self.amount = amount

    def execute(self, format="JSON"):
        params = {}
        params["symbol"] = self.symbol
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/currency_conversion", params=params)


class EarliestTimestampEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, interval=None, exchange=None):
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/earliest_timestamp", params=params)


class EarningsCalendarEndpoint(Mixin):
    def __init__(
        self,
        ctx,
        symbol=None,
        exchange=None,
        country=None,
        type=None,
        period=None,
        start_date=None,
        end_date=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.method = "earnings_calendar"

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.period is not None:
            params["period"] = self.period
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/earnings_calendar", params=params)


class EarningsEndpoint(Mixin):
    def __init__(
        self,
        ctx,
        symbol=None,
        exchange=None,
        country=None,
        type=None,
        period=None,
        outputsize=None,
        start_date=None,
        end_date=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type
        self.period = period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.method = "earnings"

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/earnings", params=params)


class ETFListEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, exchange=None):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        return self.ctx.http_client.get("/etf", params=params)


class ExchangeListEndpoint(Mixin):
    def __init__(self, ctx, type=None, name=None, code=None, country=None):
        self.ctx = ctx
        self.type = type
        self.name = name
        self.code = code
        self.country = country

    def execute(self, format="JSON"):
        params = {}
        if self.type is not None:
            params["type"] = self.type
        if self.name is not None:
            params["name"] = self.name
        if self.code is not None:
            params["code"] = self.code
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        return self.ctx.http_client.get("/exchanges", params=params)


class ExchangeRateEndpoint(Mixin):
    def __init__(self, ctx, symbol):
        self.ctx = ctx
        self.symbol = symbol

    def execute(self, format="JSON"):
        params = {}
        params["symbol"] = self.symbol
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/exchange_rate", params=params)


class ForexPairListEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, currency_base=None, currency_quote=None):
        self.ctx = ctx
        self.symbol = symbol
        self.currency_base = currency_base
        self.currency_quote = currency_quote

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.currency_base is not None:
            params["currency_base"] = self.currency_base
        if self.currency_quote is not None:
            params["currency_quote"] = self.currency_quote

        params["format"] = format
        return self.ctx.http_client.get("/forex_pairs", params=params)


class IndexListEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, exchange=None):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        return self.ctx.http_client.get("/indices", params=params)


class QuoteEndpoint(Mixin):
    def __init__(
        self,
        ctx,
        symbol,
        interval=None,
        exchange=None,
        country=None,
        volume_time_period=None,
        type=None,
        dp=5,
        timezone="Exchange",
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.volume_time_period = volume_time_period
        self.type = type
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.volume_time_period is not None:
            params["volume_time_period"] = self.volume_time_period
        if self.type is not None:
            params["type"] = self.type
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/quote", params=params)


class RealTimePriceEndpoint(Mixin):
    def __init__(self, ctx, symbol, exchange=None, country=None, type=None, dp=5):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type
        self.dp = dp

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/price", params=params)


class StockListEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, exchange=None, country=None, type=None):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type

        params["format"] = format
        return self.ctx.http_client.get("/stocks", params=params)


class SymbolSearchEndpoint(Mixin):
    def __init__(self, ctx, symbol=None, outputsize=None):
        self.ctx = ctx
        self.symbol = symbol
        self.outputsize = outputsize

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        return self.ctx.http_client.get("/symbol_search", params=params)


class UsageEndpoint(Mixin):
    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):
        params = {}
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/api_usage", params=params)


class TechnicalIndicatorListEndpoint(Mixin):
    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):
        return self.ctx.http_client.get("/technical_indicators")


class TimeSeriesEndpoint(Mixin):
    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=None,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order

    def execute(self, format="JSON"):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/time_series", params=params)
