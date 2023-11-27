# сайт https://topdisc.ru/catalog/smartfony/

import os
from bs4 import BeautifulSoup
import json
from statistics import mean, stdev
import re

folder_path = 'pages'

products_data = []

for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        products = soup.select('.item')

        for product in products:
            name = product.select_one('img.thumbnail')['alt'].strip()
            image_src = product.select_one('img.thumbnail')['src']
            price_text = product.select_one('.price').find(string=True, recursive=False).strip()
            price = int(''.join(c for c in price_text if c.isdigit()))
            product_id = product.select_one('.img-wrap img')['id']
            product_link = product.select_one('.name a')['href']

            economy = None
            div_hover = product.select_one('.hover-show')
            if div_hover:
                span_with_number = div_hover.select_one('span')
                economy = re.sub(r'\D', '', span_with_number.text)

            product_data = {
                'name': name,
                'product_link': product_link,
                'product_id': product_id,
                'image_src': image_src,
                'price': price,
                'economy': "0" if economy == '' else economy
            }

            products_data.append(product_data)

result_filepath = 'products_data.json'

with open(result_filepath, 'w', encoding='utf-8') as result_file:
    json.dump(products_data, result_file, ensure_ascii=False, indent=2)

folder_path = 'phones'

phones_data = []

translation_dict = {
    "*Причина уценки": "condition",
    "Бренд": "brand",
    "Диагональ экрана": "screen_size",
    "Разрешение экрана": "screen_resolution",
    "Тип экрана": "screen_type",
    "Смартфон с \"Монобровью\"": "notch",
    "Встроенная память": "internal_storage",
    "Поддержка карт памяти": "memory_card_support",
    "Оперативная память": "ram",
    "Платформа": "platform",
    "Количество ядер": "number_of_cores",
    "Процессор": "processor",
    "Ёмкость аккумулятора": "battery_capacity",
    "Количество SIM-карт": "number_of_sim_cards",
    "Тип SIM-карты": "sim_card_type",
    "Интернет": "internet",
    "Навигация": "navigation",
    "Модуль NFC": "nfc",
    "Двойная камера": "dual_camera",
    "Основная камера": "main_camera",
    "Фронтальная камера": "front_camera",
    "Разблокировка по лицу": "face_unlock",
    "Защита от влаги": "water_resistance",
    "Модель года": "model_year",
    "Материал корпуса": "body_material",
    "Вес, г": "weight",
    "Длина, мм": "length",
    "Ширина, мм": "width",
    "Толщина, мм": "thickness",
    "Цвет": "color"
}

for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        table_rows = soup.select('.product-accordion-tabs-wrap table tbody tr')

        phone_data = {}
        for row in table_rows:
            columns = row.find_all('td')
            if len(columns) == 2:
                key = columns[0].text.strip()
                value = columns[1].text.strip()

                # Используем словарь для соответствия русских и английских названий
                english_key = translation_dict.get(key)
                if english_key:
                    phone_data[english_key] = value

        phones_data.append(phone_data)
        
with open('phones_data.json', 'w', encoding='utf-8') as result_file:
    json.dump(phones_data, result_file, ensure_ascii=False, indent=2)


with open('products_data.json', 'r', encoding='utf-8') as file:
    products_data = json.load(file)

sorted_by_price = sorted(products_data, key=lambda x: x['price'], reverse=True)
sorted_by_price_filepath = 'sorted_products_by_price.json'

with open(sorted_by_price_filepath, 'w', encoding='utf-8') as sorted_file:
    json.dump(sorted_by_price, sorted_file, ensure_ascii=False, indent=2)

filtered_by_price = [product for product in products_data if product['price'] > 50000]
filtered_by_price_filepath = 'filtered_products_by_price.json'

with open(filtered_by_price_filepath, 'w', encoding='utf-8') as filtered_price_file:
    json.dump(filtered_by_price, filtered_price_file, ensure_ascii=False, indent=2)


price_values = [product['price'] for product in products_data]
price_sum = sum(price_values)
price_min = min(price_values)
price_max = max(price_values)
price_avg = mean(price_values)
price_stdev = stdev(price_values)

price_stats = {
    'sum': price_sum,
    'min': price_min,
    'max': price_max,
    'avg': price_avg,
    'stdev': price_stdev
}

price_stats_filepath = 'price_statistics.json'

with open(price_stats_filepath, 'w', encoding='utf-8') as price_stats_file:
    json.dump(price_stats, price_stats_file, ensure_ascii=False, indent=2)

name_frequencies = {}
for product in products_data:
    name = product['name']
    name_frequencies[name] = name_frequencies.get(name, 0) + 1

name_frequencies_filepath = 'name_frequencies.json'

with open(name_frequencies_filepath, 'w', encoding='utf-8') as name_frequencies_file:
    json.dump(name_frequencies, name_frequencies_file, ensure_ascii=False, indent=2)
