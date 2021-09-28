import requests
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_URL = os.environ.get("SHEETY_URL")


nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0"
}

user_input = input("Which exercises you did today?: ")

body_nutritionix = {
    "query": user_input,
    "gender": "male",
     "weight_kg": 80.5,
     "height_cm": 185.64,
     "age": 35
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise?"

response = requests.post(url=exercise_endpoint, headers=nutritionix_headers, json=body_nutritionix)
response.raise_for_status()
data = response.json()
print(data)

exercises = [el for el in data["exercises"]]
print(exercises)

today = datetime.now()

list_of_dics = []

for i in range(len(exercises)):
    workout = {
        "date": today.strftime("%Y/%m/%d"),
        "time": today.strftime("%H:%M:%S"),
        "exercise": exercises[i]["name"].title(),
        "duration": exercises[i]["duration_min"],
        "calories": exercises[i]["nf_calories"]
    }
    list_of_dics.append(workout)


body_sheety = {
    "workout": {}
}

sheety_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": os.environ.get("SHEETY_TOKEN"),
}

for i in range(len(list_of_dics)):
    body_sheety["workout"] = list_of_dics[i]
    rows = requests.post(url=SHEETY_URL, headers=sheety_headers, json=body_sheety)