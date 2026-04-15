import requests
from bs4 import BeautifulSoup
import json

url = "https://www.ratemyagent.com.au/real-estate-agent/courtney-brown-cx744/sales/properties"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

listings = []
for card in soup.select("[class*='PropertyCard'], [class*='property-card'], [class*='listing']"):
    address = card.select_one("[class*='address'], [class*='Address']")
    price = card.select_one("[class*='price'], [class*='Price']")
    link = card.select_one("a")
    listings.append({
        "address": address.get_text(strip=True) if address else "",
        "price": price.get_text(strip=True) if price else "",
        "url": link["href"] if link and link.get("href") else ""
    })

with open("listings.json", "w") as f:
    json.dump(listings, f)

print(f"Saved {len(listings)} listings")
print(res.status_code)
