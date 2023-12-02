import json
import msgpack
import sqlite3
import os

if os.path.exists('data.db'):
    os.remove('data.db')

def read_msgpack_file(file_path):
    with open(file_path, 'rb') as file:
        data = msgpack.unpackb(file.read())
    return data

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def apply_updates(conn, updates):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    for update in updates:
        product_name = update['name']

        cursor.execute('SELECT * FROM products WHERE name = ?', (product_name,))
        product = cursor.fetchone()

        if product is not None:
            cursor.execute('UPDATE products SET counter = counter + 1 WHERE name = ?', (product_name,))
            
            if update['method'] == 'quantity_sub':
                new_quantity = max(product['quantity'] - update['param'], 0)
                cursor.execute('UPDATE products SET quantity = ? WHERE name = ?', (new_quantity, product_name))
            elif update['method'] == 'quantity_add':
                new_quantity = product['quantity'] + update['param']
                cursor.execute('UPDATE products SET quantity = ? WHERE name = ?', (new_quantity, product_name))
            elif update['method'] == 'price_percent':
                new_price = round(product['price'] * (1 + update['param']), 2)
                cursor.execute('UPDATE products SET price = ? WHERE name = ?', (new_price, product_name))
            elif update['method'] == 'available':
                cursor.execute('UPDATE products SET isAvailable = ? WHERE name = ?', (update['param'], product_name))
            elif update['method'] == 'remove':
                cursor.execute('DELETE FROM products WHERE name = ?', (product_name,))
            elif update['method'] == 'price_abs':
                new_price = abs(update['param'])
                cursor.execute('UPDATE products SET price = ? WHERE name = ?', (new_price, product_name))
            else:
                print(f"Unknown update method: {update['method']}")
                
            cursor.execute('SELECT * FROM products WHERE name = ?', (product_name,))
            updated_product = cursor.fetchone()
            if updated_product is not None:
                if updated_product['price'] < 0:
                    print(f"Invalid price for product {product_name}. Rolling back changes.")
                    conn.rollback()
                    return

    conn.commit()

product_data_file_path = 'task_4_var_48_product_data.msgpack'
update_data_file_path = 'task_4_var_48_update_data.json'

product_data = read_msgpack_file(product_data_file_path)
update_data = read_json_file(update_data_file_path)

conn = sqlite3.connect('data.db')

cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER  NOT NULL,
        fromCity TEXT NOT NULL,
        isAvailable BOOLEAN NOT NULL,
        views INTEGER NOT NULL,
        counter INTEGER NOT NULL DEFAULT 0
    )
''')

for product in product_data:
    cursor.execute('''
        INSERT INTO products (name, price, quantity, fromCity, isAvailable, views)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product['name'], product['price'], product['quantity'], product['fromCity'], product['isAvailable'], product['views']))

conn.commit()

apply_updates(conn, update_data)

top_updated_products = cursor.execute('SELECT name, counter FROM products ORDER BY counter DESC LIMIT 10').fetchall()
print("Top 10 updated products:")
for product in top_updated_products:
    print(f"{product[0]}: {product[1]} updates")

price_analysis_query = '''
    SELECT
        fromCity,
        SUM(price) AS total_price,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS avg_price,
        COUNT(*) AS product_count
    FROM products
    GROUP BY fromCity
'''
price_analysis_results = cursor.execute(price_analysis_query).fetchall()
print("\nPrice analysis by group:")
for result in price_analysis_results:
    print(f"Group: {result[0]}")
    print(f"Total Price: {result[1]}")
    print(f"Min Price: {result[2]}")
    print(f"Max Price: {result[3]}")
    print(f"Avg Price: {result[4]}")
    print(f"Product Count: {result[5]}")
    print("\n")

quantity_analysis_query = '''
    SELECT
        fromCity,
        SUM(quantity) AS total_quantity,
        MIN(quantity) AS min_quantity,
        MAX(quantity) AS max_quantity,
        AVG(quantity) AS avg_quantity,
        COUNT(*) AS product_count
    FROM products
    GROUP BY fromCity
'''
quantity_analysis_results = cursor.execute(quantity_analysis_query).fetchall()
print("Quantity analysis by group:")
for result in quantity_analysis_results:
    print(f"Group: {result[0]}")
    print(f"Total Quantity: {result[1]}")
    print(f"Min Quantity: {result[2]}")
    print(f"Max Quantity: {result[3]}")
    print(f"Avg Quantity: {result[4]}")
    print(f"Product Count: {result[5]}")
    print("\n")

custom_query = '''
    SELECT
        p.fromCity,
        AVG(p.price)
    FROM products p
    JOIN (
        SELECT fromCity, AVG(quantity) AS avg_quantity
        FROM products
        GROUP BY fromCity
    ) AS avg_quantity_per_city
    ON p.fromCity = avg_quantity_per_city.fromCity
    WHERE p.quantity > avg_quantity_per_city.avg_quantity
    GROUP BY p.fromCity
'''
custom_query_result = cursor.execute(custom_query).fetchall()
print("Custom query result:")
for result in custom_query_result:
    print(f"City: {result[0]}, Average Price for products with quantity above average: {result[1]}")

conn.close()
