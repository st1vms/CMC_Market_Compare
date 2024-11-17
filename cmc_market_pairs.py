import requests
import json

BASE_URL = "https://api.coinmarketcap.com/data-api/v3/"

MARKET_PAIRS_ENDPOINT = BASE_URL + "cryptocurrency/market-pairs/latest"

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "platform": "web",
    "cache-control": "no-cache",
    "Sec-GPC": "1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0",
}

BASE_PARAMS = {
    "slug": "",
    "start": "1",
    "limit": "100",
    "category": "spot",
    "centerType": "all",
    "sort": "cmc_rank_advanced",
    "direction": "desc",
    "spotUntracked": "true",
}


def _query_market_pair(params: dict) -> dict | None:
    res = requests.get(
        MARKET_PAIRS_ENDPOINT, headers=BASE_HEADERS, params=params, timeout=10
    )
    if res.status_code != 200:
        print(res.text)
        return None
    
    return res.json()["data"]


def download_market_pairs_json(
    slug: str, output_file: str, category: str = "spot", center_type: str = "all"
) -> None:

    market_pairs = []

    params = BASE_PARAMS
    params["slug"] = slug
    params["start"] = 1
    params["category"] = category
    params["center_type"] = center_type

    res = _query_market_pair(params)
    if "numMarketPairs" not in res:
        return
    if "marketPairs" in res:
        market_pairs.extend(res["marketPairs"])
    else:
        return

    total_pairs = res["numMarketPairs"]
    print(f"\nScraped results 100/{total_pairs}")

    for start in range(101, total_pairs + 1, 100):
        params["start"] = start
        res = _query_market_pair(params)
        if res and "marketPairs" in res:
            market_pairs.extend(res["marketPairs"])
            print(f"Scraped results {start-1+len(res['marketPairs'])}/{total_pairs}", end="\r")
        else:
            break
    print(f"\nSaving file into {output_file}")
    with open(output_file, "w", encoding="utf-8", errors="ignore") as f:
        json.dump(market_pairs, f, indent=4)


if __name__ == "__main__":
    slug = input("\nInsert crypto name\n>>").strip()
    slug = slug.lower().replace(" ", "-")

    download_market_pairs_json(slug, f"{slug}.json")
