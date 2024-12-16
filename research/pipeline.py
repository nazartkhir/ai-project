import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import pickle
import os


def fit_encoder(brands, encoder):
    data = []
    for brand in brands:
        db_dir = f'./db/{brand}'
        for filename in os.listdir(db_dir):
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(db_dir, filename))
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                df['location'] = df['location'].astype(str)
                df['location'] = df['location'].apply(split_location)
                df['f1'] = df['f1'].astype(str)
                df['f2'] = df['f2'].astype(str)
                df['f3'] = df['f3'].astype(str)
                locations = df['location'].unique()
                f1_values = df['f1'].unique()
                f2_values = df['f2'].unique()
                f3_values = df['f3'].unique()
                data.append(locations)
                data.append(f1_values)
                data.append(f2_values)
                data.append(f3_values)
    all_values = np.concatenate(data)
    all_values = np.unique(all_values)
    all_values = all_values.astype(str)
    encoder.fit(all_values)


def split_location(location):
    if ',' in location:
        location = location.split(',')[0].strip()
    parts = location.split('•')
    return parts[1].strip() if len(parts) > 1 else location.strip()

def create_and_pickle_model(filename, encoder):
    df = pd.read_csv(filename)
    df = df.dropna(subset=['year', 'range', 'location', 'price'])
    df_cleaned = df.drop_duplicates()
    
    df_cleaned = df_cleaned.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    mean_price = df_cleaned['price'].mean()
    std_price = df_cleaned['price'].std()

    df_cleaned = df_cleaned[(df_cleaned['price'] <= mean_price + 2 * std_price) & (df_cleaned['price'] >= mean_price - 2 * std_price)]

    
    
    f1_unique = df_cleaned['f1'].unique()
    f2_unique = df_cleaned['f2'].unique()
    f3_unique = df_cleaned['f3'].unique()
    
    df_cleaned.loc[df_cleaned['f2'].isin(f3_unique), 'f2'] = np.nan
    df_cleaned.loc[df_cleaned['f1'].isin(f3_unique), 'f1'] = np.nan
    df_cleaned.loc[df_cleaned['f1'].isin(f2_unique), 'f1'] = np.nan
    
    rare_f1 = df_cleaned['f1'].value_counts()[df_cleaned['f1'].value_counts() < 10].index
    df_cleaned.loc[df_cleaned['f1'].isin(rare_f1), 'f1'] = np.nan
    
    rare_f2 = df_cleaned['f2'].value_counts()[df_cleaned['f2'].value_counts() < 10].index
    df_cleaned.loc[df_cleaned['f2'].isin(rare_f2), 'f2'] = np.nan
    
    rare_f3 = df_cleaned['f3'].value_counts()[df_cleaned['f3'].value_counts() < 10].index
    df_cleaned.loc[df_cleaned['f3'].isin(rare_f3), 'f3'] = np.nan
    
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
    df_cleaned['location'] = df_cleaned['location'].apply(split_location)
    df_cleaned['location'] = df_cleaned['location'].astype(str)
    df_cleaned['location_encoded'] = encoder.transform(np.array(df_cleaned['location'], dtype=str))
    df_cleaned['f1_encoded'] = encoder.transform(df_cleaned['f1'].astype(str).values)
    df_cleaned['f2_encoded'] = encoder.transform(df_cleaned['f2'].astype(str).values)
    df_cleaned['f3_encoded'] = encoder.transform(df_cleaned['f3'].astype(str).values)
    
    df_cleaned['mileage_per_year'] = df_cleaned['range'] / (2025 - df_cleaned['year'])
    
    X = df_cleaned[['year', 'range', 'kp', 'hp', 'dtp', 'fuel', 'f1_encoded', 'f2_encoded', 'f3_encoded', 'mileage_per_year', 'location_encoded']]
    y = df_cleaned['price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestRegressor(n_estimators=500, max_depth=5)
    model.fit(X, y)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = model.score(X_test, y_test)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print(filename)
    print(f'Root Mean Squared Error: {rmse}')
    print()
    
    return model

def create_models(brand, encoder):
    db_dir = f'./db/{brand}'
    models_dir = f'./models/{brand}'
    for filename in os.listdir(db_dir):
        if filename.endswith('.csv'):
            model_filename = os.path.splitext(filename)[0] + '_model.pkl'
            model_filepath = os.path.join(models_dir, model_filename)
            model = create_and_pickle_model(os.path.join(db_dir, filename), encoder)
            with open(model_filepath, 'wb') as file:
                pickle.dump(model, file)


def main():
    brands = ['vw', 'bmw']
    encoder = LabelEncoder()
    fit_encoder(brands, encoder)
    for brand in brands:
        create_models(brand, encoder)
    encoder_filepath = './models/encoder.pkl'
    with open(encoder_filepath, 'wb') as file:
        pickle.dump(encoder, file)


if __name__ == '__main__':
    main()

