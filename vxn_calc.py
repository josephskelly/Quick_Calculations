import requests

def get_vxn():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVXN"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    return price

vxn = get_vxn()
result = (vxn / 100) * 5000

print(f"Current VXN:  {vxn:.2f}")
print(f"Result:       {result:,.2f}  (VXN / 100 × 5,000)")
