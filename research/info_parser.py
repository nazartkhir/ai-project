import requests
import csv
import time
from bs4 import BeautifulSoup

DB = "db/bmw/x6.csv"

def main():
    update(DB)
    #parse_car("https://auto.ria.com/uk/auto_ford_fusion_37358678.html")

def update(db):
    data = []
    ctr = 1
    with open(db, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            link = row[0]
            if row[2] == "":
                try:
                    info = parse_car(link)
                    ctr+=1
                except BaseException as e:
                    print(e)
                    info = ["","","","","","","","","","","","","",""]
                date = row[1]
                tmp = [link, date]
                tmp.extend(info)
                data.append(tmp)
                if ctr % 100 == 0:
                    print(f'{ctr/10}%')
            else:
                data.append(row)
    with open(db, "w") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def parse_car(url):
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
    tmp = [price, title, subtitle, f1, f2, f3, year, hp, range, kp, dtp, fuel, location, desc]
    return tmp
    

if __name__ == "__main__":
    main()
