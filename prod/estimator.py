import pickle
import pandas as pd
import numpy as np
import parser


def split_location(location):
    if ',' in location:
        location = location.split(',')[0].strip()
    parts = location.split('•')
    return parts[1].strip() if len(parts) > 1 else location.strip()

def format_data(data, encoder):
    data = [elem.strip() if isinstance(elem, str) else elem for elem in data]  
    year = int(data[10])
    hp = int(data[11])
    range = int(data[12])
    kp = int(data[13])
    dtp = int(data[14])
    fuel = int(data[15])
    f1 = data[7]
    f2 = data[8]
    f3 = data[9]
    location = data[16]
    location = split_location(location)
    mlpy = range / (2025 - year)
    location = encoder.transform([location])[0]
    f1 = encoder.transform([f1])[0]
    f2 = encoder.transform([f2])[0]
    f3 = encoder.transform([f3])[0]
    features = [year, range, kp, hp, dtp, fuel, f1, f2, f3, mlpy, location]
    df = pd.DataFrame([features], columns=['year', 'range', 'kp', 'hp', 'dtp', 'fuel', 'f1_encoded', 'f2_encoded', 'f3_encoded', 'mileage_per_year', 'location_encoded'])
    return df

def estimate_car(info):
    brand = info[0]
    model = info[1]
    year = int(info[10])
    if year < 2004:
        return 0
    with open(f"models/{brand}/{model}_model.pkl", 'rb') as file:
        model = pickle.load(file)
    with open(f"models/encoder.pkl", 'rb') as file:
        encoder = pickle.load(file)
    processed = format_data(info, encoder)
    prediction = model.predict(processed)[0]
    return prediction

def wrapper():
    cars = parser.get_new()
    deals = []
    for car in cars:
        try:
            estimate = estimate_car(car)
        except BaseException as e:
            print(e)
            continue
        price = car[4]
        if price < estimate*0.9:
            car.append(estimate)
            deals.append(car)
    return deals