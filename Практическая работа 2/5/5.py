import json
import csv
import statistics
import msgpack
import pickle
import os

with open('items.json', 'r') as json_file:
    data = json.load(json_file)

selected_fields = ['Price', 'QuantityInStock', 'WeightInGrams', 'LengthInCentimeters', 'WidthInCentimeters', 'UnitsSold']

results = {}

for field in selected_fields:
    values = [item[field] for item in data]

    if isinstance(values[0], (int, float)):
        results[field] = {
            "Max": max(values),
            "Min": min(values),
            "Mean": statistics.mean(values),
            "Sum": sum(values),
            "StdDev": statistics.stdev(values)
        }
    elif isinstance(values[0], str):
        frequency = {}
        for value in values:
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1
        results[field] = frequency

with open('results.json', 'w') as json_result_file:
    json.dump(results, json_result_file)

with open('data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(selected_fields)
    for item in data:
        writer.writerow([item[field] for field in selected_fields])

with open('data.msgpack', 'wb') as msgpack_file:
    packed_data = msgpack.packb(data)
    msgpack_file.write(packed_data)

with open('data.pkl', 'wb') as pickle_file:
    pickle.dump(data, pickle_file)
    
def get_file_size(file_path):
    return os.path.getsize(file_path)

json_size = get_file_size('results.json')
csv_size = get_file_size('data.csv')
msgpack_size = get_file_size('data.msgpack')
pkl_size = get_file_size('data.pkl')

print(f"Размер results.json: {json_size} байт")
print(f"Размер data.csv: {csv_size} байт")
print(f"Размер data.msgpack: {msgpack_size} байт")
print(f"Размер data.pkl: {pkl_size} байт")