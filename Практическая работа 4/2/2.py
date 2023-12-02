import sqlite3
import json

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

create_table_query_2 = '''
    CREATE TABLE "data_table_2" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" TEXT,
        "price" INTEGER,
        "place" TEXT,
        "date" TEXT
    );
'''
cursor.execute(create_table_query_2)

with open('task_2_var_48_subitem.json', 'r', encoding='utf-8') as file:
    data_2 = json.load(file)

for row in data_2:
    cursor.execute('''
        INSERT INTO data_table_2 ("title", "price", "place", "date")
        VALUES (?, ?, ?, ?)
    ''', (row['title'], row['price'], row['place'], row['date']))

conn.commit()

# Запрос 1
cursor.execute('''
    SELECT data_table.title, data_table.author, data_table_2.price
    FROM data_table
    JOIN data_table_2 ON data_table.title = data_table_2.title
    WHERE data_table_2.place = 'offline'
    LIMIT 10;
''')
result_1 = cursor.fetchall()

with open('output_1.json', 'w', encoding='utf-8') as output_file:
    json.dump(result_1, output_file, ensure_ascii=False, indent=2)

# Запрос 2
cursor.execute('''
    SELECT data_table.title, data_table.genre, data_table_2.date
    FROM data_table
    JOIN data_table_2 ON data_table.title = data_table_2.title
    WHERE data_table_2.price > 4000
    LIMIT 10;
''')
result_2 = cursor.fetchall()

with open('output_2.json', 'w', encoding='utf-8') as output_file:
    json.dump(result_2, output_file, ensure_ascii=False, indent=2)

# Запрос 3
cursor.execute('''
    SELECT data_table.title, AVG(data_table_2.price)
    FROM data_table
    JOIN data_table_2 ON data_table.title = data_table_2.title
    GROUP BY data_table.title
    LIMIT 10;
''')
result_3 = cursor.fetchall()

with open('output_3.json', 'w', encoding='utf-8') as output_file:
    json.dump(result_3, output_file, ensure_ascii=False, indent=2)

conn.close()
