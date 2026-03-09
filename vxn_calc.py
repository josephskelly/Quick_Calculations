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

parser = argparse.ArgumentParser()
parser.add_argument("--nlv", type=float, default=5000)
parser.add_argument("--position", type=float, default=0)
args = parser.parse_args()

nlv = args.nlv
position = args.position
vxn = get_vxn()
result = (vxn / 100) * nlv

print(f"Current VXN:  {vxn:.2f}")
print(f"NLV:          {nlv:,}")
print(f"Position:     {position:,}")
print(f"Result:       {result:,.2f}")
