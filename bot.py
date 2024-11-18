import requests
from sklearn.calibration import LabelEncoder
import telebot
import time
import os
import pandas as pd
import pickle
import csv
import threading
import cars
import list_parser
import info_parser
from sklearn.ensemble import RandomForestRegressor




token = '7801015394:AAGXIhp_lOd5LKIvj1nlYIj7Kxl0QXoE6dk'
bot = telebot.TeleBot(token)

script_dir = os.path.dirname(os.path.abspath(__file__))
tg_path = os.path.join(script_dir, 'db', 'tg.csv')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    update_db(message.chat.id)
    bot.send_message(message.chat.id, "Welcome, this bot constantly scans auto.ria and messages you when it finds a good deal.")


@bot.message_handler(commands=['run'])
def run(message):
    id = message.chat.id
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[1] = "admin"
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, "You will now get offers.")


@bot.message_handler(commands=['stop'])
def stop(message):
    id = message.chat.id
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[1] = "user"
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, "You will no longer get offers.")


def update_db(id):
    ids = get_ids()
    if str(id) not in ids:
        with open('db/tg.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([id,"user","all"])


def get_ids():
    ids = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == "admin":
                ids.append(row[0])
    return ids


def get_results():
    results = []
    for model, url in cars.CARS['VW'].items():
        link = url + "0"
        autos = list_parser.parse_list(link)
        new_autos = []
        with open('db/tmp.csv') as file:
            reader = csv.reader(file)
            ids = []
            next(reader)
            for row in reader:
                ids.append(row[0])
            for auto in autos:
                if auto not in ids:
                    new_autos.append(auto)
        new_data = []
        for auto in new_autos:
            try:
                info = info_parser.parse_car(auto)
            except BaseException as e:
                print(e)
                info = ["","","","","","","","",""]
            date = time.strftime("%Y-%m-%d")
            tmp = [auto, date]
            tmp.extend(info)
            new_data.append(tmp)
        with open('db/tmp.csv', 'a') as file:
            writer = csv.writer(file)
            for row in new_data:
                writer.writerow(row)
        for row in new_data:
            if int(row[5]) <2004:
                continue
            df = pd.DataFrame([row], columns=['id', 'date', 'price', 'title', 'subtitle', 'year', 'hp', 'range', 'kp', 'dtp', 'desc'])
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['year'].astype(int)
            df['hp'] = df['hp'].astype(int)
            df['range'] = df['range'].astype(int)
            df['kp'] = df['kp'].astype(int)
            df['dtp'] = df['dtp'].astype(int)
            df['subtitle'] = df['subtitle'].astype(str)
            
            def split_subtitle1(subtitle):
                return subtitle.split('•')[0]
            
            df['new_subtitle1'] = df['subtitle'].apply(split_subtitle1)
            df['new_subtitle1'] = df['new_subtitle1'].str.strip()
            
            label_encoder = LabelEncoder()
            df['new_subtitle1_encoded'] = label_encoder.fit_transform(df['new_subtitle1'])
            
            df['mileage_per_year'] = df['range'] / (2025 - df['year'])
            
            X = df[['year', 'range', 'kp', 'hp', 'dtp', 'new_subtitle1_encoded', 'mileage_per_year']]
            
            model_path = f'./models/vw/{model}_model.pkl'
            mdl = None
            with open(model_path, 'rb') as file:
                mdl = pickle.load(file)
            
            predicted_price = mdl.predict(X)[0]
            predicted_price = int(round(predicted_price))
            print(row[2], predicted_price)
            if row[2] < 0.8*predicted_price and row[2] > 0.5*predicted_price:
                results.append([True, row[2], predicted_price, row[0]])
    return results


def main():
    while True:
        ids = get_ids()
        results = []
        try:
            results = get_results()
        except Exception as e:
            print(e)
        for id in ids:
            for car in results:
                if car[0]:
                    msg = f"Car Found!\n{car[3]}\nPrice: {car[1]}\nPredicted price: {car[2]}"
                    bot.send_message(id, msg)
        time.sleep(60)


if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    bot.infinity_polling()

