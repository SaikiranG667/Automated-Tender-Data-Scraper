Automated Tender Data Scraper – CPWD eTender Portal


📌 Overview

This Python script automates the extraction of tender information from the CPWD eTender portal using Selenium WebDriver.
It navigates through the site, collects tender details such as NIT/RFP number, work title, estimated cost, EMD amount, bid submission date, and bid opening date, and saves them to a CSV file for further analysis.

✨ Features

Automated Navigation: Opens CPWD eTender site and clicks through tender listings.

Data Extraction: Scrapes tender details from multiple pages.

Data Storage: Saves extracted data to a CSV file (cpwd_tenders.csv).

Handles Alerts: Detects and accepts initial pop-up alerts on page load.

Pagination Support: Extracts data from multiple pages (first 20 tenders).

🛠️ Technologies Used

Python 3.x

Selenium – for browser automation

Pandas – for data storage and CSV export

Chrome WebDriver – via webdriver_manager for auto driver setup

Install dependencies

```bash
pip install -r requirements.txt
```


Run the script:

```bash
pip install -r requirements.txt
```
