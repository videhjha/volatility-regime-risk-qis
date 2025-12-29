import pandas as pd

def load_prices(filepath):
    df = pd.read_csv(filepath)

    # Parse dates explicitly (DD-MM-YYYY)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    # Remove commas from price strings and convert to numeric
    df["close"] = (
        df["close"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # Drop rows with invalid prices
    df = df.dropna(subset=["close"])

    # Sort and index
    df = df.sort_values("date")
    df = df.set_index("date")

    return df