import sqlite3
import pickle
import json

with open('task_1_var_48_item.pkl', 'rb') as file:
    data = pickle.load(file)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE "data_table" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" TEXT,
        "author" TEXT,
        "genre" TEXT,
        "pages" INTEGER,
        "published_year" INTEGER,
        "isbn" TEXT,
        "rating" REAL,
        "views" INTEGER
    );
'''
cursor.execute(create_table_query)

for row in data:
    cursor.execute('''
        INSERT INTO data_table ("title", "author", "genre", "pages", "published_year", "isbn", "rating", "views")
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (row['title'], row['author'], row['genre'], row['pages'], row['published_year'], row['isbn'], row['rating'], row['views']))

conn.commit()

# Запрос 1: Вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json
var_value = 48
cursor.execute(f'SELECT * FROM data_table ORDER BY rating LIMIT {var_value + 10}')
result_1 = cursor.fetchall()

result_1_decoded = json.loads(json.dumps(result_1, ensure_ascii=False))

with open('output_1.json', 'w', encoding='utf-8') as output_file:
    json.dump(result_1_decoded, output_file, ensure_ascii=False, indent=2)

# Запрос 2: Вывод (сумму, мин, макс, среднее) по произвольному числовому полю
numeric_field = 'pages'
cursor.execute(f'SELECT SUM({numeric_field}), MIN({numeric_field}), MAX({numeric_field}), AVG({numeric_field}) FROM data_table')
result_2 = cursor.fetchone()
print(f'Sum: {result_2[0]}, Min: {result_2[1]}, Max: {result_2[2]}, Average: {result_2[3]}')

# Запрос 3: Вывод частоты встречаемости для категориального поля
categorical_field = 'genre'
cursor.execute(f'SELECT {categorical_field}, COUNT(*) FROM data_table GROUP BY {categorical_field}')
result_3 = cursor.fetchall()
print(result_3)

# Запрос 4: Вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json
var_predicate = 2015
predicate_field = 'published_year'
cursor.execute(f'SELECT * FROM data_table WHERE {predicate_field} > {var_predicate} ORDER BY rating LIMIT {var_value + 10}')
result_4 = cursor.fetchall()

result_4_decoded = json.loads(json.dumps(result_4, ensure_ascii=False))

with open('output_2.json', 'w', encoding='utf-8') as output_file:
    json.dump(result_4_decoded, output_file, ensure_ascii=False, indent=2)
    
conn.close()
