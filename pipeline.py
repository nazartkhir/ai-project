import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import pickle
import os

def create_and_pickle_model(filename):
    df = pd.read_csv(filename)
    df = df.dropna(subset=['year', 'range'])
    df_cleaned = df.drop_duplicates()
    
    df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
    df_cleaned['year'] = df_cleaned['year'].astype(int)
    df_cleaned['hp'] = df_cleaned['hp'].astype(int)
    df_cleaned['range'] = df_cleaned['range'].astype(int)
    df_cleaned['kp'] = df_cleaned['kp'].astype(int)
    df_cleaned['dtp'] = df_cleaned['dtp'].astype(int)
    df_cleaned['subtitle'] = df_cleaned['subtitle'].astype(str)
    
    df_cleaned = df_cleaned[df_cleaned['year'] >= 2004]
    df_cleaned.loc[df_cleaned['kp'] == -1, 'kp'] = 0
    df_cleaned.loc[df_cleaned['hp'] == -1, 'hp'] = df_cleaned['hp'].mean()
    
    def split_subtitle1(subtitle):
        return subtitle.split('•')[0]
    
    df_cleaned['new_subtitle1'] = df_cleaned['subtitle'].apply(split_subtitle1)
    df_cleaned['new_subtitle1'] = df_cleaned['new_subtitle1'].str.strip()
    
    df_cleaned = df_cleaned[df_cleaned['new_subtitle1'].map(df_cleaned['new_subtitle1'].value_counts()) >= 3]
    
    label_encoder = LabelEncoder()
    df_cleaned['new_subtitle1_encoded'] = label_encoder.fit_transform(df_cleaned['new_subtitle1'])
    
    
    df_cleaned['mileage_per_year'] = df_cleaned['range'] / (2025 - df_cleaned['year'])
    
    X = df_cleaned[['year', 'range', 'kp', 'hp', 'dtp', 'new_subtitle1_encoded', 'mileage_per_year']]
    y = df_cleaned['price']
    
    model = RandomForestRegressor(n_estimators=500)
    model.fit(X, y)
    
    return model

def main():
    db_dir = './db/vw'
    models_dir = './models/vw'
    for filename in os.listdir(db_dir):
        if filename.endswith('.csv'):
            model_filename = os.path.splitext(filename)[0] + '_model.pkl'
            model_filepath = os.path.join(models_dir, model_filename)
            model = create_and_pickle_model(os.path.join(db_dir, filename))
            with open(model_filepath, 'wb') as file:
                pickle.dump(model, file)

if __name__ == '__main__':
    main()

