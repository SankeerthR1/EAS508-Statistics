import numpy as np
import pandas as pd
import yfinance as yf

TICKERS = {
    "corn": "ZC=F",
    "soybean": "ZS=F",
    "wheat": "ZW=F",
}


def download_futures_monthly(start: str = "2010-01-01", end: str = "2026-01-01") -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    for commodity, ticker in TICKERS.items():
        daily = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=False,
            progress=False,
        )

        if daily.empty:
            print(f"No data returned for {commodity} ({ticker}).")
            continue

        if isinstance(daily.columns, pd.MultiIndex):
            daily.columns = daily.columns.get_level_values(0)

        price_col = "Adj Close" if "Adj Close" in daily.columns else "Close"
        if price_col not in daily.columns:
            print(f"No price column available for {commodity} ({ticker}).")
            continue

        monthly = daily[[price_col]].resample("ME").last().copy()
        monthly["futures_return"] = np.log(monthly[price_col]).diff()
        monthly["commodity"] = commodity
        monthly = monthly.reset_index().rename(columns={"Date": "date", price_col: "futures_price"})
        frames.append(monthly)

    if not frames:
        raise RuntimeError("No commodity data downloaded. Check internet connection/tickers.")

    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    df = download_futures_monthly()
    out = "data/raw/futures_monthly.csv"
    df.to_csv(out, index=False)
    print(f"Saved {out} with {len(df):,} rows.")
