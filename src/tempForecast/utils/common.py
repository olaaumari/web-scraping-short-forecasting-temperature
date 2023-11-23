import calendar
from datetime import datetime
import locale
import random
import os
import numpy as np
import pandas as pd
import json
from tempForecast.constants import *

from box.exceptions import BoxValueError
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
import base64
import yaml

from tempForecast import logger

def get_random_headers():
    return random.choice(HEADERS_LIST)

def format_day(day):
    return "1er" if day == 1 else str(day)


def get_month_name_in_french(month_number):
    # On utilise le module locale pour mettre le mois en français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    if month_number == 8:  # Cas spécifique pour août
        return "aout"
    elif month_number == 12:  # Cas spécifique pour décembre
        return "decembre"
    elif month_number == 2:  # Cas spécifique pour février
        return "fevrier"
    return calendar.month_name[month_number].lower()

def to_float(value):
    try:
        return float(value)
    except ValueError:  # Si la conversion échoue, retournez np.nan
        return np.nan
    

def calculate_days_to_scrap(last_df: pd.DataFrame) -> int:
    today = datetime.now()

    try:
        #df_t.index = pd.to_datetime(df_t.index)
        last_df['Datetime'] = pd.to_datetime(last_df['Datetime'])
        # Filtrez les dates antérieures à une certaine année, disons 2000, pour être sûr d'éliminer les valeurs erronées comme 1970
        filtered_dates = last_df[last_df.Datetime.dt.year > 2022].Datetime

        if not filtered_dates.empty:
            last_date_in_df = filtered_dates[0]
        else:
            last_date_in_df = today
    except:
        # Si df_t n'est pas défini ou n'a pas la colonne 'Datetime', scraper à partir d'aujourd'hui.
        last_date_in_df = today

    days_to_scrape = (today - last_date_in_df).days

    return days_to_scrape


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")