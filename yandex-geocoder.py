import requests
import csv
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://geocode-maps.yandex.ru/1.x/"

def get_coordinates(address):
    """Получает координаты для заданного адреса."""
    params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        try:
            json_data = response.json()
            coords = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lon, lat = map(float, coords.split())  # Разделяем долготу и широту
            return lat, lon
        except (IndexError, KeyError):
            print(f"Координаты для '{address}' не найдены.")
            return None
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

# Читаем адреса из файла address.txt
addresses = []
with open("address.txt", mode="r", encoding="utf-8") as file:
    addresses = [line.strip() for line in file if line.strip()]  # Убираем пустые строки

# Путь к файлу для сохранения
file_path = 'coordinates.csv'

# Открываем CSV файл для записи
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Записываем заголовок
    writer.writerow(["Широта", "Долгота", 
                     "Описание", "Подпись", 
                     "Номер метки"])
    
    # Записываем данные
    for index, address in enumerate(addresses, start=1):
        coords = get_coordinates(address)
        if coords:
            writer.writerow([coords[0], coords[1], address, "", index])

print(f"Данные успешно сохранены в {file_path}")