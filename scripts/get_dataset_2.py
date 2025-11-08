"""
Análise de mercado de veículos Honda Civic no estado da California
Parte 1.1: Coleta de dados complementar
"""

import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
API_KEY = os.getenv("MARKETCHECK_API_KEY")

all_listings = []

rows_per_request = 50
start = 0

city_input = input("Digite as cidades separadas por vírgula (ex: Los Angeles, Sacramento): ")
cities = [c.strip() for c in city_input.split(",") if c.strip()]

while True:
    url = "https://mc-api.marketcheck.com/v2/search/car/active"
    params = {
        "make": "Honda",
        "model": "Civic",
        "state": "CA",
        "city": cities,
        "car_type": "used",
        "year": "2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023",
        "rows": rows_per_request,
        "start": start,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 422:
        break

    elif response.status_code != 200:
        print(f"Erro {response.status_code}, start={start}")
        break

    data = response.json()
    listings = data.get("listings", [])
    num_found = data.get("num_found", 0)

    if not listings or start >= num_found:
        break

    all_listings.extend(listings)
    start += len(listings)
    time.sleep(0.2)

filename = "marketcheck.csv"

if os.path.exists(filename):
    df_existing = pd.read_csv(filename)
else:
    df_existing = pd.DataFrame()

df_new = pd.json_normalize(all_listings)

if not df_existing.empty:
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["vin"])
else:
    df_combined = df_new.drop_duplicates(subset=["vin"])

df_combined.to_csv(filename, index=False)
print(f"Total de registros no CSV: {len(df_combined)}")
