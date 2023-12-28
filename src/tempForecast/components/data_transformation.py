import sqlite3
import pandas as pd
from tempForecast.components.pipeline_transformation import pipe

# écrire la variable qui représente le dossier où on se trouve pour le mettre dans db_path
class WeatherDatabase:
    def __init__(self, db_path='research/weather_data.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY,
            datetime DATE UNIQUE,
            température REAL,
            vent REAL,
            rafales REAL,
            vent_direction TEXT,
            humidite REAL,
            pt_de_rosee REAL,
            pression REAL,
            bio_meteo TEXT,
            radiation_solaire REAL
        )
        ''')

    def insert_dataframe(self, df):
        cursor = self.conn.cursor()
        for index, row in df.iterrows():
            try:
                cursor.execute('''
                INSERT OR IGNORE INTO weather_data 
                (Datetime, température, vent, rafales, vent_direction, humidite, pt_de_rosee, pression, bio_meteo, radiation_solaire) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (row['Datetime'].strftime('%Y-%m-%d %H:%M:%S'), row['Température'], row['Vent'], row['Rafales'], row['vent_direction'], row['Humidité'], row['Pt de rosée'], row['Pression'], row['Bio-météo'], row['Radiation solaire']))
            except Exception as e:
                print(f"Error inserting into database: {e}")
        self.conn.commit()

    def get_data(self):
        df_from_db = pd.read_sql('SELECT * FROM weather_data', self.conn)
        df_from_db.sort_values(by="datetime", inplace=True, ascending=False)  # Most recent data first
        df_from_db['datetime'] = pd.to_datetime(df_from_db['datetime'])
        return df_from_db

    def close_connection(self):
        self.conn.close()


    def load_data_and_transform(self):
        database  = WeatherDatabase()
        df = database.get_data()
        database.close_connection()
        


        df.index = df['datetime']
        df.sort_index(inplace=True)
        
        df = pd.DataFrame(df)

        return df        
    
    
    def split_train_test(self, df):
        df.index = pd.to_datetime(df.index)
        threshold_time = df.index.max() - pd.Timedelta(hours=48)
        X_train = df[df.index < threshold_time]
        X_test = df[df.index >= threshold_time - pd.offsets.Hour(48)]

        y_train = df[df.index < threshold_time][["température"]]
        y_test = df[df.index >= threshold_time - pd.offsets.Hour(48)][[
            "température"
        ]]
        

        return X_train, X_test, y_train, y_test
    
    def fit_transform_pipe(self, df):
        df.index = pd.to_datetime(df.index)
        X_train_t = pipe.fit_transform(df[['température','vent','rafales']])

        return X_train_t
    
    def transform_pipe(self, df):

        df.index = pd.to_datetime(df.index)

        X_test_t = pipe.fit_transform(df[['température','vent','rafales']])

        return X_test_t