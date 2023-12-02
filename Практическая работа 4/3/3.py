import sqlite3
import csv
import os
import msgpack
import json

if os.path.exists('data.db'):
    os.remove('data.db')

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE "table1" (
    "Id" INTEGER,
    "artist" TEXT,
    "song" TEXT,
    "duration_ms" INTEGER,
    "year" INTEGER,
    "tempo" REAL,
    "genre" TEXT,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
'''
cursor.execute(create_table_query)
conn.commit()

csv_file_path = 'C:\\Users\\Capybara\\Desktop\\data_engineering\\Data_Engineering\\Практическая работа 4\\3\\task_3_var_48_part_1.csv'

with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=";")

    next(csv_reader)
    next(csv_reader)

    for row in csv_reader:
        if all(value.strip() == '' or value == '0' for value in row):
            continue

        cursor.execute('''
            INSERT INTO table1 (artist, song, duration_ms, year, tempo, genre)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row[0],  # artist
            row[1],  # song
            int(row[2]),  # duration_ms
            int(row[3]),  # year
            float(row[4]),  # tempo
            row[5]  # genre
        ))

msgpack_file_path = 'C:\\Users\\Capybara\\Desktop\\data_engineering\\Data_Engineering\\Практическая работа 4\\3\\task_3_var_48_part_2.msgpack'

with open(msgpack_file_path, 'rb') as msgpack_file:
    msgpack_data = msgpack.unpack(msgpack_file, raw=False)
    
    for row in msgpack_data:
        cursor.execute('''
            INSERT INTO table1 (artist, song, duration_ms, year, tempo, genre)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['artist'],
            row['song'],
            row['duration_ms'],
            row['year'],
            row['tempo'],
            row['genre']
        ))

conn.commit()

select_query = '''
    SELECT * FROM table1
    ORDER BY duration_ms
    LIMIT ?
'''

var = 48
cursor.execute(select_query, (var + 10,))
result_rows = cursor.fetchall()

json_file_path = 'sorted_data.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(result_rows, json_file, ensure_ascii=False, indent=4)

stats_query = '''
    SELECT 
        SUM(duration_ms) as total_duration,
        MIN(duration_ms) as min_duration,
        MAX(duration_ms) as max_duration,
        AVG(duration_ms) as avg_duration
    FROM table1
'''

cursor.execute(stats_query)
stats_result = cursor.fetchone()

print('Статистика по полю duration_ms:')
print(f'Total Duration: {stats_result[0]}')
print(f'Min Duration: {stats_result[1]}')
print(f'Max Duration: {stats_result[2]}')
print(f'Average Duration: {stats_result[3]}')

frequency_query = '''
    SELECT year, COUNT(*) as frequency
    FROM table1
    GROUP BY year
    ORDER BY frequency DESC
'''

cursor.execute(frequency_query)
frequency_result = cursor.fetchall()

print('Частота встречаемости по полю year:')
for year, frequency in frequency_result:
    print(f'{year}: {frequency}')

filter_query = '''
    SELECT * FROM table1
    WHERE year > 2010
    ORDER BY duration_ms
    LIMIT ?
'''

cursor.execute(filter_query, (var + 15,))
filtered_result_rows = cursor.fetchall()

filtered_json_file_path = 'filtered_sorted_data.json'
with open(filtered_json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(filtered_result_rows, json_file, ensure_ascii=False, indent=4)

conn.close()
