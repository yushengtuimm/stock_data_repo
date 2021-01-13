from .context import Context
from .http_client import HttpClient
from .time_series import TimeSeries
from .endpoints import (
    CryptoListEndpoint,
    CryptoExchangeListEndpoint,
    CurrencyConversionEndpoint,
    EarliestTimestampEndpoint,
    EarningsCalendarEndpoint,
    EarningsEndpoint,
    ETFListEndpoint,
    ExchangeListEndpoint,
    ExchangeRateEndpoint,
    ForexPairListEndpoint,
    IndexListEndpoint,
    QuoteEndpoint,
    RealTimePriceEndpoint,
    StockListEndpoint,
    SymbolSearchEndpoint,
    TechnicalIndicatorListEndpoint,
    TimeSeriesEndpoint,
    UsageEndpoint,
)


class TDClient:
    def __init__(self, apikey, http_client=None, base_url=None, **params):
        self.ctx = Context()
        self.ctx.apikey = apikey
        self.ctx.base_url = base_url or "https://api.twelvedata.com"
        self.ctx.http_client = http_client or HttpClient(self.ctx.base_url)
        self.ctx.params = params

    def get_stock_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return StockListEndpoint(ctx, **ctx.params)

    def get_forex_pair_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return ForexPairListEndpoint(ctx, **ctx.params)

    def get_crypto_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return CryptoListEndpoint(ctx, **ctx.params)

    def get_etf_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return ETFListEndpoint(ctx, **ctx.params)

    def get_index_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return IndexListEndpoint(ctx, **ctx.params)

    def get_exchange_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return ExchangeListEndpoint(ctx, **ctx.params)

    def get_crypto_exchange_list(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return CryptoExchangeListEndpoint(ctx, **ctx.params)

    def get_technical_indicator_list(self):
        return TechnicalIndicatorListEndpoint(ctx=self.ctx)

    def get_earliest_timestamp(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return EarliestTimestampEndpoint(ctx, **ctx.params)

    def symbol_search(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return SymbolSearchEndpoint(ctx, **ctx.params)

    def time_series(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return TimeSeries(ctx)

    def exchange_rate(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return ExchangeRateEndpoint(ctx, **ctx.params)

    def currency_conversion(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return CurrencyConversionEndpoint(ctx, **ctx.params)

    def quote(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return QuoteEndpoint(ctx, **ctx.params)

    def real_time_price(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return RealTimePriceEndpoint(ctx, **ctx.params)

    def get_earnings(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return EarningsEndpoint(ctx, **ctx.params)

    def get_earnings_calendar(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return EarningsCalendarEndpoint(ctx, **ctx.params)

    def get_usage(self, **params):
        ctx = Context.from_context(self.ctx)
        ctx.params.update(params)
        return UsageEndpoint(ctx, **params)