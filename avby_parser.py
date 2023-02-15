import sys
import requests
from bs4 import BeautifulSoup
from data import Car
import re
import db_client


PARSER_NAME = 'avby'


def get_cars(min_price, max_price, count_cars):
    cars_arr = []
    resp = requests.get(f'https://cars.av.by/filter')
    html = BeautifulSoup(resp.content, 'html.parser')
    counter = 0
    for a in html.find_all('div', class_='listing-item'):
        if counter == count_cars: break;
        title = a.find('span', class_='link-text').text.strip()
        link = a.find('a', class_='listing-item__link').text.strip()
        offer_date = a.find('div', class_='listing-item__date').text.strip()
        city = a.find('div', class_='listing-item__location').text.strip()
        price = int(re.sub('[^0-9]', '', a.find('div', class_='listing-item__price').text.strip()))
        if price > min_price and price < max_price:
            cars_arr.append(Car(
                link=link,
                reference=PARSER_NAME,
                price=price,
                title=title,
                offer_date=offer_date,
                city=city
                ))
            counter +=1
            print(f'Спаршено {counter} из {count_cars}')
            ready_cars = list(cars_arr)
    if len(cars_arr) == 0:
        print("По заданной цене ничего не найдено")
        sys.exit()
    if len(cars_arr) < count_cars:
        print(f"По заданной цене найдено только {len(cars_arr)} предложений")
    return ready_cars


def save_cars(cars):
    db_client.create_cars_table()
    counter = 1;
    for car in cars:
        print(f'Загружено в базу {counter} из {len(cars)}')
        db_client.insert_car(car)
        counter+=1


def get_last_cars():
    min_price = int(input("Введите минимальную цену\n"))
    max_price = int(input("Введите максимальную цену\n"))
    count_cars = int(input("Введите желаемое число предложений\n"))
    cars = get_cars(min_price, max_price, count_cars)
    save_cars(cars)


get_last_cars()

