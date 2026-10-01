from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import subprocess
import time


# INPUT YOUR LOGIN DETAILS
user = ""
passwd = ""


options = webdriver.SafariOptions()
browser = webdriver.Safari(options=options)
browser.get('https://www.theknot.com/login')

wait = WebDriverWait(browser, 15)

user_elem = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
user_elem.send_keys(user)

passwd_elem = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
passwd_elem.send_keys(passwd)
passwd_elem.submit()

wait.until(EC.url_contains("theknot.com"))
time.sleep(3)

browser.get("https://www.theknot.com/our-guest-list/rsvps")

download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="rsvp-download-responses-button"]')))
download_button.click()

#Wait for download to finish before continuing
time.sleep(3)

# 
import glob
import os

download_folder = os.path.expanduser("~/Downloads")

time.sleep(3)

#finds any rsvp files to be replaced, dont want to clog up downloads folder
files = glob.glob(os.path.join(download_folder, "rsvp*.csv"))
latest = max(files, key=os.path.getctime)

os.replace(latest, os.path.join(download_folder, "rsvp.csv"))
print("Saved as rsvp.csv")

rsvp_file = os.path.join(download_folder, "rsvp.csv")
df = pd.read_csv(rsvp_file)

df = df[["First Name", "Last Name", "Wedding Day - RSVP"]]

#save and open separate csv for those attending and those who declined, makes it easy to copy and paste
attending = df[df["Wedding Day - RSVP"] == "Attending"]
attending.to_csv(os.path.join(download_folder, "attending.csv"), index=False)

regret = df[df["Wedding Day - RSVP"] == "Regret"]
regret.to_csv(os.path.join(download_folder, "regret.csv"), index=False)

noresponse = df[df["Wedding Day - RSVP"] == "No Response"]
noresponse.to_csv(os.path.join(download_folder, "noresponse.csv"), index=False)

subprocess.run(["open", "-a", "Microsoft Excel", os.path.join(download_folder, "attending.csv")])
subprocess.run(["open", "-a", "Microsoft Excel", os.path.join(download_folder, "regret.csv")])
subprocess.run(["open", "-a", "Microsoft Excel", os.path.join(download_folder, "noresponse.csv")])

print("RSVP Lists Extracted")

browser.quit()
