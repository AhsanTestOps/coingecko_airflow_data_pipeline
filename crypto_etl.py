import requests                 # To call CoinGecko API
import pandas as pd             # To create table and CSV
from datetime import datetime, timezone   # To add fetch timestamp


def get_top_coins_to_csv():
    """
    Fetch top 100 coins from CoinGecko and save selected fields to CSV.
    """

    print("🚀 Fetching top 100 coins from CoinGecko...")

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,                 # Top 100 coins
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("❌ API request failed with status:", response.status_code)
        return

    data = response.json()

    refined_list = []

    for rank, coin in enumerate(data, start=1):
        refined_coin = {
            "rank": rank,
            "symbol": coin.get("symbol", "").upper(),
            "name": coin.get("name", ""),
            "price_usd": coin.get("current_price", 0),
            "change_1h_percent": coin.get("price_change_percentage_1h_in_currency"),
            "change_24h_percent": coin.get("price_change_percentage_24h_in_currency"),
            "change_7d_percent": coin.get("price_change_percentage_7d_in_currency"),
            "volume_24h": coin.get("total_volume", 0),
            "market_cap": coin.get("market_cap", 0),
            "last_updated": coin.get("last_updated", ""),
            "fetched_at_utc": datetime.now(timezone.utc)
        }

        refined_list.append(refined_coin)

    # Convert to DataFrame
    df = pd.DataFrame(refined_list)

    # Save to CSV
    csv_file = "coingecko_top100.csv"
    df.to_csv(csv_file, index=False)

    print(f"✅ CSV file saved successfully: {csv_file}")
    print("📊 Sample rows:")
    print(df.head(5))


# Run the ETL
if __name__ == "__main__":
    get_top_coins_to_csv()