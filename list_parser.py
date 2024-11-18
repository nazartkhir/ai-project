import requests
import csv
import time
import cars
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


URL = cars.CARS["VW"]["touareg"]
DB = "db/vw/touareg.csv"
DATE = time.strftime("%Y-%m-%d")


def main():
    res = parse_all(URL)
    num = db_update(DB, DATE, res)
    print(f"{num} cars added to {DB}.")


def parse_list(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    try:
        page = requests.get(url, headers=headers, timeout=5.0)
    except:
        print(f"!failed  {url}")
        return []
    soup = BeautifulSoup(page.content, "html.parser")
    data = soup.find("div", {"id":"searchResults"})
    cars = data.find_all("a", {"class":"m-link-ticket"})
    links = []
    for car in cars:
        links.append(car["href"])
    return links


def initial(url):
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    pagination = soup.find("div", {"id":"searchPagination"})
    spans = pagination.find_all("span", {"class":"page-item mhide"})
    last = spans[-1].text
    driver.quit()
    return int(last.strip())

def parse_all(url):
    num = initial(url)
    print(f"Total pages: {num}")
    time.sleep(0.5)
    res = []
    failed = []
    for i in range(num):
        link = url + str(i)
        tmp = parse_list(link)
        if tmp:
            res.extend(tmp)
        else:
            failed.append(link)
        time.sleep(0.5)
    while len(failed) != 0:
        link = failed.pop()
        tmp = parse_list(link)
        if tmp:
            res.extend(tmp)
        else:
            failed.append(link)
        time.sleep(0.5)
    return res

def db_update(db, date, results):
    old = []
    with open(db, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = row[0]
            old.append(id)
    new = []
    for link in results:
        if link not in old:
            new.append(link)
    with open(db, "a") as file:
        writer = csv.writer(file)
        for link in new:
            writer.writerow([link,date,"","","","","","","","",""])
    return len(new)


if __name__ == "__main__":
    main()
