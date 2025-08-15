from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Column name mapping
csv_cols = {
    "NIT/RFP NO": "ref_no",
    "Name of Work / Subwork / Packages": "title",
    "Estimated Cost": "tender_value",
    "Bid Submission Closing Date & Time": "bid_submission_end_date",
    "EMD Amount": "emd",
    "Bid Opening Date & Time": "bid_open_date"
}

# Setup ChromeDriver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# Step 1: Open the CPWD eTender site
driver.get("https://etender.cpwd.gov.in/")
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print(alert.text)
    alert.accept()

except:
    print("alert appeared.")
time.sleep(5)

# Step 2: Click "All" under New Tenders
try:
    all_tab = wait.until(EC.element_to_be_clickable((By.ID, "a_TenderswithinOneday3")))
    driver.execute_script("arguments[0].click();", all_tab)
    time.sleep(5)
except Exception as e:
    print("Could not click 'All':", e)
    driver.quit()
    exit()

# Step 3: Extract tenders from current page
def extract_tenders():
    rows = driver.find_elements(By.CSS_SELECTOR, "#awardedDataTable tbody tr")
    tenders = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 8:
            nit_no = cells[1].text.strip()
            title = cells[2].text.strip()
            est_cost = cells[4].text.replace("₹", "").strip()
            emd_amt = cells[5].text.replace("₹", "").strip()
            bid_sub_date = cells[6].text.strip()
            bid_open_date = cells[7].text.strip()
            tenders.append({
                "ref_no": nit_no,
                "title": title,
                "tender_value": est_cost,
                "bid_submission_end_date": bid_sub_date,
                "emd": emd_amt,
                "bid_open_date": bid_open_date
            })
    return tenders

# Step 4: Scrape first 10 tenders
wait.until(EC.presence_of_element_located((By.ID, "awardedDataTable")))
all_data = extract_tenders()

# Step 5: Go to next page to get next 10
try:
    next_btn = wait.until(EC.element_to_be_clickable((By.ID, "awardedDataTable_next")))
    driver.execute_script("arguments[0].click();", next_btn)
    time.sleep(5)
    all_data += extract_tenders()
except Exception as e:
    print("Could not click next button:", e)

# Step 6: Save to CSV in current folder
df = pd.DataFrame(all_data[:20])
output_file = os.path.join(os.getcwd(), "cpwd_tenders.csv")
df.to_csv(output_file, index=True)
print(f"Saved first 20 tenders to: {output_file}")

driver.quit()
