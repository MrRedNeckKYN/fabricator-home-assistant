#!/usr/bin/env python3
"""Unofficial ARM64 Grass launcher; manual noVNC login only.

Adapted from MRColorR/get-grass's GPL-3.0 grass-node-arm64 recipe.
"""
import logging
import os
import random
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DATA_DIR = "/data/grass"
EXTENSION_ID = os.getenv("EXTENSION_ID", "ilehaonighjijnmpnagapkhpcdbhclfg")


def download_extension():
    path = os.path.join(DATA_DIR, "extensions", EXTENSION_ID, f"{EXTENSION_ID}.crx")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    url = (
        "https://clients2.google.com/service/update2/crx"
        f"?response=redirect&prodversion=131.0.0.0&acceptformat=crx2,crx3"
        f"&x=id%3D{EXTENSION_ID}%26uc"
    )
    logging.info("Downloading Grass extension from Chrome Web Store")
    response = requests.get(url, allow_redirects=True, timeout=60)
    response.raise_for_status()
    with open(path, "wb") as output:
        output.write(response.content)
    return path


def start_browser(extension_path):
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={DATA_DIR}/chromium-profile")
    options.add_experimental_option("prefs", {"extensions.ui.developer_mode": True})
    options.add_extension(extension_path)
    return webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)


def wait_for_login(driver):
    logging.info("Open http://HOME_ASSISTANT_IP:6080 and log in to Grass in the browser window")
    while True:
        try:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(f"chrome-extension://{EXTENSION_ID}/index.html")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Grass is Connected')]"))
            )
            logging.info("Grass extension reports connected")
            return driver.current_window_handle
        except (TimeoutException, NoSuchElementException, WebDriverException):
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            logging.info("Still waiting for manual login")
            time.sleep(30)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    os.makedirs(DATA_DIR, exist_ok=True)
    while True:
        driver = None
        try:
            driver = start_browser(download_extension())
            driver.get("https://app.grass.io/dashboard")
            window = wait_for_login(driver)
            while True:
                time.sleep(random.randint(3600, 14400))
                driver.switch_to.window(window)
                driver.refresh()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Grass is Connected')]"))
                )
        except Exception as exc:
            logging.error("Grass browser session ended: %s", exc)
            time.sleep(random.randint(30, 90))
        finally:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass


if __name__ == "__main__":
    main()
