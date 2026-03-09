import argparse
import requests

def get_vxn():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVXN"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    return price

def yahoo_session():
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    s.get("https://fc.yahoo.com", timeout=10)
    s.get("https://finance.yahoo.com", timeout=10)
    crumb = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10).text
    return s, crumb

def get_stock_iv(ticker):
    s, crumb = yahoo_session()
    r = s.get(f"https://query2.finance.yahoo.com/v7/finance/options/{ticker}?crumb={crumb}", timeout=10)
    r.raise_for_status()
    result = r.json()["optionChain"]["result"][0]
    price = result["quote"]["regularMarketPrice"]
    calls = result["options"][0]["calls"]

    # Find call closest to current price (ATM)
    atm = min(calls, key=lambda c: abs(c["strike"] - price))
    return atm["impliedVolatility"] * 100, price

parser = argparse.ArgumentParser()
parser.add_argument("--nlv", type=float, default=5000)
parser.add_argument("--position", type=float, default=0)
parser.add_argument("--vxn", type=float, default=None)
parser.add_argument("--ticker", type=str, default=None)
args = parser.parse_args()

nlv = args.nlv
position = args.position

if args.ticker:
    iv, stock_price = get_stock_iv(args.ticker.upper())
    vxn = iv
    label = f"{args.ticker.upper()} IV"
    extra = f"Stock Price:  ${stock_price:,.2f}"
elif args.vxn is not None:
    vxn = args.vxn
    label = "VXN"
    extra = None
else:
    vxn = get_vxn()
    label = "VXN"
    extra = None

result = (vxn / 100) * nlv

difference = result - position

print(f"Current {label}:  {vxn:.2f}")
if extra:
    print(extra)
print(f"NLV:          {nlv:,}")
print(f"Position:     {position:,}")
print(f"Result:       {result:,.2f}")
print()
if difference > 0:
    print(f"Buy {difference:,.2f} to reach your target.")
else:
    print(f"No purchase needed. Your position exceeds the target by {abs(difference):,.2f}.")
