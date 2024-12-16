import requests
from bs4 import BeautifulSoup
import time
from cars import CARS
import pickle
import pandas as pd
import csv
from sklearn.preprocessing import LabelEncoder


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


def parse_car(url):
    date = time.strftime("%Y-%m-%d-%H-%M")
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    try:
        page = requests.get(url, headers=headers, timeout=5.0)
    except:
        print(f"!failed  {url}")
        return {}
    soup = BeautifulSoup(page.content, "html.parser")
    
    data = soup.find("div", {"class": "ticket-status-0"})
    location = data.find("section", {"id": "userInfoBlock"})
    location = location.find_all("li", {"class": "item"})
    location = location[1].text.strip()
    title = data.find("h1", {"class": "head"}).text
    try:
        subtitle = data.find("h3", {"class": "under-head"}).text
    except BaseException as e:
        subtitle = ""
    price = data.find("div", {"class": "price_value"}).find("strong").text
    tech = data.find("div", {"class": "technical-info", "id": "details"})
    dds = tech.find_all("dd")
    texts = []
    range = -1
    kp = -1
    dtp = 0
    hp = -1
    desc = ""
    fuel = -1
    for dd in dds:
        texts.append(dd.text)
    for text in texts:
        splited = text.split()
        if splited[0] == "Пробіг":
            range = int(splited[1])
        if splited[0] == "Коробка":
            kp = splited[2]
            if "Автомат" in kp:
                kp = 1
            else:
                kp = 0
        if "Опис" in splited[0]:
            desc = text.replace("Опис", "")
        if splited[0] == "Участь":
            if splited[3] == "Був":
                dtp = 1
        if splited[0] == "Двигун":
            for i, elem in enumerate(splited):
                if "Газ" in elem:
                    fuel = 2
                elif "Бензин" in elem:
                    fuel = 1
                elif "Дизель" in elem:  
                    fuel = 0
    year = int(title.split()[-1])
    price = price.split()
    price = price[:-1]
    price = "".join(price)
    price = int(price)
    if subtitle:
        spl = subtitle.split()
        for i, elem in enumerate(spl):
            if "к.с." in elem:
                hp = int(spl[i-1][1:])
        subtitle = subtitle.lower().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    features = subtitle.split("•")
    f1 = ""
    f2 = ""
    f3 = ""
    if len(features) > 0:
        f1 = features[0]
    if len(features) > 1:    
        f2 = features[1]
    if len(features) > 2:
        f3 = features[2]
    title = title.lower().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    desc = desc.lower().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    desc = desc.replace(" читати ще сховати", "")
    tmp = [url, date, price, title, subtitle, f1, f2, f3, year, hp, range, kp, dtp, fuel, location, desc]
    return tmp


def get_new():
    all_cars = []
    for brand, models in CARS.items():
        for model, url in models.items():
            url = url + "0"
            links = parse_list(url)
            data = []
            for link in links:
                try:
                    info = [brand, model]
                    tmp = parse_car(link)
                    info.extend(tmp)
                except BaseException as e:
                    print(e)
                    info = ["","","","","","","","","","","","","","","","","",""]
                data.append(info)
            all_cars.extend(data)
    new_cars = []
    
    with open("tmp.csv", 'r') as file:
        reader = csv.reader(file)
        ids = []
        next(reader)
        for row in reader:
            ids.append(row[2])
        for car in all_cars:
            if car[2] not in ids:
                new_cars.append(car)
    print(len(new_cars))
    with open("tmp.csv", 'a') as file:
        writer = csv.writer(file)
        for row in new_cars:
            writer.writerow(row)
    return new_cars
