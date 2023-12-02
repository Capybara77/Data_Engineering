# Предметная область - продажа бу авто
# csv.csv - данные по авто (бренд, модель)
# sell_history.json - данные о продажах авто (модель, цена)
# cars_year.json - данные о годах выпуска авто (модель, год)

import sqlite3
import csv
import json

conn = sqlite3.connect('car_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Cars (
                    Brand TEXT,
                    Model TEXT
                )''')

with open('csv.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        cursor.execute('INSERT INTO Cars VALUES (?, ?)', (row[0], row[1]))

cursor.execute('''CREATE TABLE IF NOT EXISTS SellHistory (
                    Model TEXT,
                    Price INTEGER
                )''')

with open('sell_history.json', 'r') as json_file:
    sell_history_data = json.load(json_file)
    for record in sell_history_data:
        cursor.execute('INSERT INTO SellHistory VALUES (?, ?)', (record['Model'], record['Price']))

cursor.execute('''CREATE TABLE IF NOT EXISTS CarYear (
                    Model TEXT,
                    Year INTEGER
                )''')

with open('cars_year.json', 'r') as json_file:
    car_year_data = json.load(json_file)
    for record in car_year_data:
        cursor.execute('INSERT INTO CarYear VALUES (?, ?)', (record['Model'], record['Year']))

conn.commit()

# Запрос 1: Выборка с простым условием + сортировка + ограничение количество
cursor.execute('''SELECT * FROM Cars 
                  WHERE Brand = 'Toyota'
                  ORDER BY Model
                  LIMIT 5''')
result1 = cursor.fetchall()

# Запрос 2: Подсчет объектов по условию
cursor.execute('''SELECT COUNT(*) FROM SellHistory
                  WHERE Price > 10000''')
result2 = cursor.fetchall()

# Запрос 3: Группировка и подсчет средней цены продажи для каждой модели
cursor.execute('''SELECT SellHistory.Model, c.Brand, AVG(Price) AS AvgPrice
                  FROM SellHistory
                  JOIN Cars AS c ON c.Model = SellHistory.Model
                  GROUP BY SellHistory.Model''')
result3 = cursor.fetchall()

# Запрос 4: Обновление данных - увеличение цены продажи на 10% для всех моделей Toyota
cursor.execute('''UPDATE SellHistory
                  SET Price = Price * 1.1
                  WHERE Model IN (SELECT Model FROM Cars WHERE Brand = 'Toyota')''')

# Запрос 5: Выборка данных после обновления
cursor.execute('''SELECT * FROM SellHistory
                  WHERE Model IN (SELECT Model FROM Cars WHERE Brand = 'Toyota')''')
result5 = cursor.fetchall()

# Запрос 6: Подсчет суммарной цены продажи для каждой марки авто
cursor.execute('''SELECT Cars.Brand, SUM(SellHistory.Price) AS TotalPrice
                  FROM Cars
                  JOIN SellHistory ON Cars.Model = SellHistory.Model
                  GROUP BY Cars.Brand''')
result6 = cursor.fetchall()

# Запрос 7: Выборка данных о годе выпуска для моделей с самой высокой ценой продажи
cursor.execute('''SELECT CarYear.Model, CarYear.Year, MAX(SellHistory.Price) AS MaxPrice
                  FROM CarYear
                  JOIN SellHistory ON CarYear.Model = SellHistory.Model
                  GROUP BY CarYear.Model
                  ORDER BY MaxPrice DESC
                  LIMIT 3''')
result7 = cursor.fetchall()

with open('result1.json', 'w') as json_file:
    json.dump(result1, json_file)

with open('result2.json', 'w') as json_file:
    json.dump(result2, json_file)

with open('result3.json', 'w') as json_file:
    json.dump(result3, json_file)

with open('result5.json', 'w') as json_file:
    json.dump(result5, json_file)

with open('result6.json', 'w') as json_file:
    json.dump(result6, json_file)

with open('result7.json', 'w') as json_file:
    json.dump(result7, json_file)

conn.close()
