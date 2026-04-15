import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "beautifulsoup4"], capture_output=True)
subprocess.run(["playwright", "install", "chromium"], capture_output=True)

from playwright.sync_api import sync_playwright
import json

url = "https://www.ratemyagent.com.au/real-estate-agent/courtney-brown-cx744/sales/properties"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        locale="en-AU"
    )
    page = context.new_page()
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(5000)
    
    # Print page content for debugging
    html = page.content()
    print(html[:3000])
    
    browser.close()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

listings = []
for card in soup.select("a[href*='/property/']"):
    address = card.select_one("[class*='address'], [class*='Address'], h2, h3")
    price = card.select_one("[class*='price'], [class*='Price']")
    listings.append({
        "address": address.get_text(strip=True) if address else card.get_text(strip=True)[:80],
        "price": price.get_text(strip=True) if price else "",
        "url": card["href"] if card.get("href") else ""
    })

listings = [l for l in listings if l["address"]]

with open("listings.json", "w") as f:
    json.dump(listings, f)

print(f"Saved {len(listings)} listings")
