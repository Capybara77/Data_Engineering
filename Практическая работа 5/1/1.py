import msgpack
from pymongo import MongoClient
from bson import json_util
import json

client = MongoClient('localhost', 27017)

db = client['mydatabase']

file_path = 'task_1_item.msgpack'
with open(file_path, 'rb') as file:
    data = msgpack.load(file)

collection_name = 'mycollection'
collection = db[collection_name]

collection.delete_many({})

collection.insert_many(data)

result_1 = list(collection.find().sort("salary", -1).limit(10))
with open('result_1.json', 'w', encoding='utf-8') as json_file_1:
    json.dump(result_1, json_file_1, default=json_util.default, ensure_ascii=False)

result_2 = list(collection.find({"age": {"$lt": 30}}).sort("salary", -1).limit(15))
with open('result_2.json', 'w', encoding='utf-8') as json_file_2:
    json.dump(result_2, json_file_2, default=json_util.default, ensure_ascii=False)

result_3 = list(collection.find({
    "$and": [
        {"city": "Барселона"},
        {"job": {"$in": ["Инженер", "Врач", "Учитель"]}}
    ]
}).sort("age", 1).limit(10))
with open('result_3.json', 'w', encoding='utf-8') as json_file_3:
    json.dump(result_3, json_file_3, default=json_util.default, ensure_ascii=False)

result_4_count = collection.count_documents({
    "$and": [
        {"age": {"$gte": 25, "$lte": 40}},
        {"year": {"$in": [2019, 2022]}},
        {"$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]}
    ]
})
result_4 = {"count": result_4_count}
with open('result_4.json', 'w', encoding='utf-8') as json_file_4:
    json.dump(result_4, json_file_4, default=json_util.default, ensure_ascii=False)

client.close()
