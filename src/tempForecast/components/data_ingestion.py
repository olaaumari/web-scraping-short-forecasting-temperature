import sys
sys.path.append('C:/Users/Zbook Create G7/Desktop/temperature forecasting/src/tempForecast')
from tempForecast.components.data_transformation import WeatherDatabase

import pandas as pd
from tempForecast.utils.common import *
from constants import *
import requests
import numpy as np
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import time

today = datetime.now()

class weather_scraping:

    def __init__(self, last_df = None):
        self.HEADERS_LIST = HEADERS_LIST
        self.last_df = last_df
        self.days_to_scrape = calculate_days_to_scrap(self.last_df) if self.last_df is not None else 5
        

    def web_scraping(self):
        global today

        liste_de_df = []

        for i in range(self.days_to_scrape + 1):
            # Soustraction des jours
            date_to_scrape = today - timedelta(days=i)
            
            print(date_to_scrape)
            headers = get_random_headers()
            # Mise à jour de l'URL pour utiliser le nom du mois en français
            URL = f"https://www.infoclimat.fr/observations-meteo/archives/{format_day(date_to_scrape.day)}/{get_month_name_in_french(date_to_scrape.month)}/{date_to_scrape.year}/paris-5eme-tour-zamansky-jussieu/000BV.html?dixminutes"
            print(URL)

            response = requests.get(URL, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            # Extraire toutes les lignes de la table en une seule fois
            rows = soup.select("#resptable-releves > tbody:nth-child(2) > tr")

            # Ici, vous pouvez continuer avec le reste du traitement pour chaque jour...

            # Initialiser les listes
            (
                dates,
                hours,
                temperatures,
                vents,
                rafales,
                humidites,
                pts_rosee,
                vent_directions,
                pressions,
                bio_meteo,
                radiations_solaires,
            ) = ([] for _ in range(11))

            # Parcourir chaque ligne et extraire les informations
            for row in rows:
                # Extraction de la date et de l'heure
                date_elements = row.find_all(class_="tipsy-trigger")
                date_text = "Date not found."
                hour_text = np.nan
                for el in date_elements:
                    if "Heure réelle d'émission" in el.attrs.get("title", ""):
                        date_text = BeautifulSoup(
                            el["title"].split("<br />")[1], "html.parser"
                        ).text
                        hour_text = BeautifulSoup(
                            el["title"].split("<br />")[2], "html.parser"
                        ).text
                        break
                dates.append(date_text)
                hours.append(hour_text)

                # Extraction des autres données
                temperatures.append(
                    row.select_one("td:nth-child(2) > span:nth-child(1)").text
                    if row.select_one("td:nth-child(2) > span:nth-child(1)")
                    else np.nan
                )
                vents.append(
                    row.select_one("td:nth-child(3) > span:nth-child(1)").text
                    if row.select_one("td:nth-child(3) > span:nth-child(1)")
                    else np.nan
                )
                rafales.append(
                    row.select_one("td:nth-child(3) > span:nth-child(5)").text
                    if row.select_one("td:nth-child(3) > span:nth-child(5)")
                    else np.nan
                )
                humidites.append(
                    row.select_one("td:nth-child(4) > span:nth-child(1)").text
                    if row.select_one("td:nth-child(4) > span:nth-child(1)")
                    else np.nan
                )
                pts_rosee.append(
                    row.select_one("td:nth-child(6) > span:nth-child(1)").text
                    if row.select_one("td:nth-child(6) > span:nth-child(1)")
                    else np.nan
                )
                vent_directions.append(
                    row.select_one("td:nth-child(3) > div:nth-child(6)")["title"]
                    .split(" ")[-1]
                    .replace("°", "")
                    if row.select_one("td:nth-child(3) > div:nth-child(6)")
                    else np.nan
                )
                pressions.append(
                    row.select_one("td:nth-child(7)")
                    .text.strip()
                    .replace("hPa", "")
                    .replace("=", "")
                    .strip()
                    if row.select_one("td:nth-child(7)")
                    else np.nan
                )
                bio_meteo.append(
                    row.select_one("td:nth-child(5) > span:nth-child(1)").text
                    if row.select_one("td:nth-child(5) > span:nth-child(1)")
                    else np.nan
                )
                radiations_solaires.append(
                    row.select_one(
                        "td:nth-child(5) > a:nth-child(4) > span:nth-child(1)"
                    ).text
                    if row.select_one(
                        "td:nth-child(5) > a:nth-child(4) > span:nth-child(1)"
                    )
                    else np.nan
                )

            df = pd.DataFrame(
                {
                    "Date": dates,
                    "Heure": hours,
                    "Température": temperatures,
                    "Vent": vents,
                    "Rafales": rafales,
                    "vent_direction": vent_directions,
                    "Humidité": humidites,
                    "Pt de rosée": pts_rosee,
                    "Pression": pressions,
                    "Bio-météo": bio_meteo,
                    "Radiation solaire": radiations_solaires,
                }
            )

            # Convert columns to string type
            df["Date"] = df["Date"].astype(str)
            df["Heure"] = df["Heure"].astype(str)
            df["Température"] = df["Température"].astype(str)
            df["Vent"] = df["Vent"].astype(str)
            df["Rafales"] = df["Rafales"].astype(str)
            df["vent_direction"] = df["vent_direction"].astype(str)
            df["Humidité"] = df["Humidité"].astype(str)
            df["Pt de rosée"] = df["Pt de rosée"].astype(str)
            df["Pression"] = df["Pression"].astype(str)
            df["Radiation solaire"] = df["Radiation solaire"].astype(str)
            df["Bio-météo"] = df["Bio-météo"].astype(str)

            df["Température"] = df["Température"].apply(to_float)
            df["Vent"] = df["Vent"].apply(to_float)
            df["Rafales"] = df["Rafales"].apply(to_float)
            df["vent_direction"] = df["vent_direction"].apply(to_float)
            df["Humidité"] = df["Humidité"].apply(to_float)
            df["Pt de rosée"] = df["Pt de rosée"].apply(to_float)
            df["Pression"] = df["Pression"].apply(to_float)
            df["Radiation solaire"] = df["Radiation solaire"].apply(to_float)
            df["Bio-météo"] = df["Bio-météo"].apply(to_float)

            # Replace 'nan' strings back to np.nan
            df["Date"].replace("nan", np.nan, inplace=True)
            df["Heure"].replace("nan", np.nan, inplace=True)

            # Combine the 'Date' and 'Heure' columns and remove ' UTC' from the end of 'Heure'
            df["Datetime"] = df["Date"] + " " + df["Heure"].str.replace(" UTC", "")

            # Convert the combined string into a datetime object
            df["Datetime"] = pd.to_datetime(df["Datetime"], format="%d/%m/%Y %Hh%M")

            # If you want to drop the original 'Date' and 'Heure' columns
            df.drop(["Date", "Heure"], axis=1, inplace=True)

            liste_de_df.append(df)
            # print(df)
            sleep_duration = random.randint(3, 5)  # Attendre entre 2 à 5 secondes
            time.sleep(sleep_duration)

        final_df = pd.concat(liste_de_df, axis=0, ignore_index=False)

        return final_df


    def load_data(self, df=None):

        database = WeatherDatabase()

        if df is not None:
                database.insert_dataframe(df)    

        df = database.get_data()
        database.close_connection()
        
        return df 

           