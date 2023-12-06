# Предметная область - продажа бу авто
# csv.csv - данные по авто (бренд, модель)
# sell_history.json - данные о продажах авто (модель, цена)
# cars_year.json - данные о годах выпуска авто (модель, год)

from pymongo import MongoClient
import csv
import json

client = MongoClient('localhost', 27017)
db = client['car_database']

collection_cars = db['Cars']
with open('csv.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        collection_cars.insert_one({
            'Brand': row[0],
            'Model': row[1]
        })

collection_sell_history = db['SellHistory']
with open('sell_history.json', 'r') as json_file:
    sell_history_data = json.load(json_file)
    for record in sell_history_data:
        collection_sell_history.insert_one({
            'Model': record['Model'],
            'Price': record['Price']
        })

collection_car_year = db['CarYear']
with open('cars_year.json', 'r') as json_file:
    car_year_data = json.load(json_file)
    for record in car_year_data:
        collection_car_year.insert_one({
            'Model': record['Model'],
            'Year': record['Year']
        })

# Задание 1: Выборка
result_select_all_models = list(collection_cars.find({}, {'Model': 1, '_id': 0}))
with open('result_select_all_models.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_select_all_models, json_file, default=str, ensure_ascii=False)

# Задание 2: Выбор с агрегацией
result_avg_price_by_model = list(collection_sell_history.aggregate([
    {"$group": {
        "_id": "$Model",
        "avg_price": {"$avg": "$Price"}
    }}
]))
with open('result_avg_price_by_model.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_avg_price_by_model, json_file, default=str, ensure_ascii=False)

# Задание 3: Обновление года выпуска для определенной модели
model_to_update = "e-tron Sportback"
new_year = 2023
collection_car_year.update_one({'Model': model_to_update}, {"$set": {'Year': new_year}})
print(f"\nДанные для модели {model_to_update} обновлены. Новый год выпуска: {new_year}")

# Удаление данных о продажах для определенной модели
model_to_delete = "Omega"
collection_sell_history.delete_many({'Model': model_to_delete})
print(f"\nДанные о продажах для модели {model_to_delete} удалены.")

client.close()
