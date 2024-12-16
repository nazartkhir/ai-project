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
import estimator
from sklearn.ensemble import RandomForestRegressor



token = '7801015394:AAGXIhp_lOd5LKIvj1nlYIj7Kxl0QXoE6dk'
bot = telebot.TeleBot(token)

script_dir = os.path.dirname(os.path.abspath(__file__))
tg_path = os.path.join(script_dir, 'tg.csv')

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


@bot.message_handler(commands=['select_model'])
def select_models(message):
    id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    models = cars.get_models()
    for model in models:
        markup.add(model)
    msg = bot.send_message(id, "Select a model:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_selected_model)
def save_selected_model(message):
    id = message.chat.id
    selected_model = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            if selected_model == "all":
                row[2] = "all"
                break
            prev = row[2]
            prev += f"${selected_model}"
            row[2] = prev
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"You have selected {selected_model}.")


@bot.message_handler(commands=['my_models'])
def get_models(message):
    id = message.chat.id
    models = get_user_models(id)
    bot.send_message(id, f"Your models: {models}")


@bot.message_handler(commands=['set_min_price'])
def set_min_price(message):
    id = message.chat.id
    msg = bot.send_message(id, "Enter the minimum price:")
    bot.register_next_step_handler(msg, save_min_price)
def save_min_price(message):
    id = message.chat.id
    min_price = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[3] = min_price
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"Minimum price set to {min_price}.")


@bot.message_handler(commands=['set_max_price'])
def set_max_price(message):
    id = message.chat.id
    msg = bot.send_message(id, "Enter the maximum price:")
    bot.register_next_step_handler(msg, save_max_price)
def save_max_price(message):
    id = message.chat.id
    max_price = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[4] = max_price
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"Maximum price set to {max_price}.")


@bot.message_handler(commands=['set_min_year'])
def set_min_year(message):
    id = message.chat.id
    msg = bot.send_message(id, "Enter the minimum year:")
    bot.register_next_step_handler(msg, save_min_year)
def save_min_year(message):
    id = message.chat.id
    min_year = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[5] = min_year
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"Minimum year set to {min_year}.")


@bot.message_handler(commands=['set_max_year'])
def set_max_year(message):
    id = message.chat.id
    msg = bot.send_message(id, "Enter the maximum year:")
    bot.register_next_step_handler(msg, save_max_year)
def save_max_year(message):
    id = message.chat.id
    max_year = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[6] = max_year
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"Maximum year set to {max_year}.")


@bot.message_handler(commands=['set_min_range'])
def set_min_range(message):
    id = message.chat.id
    msg = bot.send_message(id, "Enter the minimum range:")
    bot.register_next_step_handler(msg, save_min_range)
def save_min_range(message):
    id = message.chat.id
    min_range = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[7] = min_range
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"Minimum range set to {min_range}.")


@bot.message_handler(commands=['set_max_range'])
def set_max_range(message):
    id = message.chat.id
    msg = bot.send_message(id, "Enter the maximum range:")
    bot.register_next_step_handler(msg, save_max_range)
def save_max_range(message):
    id = message.chat.id
    max_range = message.text
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            row[8] = max_range
    with open(tg_path, 'w') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    bot.send_message(id, f"Maximum range set to {max_range}.")


def get_user_filters(id):
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            return row[3:9]


@bot.message_handler(commands=['my_filters'])
def my_filters(message):
    id = message.chat.id
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            filters = row[3:9]
            bot.send_message(id, f"Your filters:\nMin price: {filters[0]}\nMax price: {filters[1]}\nMin year: {filters[2]}\nMax year: {filters[3]}\nMin range: {filters[4]}\nMax range: {filters[5]}")

def get_user_models(id):
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    for row in rows:
        if str(id) == row[0]:
            models = row[2].split('$')
            if len(models) > 1:
                return models[1:]
            else:   
                return ["all"]


def update_db(id):
    ids = get_ids()
    if str(id) not in ids:
        with open(tg_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([id,"user","all","0","100000","0","100000","0","100000"])


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
    return estimator.wrapper()


def filter_cars(cars, id):
    rows = []
    with open(tg_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    filtered_cars = []
    for row in rows:
        if str(id) == row[0]:
            models = get_user_models(id)
            for car in cars:
                if models[0] != "all":
                    if car[1] in models:
                        filtered_cars.append(car)
    filtered_cars2 = [] 
    for car in filtered_cars:
        filters = get_user_filters(id)
        if int(filters[0]) <= car[4] <= int(filters[1]) and int(filters[2]) <= car[10] <= int(filters[3]) and int(filters[4]) <= car[12] <= int(filters[5]):
            filtered_cars2.append(car)
    return filtered_cars2


def main():
    while True:
        ids = get_ids()
        results = []
        try:
            results = get_results()
        except Exception as e:
            print(e)
        for id in ids:
            filtered = filter_cars(results, id)
            for car in filtered:
                msg = f"Car Found!\n{car[2]}\nPrice: {car[4]}\nPredicted price: {round(car[-1])}"
                bot.send_message(id, msg)
        time.sleep(60)


if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    bot.infinity_polling()
