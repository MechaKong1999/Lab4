import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

API_KEY = os.getenv("API_KEY")
ROVER = "curiosity"
API_URL = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/photos"
load_dotenv()

Date = input("Enter the date (YYYY-MM-DD): ")
params = {
    "earth_date": Date
}

def validatedate(Date):
    try:
        datetime.strptime(Date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def findphotos(Date):
    validatedate(Date)
    url=f"{API_URL}?earth_date={Date}&api_key={API_KEY}"
    params = {
        "earth_date": Date, 
        "api_key": API_KEY
    }
    r = requests.get(url, params=params)
    return r.json().get("photos")

def imagedownload(photos):
    for photo in photos:
        img_url = photo.get("img_src")
        img_data = requests.get(img_url).content
        img_name = f"{photo.get('id')}.jpg"
        with open(img_name, 'wb') as handler:
            handler.write(img_data)
        print(f"Downloaded {img_name}")

photos = findphotos(Date)
if photos:
    imagedownload(photos)
else:
    print("No photos found for this date.")


