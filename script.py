import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
#options.add_argument("--headless")  
driver = webdriver.Chrome(options=options)

url = "https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=100"
driver.get(url)

time.sleep(5)

results = driver.find_elements(By.CSS_SELECTOR, "li.result-item")[:3]

data = []

for item in results:
    try:
        business_name = item.find_element(By.CSS_SELECTOR, "h2.title a").text.strip()
    except:
        business_name = ""

    try:
        last_update = item.find_element(By.CSS_SELECTOR, ".updated-date").text.replace("Updated ", "").strip()
    except:
        last_update = ""

    try:
        address1 = item.find_element(By.CSS_SELECTOR, ".contact .address1").text.strip()
        address3 = item.find_element(By.CSS_SELECTOR, ".contact .address3").text.strip()
        full_address = f"{address1}, {address3}"
    except:
        full_address = ""

    try:
        materials_elements = item.find_elements(By.CSS_SELECTOR, ".result-materials .material")
        materials = ", ".join([m.text.strip() for m in materials_elements])
    except:
        materials = ""

    data.append({
        "business_name": business_name,
        "last_update_date": last_update,
        "street_address": full_address,
        "materials_accepted": materials
    })

driver.quit()

csv_file = "earth911_recycling_centers.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["business_name", "last_update_date", "street_address", "materials_accepted"])
    writer.writeheader()
    writer.writerows(data)

print(f"Data for {len(data)} facilities saved to {csv_file}")
