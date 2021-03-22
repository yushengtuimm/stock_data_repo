import pandas as pd
import numpy as np


class VolatilityIndicator:
    def __init__(self):
        pass

    def true_range(self, df):
        return pd.DataFrame(
            {
                "hl": df["h"] - df["l"],
                "hc": abs(df["h"] - df["c"].shift(1)),
                "lc": abs(df["l"] - df["c"].shift(1)),
            }
        ).max(axis=1)

    def normalize_tr(self, df):
        return (
            pd.DataFrame(
                {
                    "hl": df["h"] - df["l"],
                    "hc": abs(df["h"] - df["c"].shift(1)),
                    "lc": abs(df["l"] - df["c"].shift(1)),
                }
            )
            .max(axis=1)
            .div(df["c"].shift(1))
            .mul(100)
        )

    def atr(self, df, n=14):
        series = self.true_range(df)
        return self.wwma(series, n)

    def natr(self, df, n=14):
        series = self.normalize_tr(df)
        return self.wwma(series, n)

    def wwma(self, series, n):
        return series.ewm(alpha=1 / n, min_periods=n, adjust=False).mean()
