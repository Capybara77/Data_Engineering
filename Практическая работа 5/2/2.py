import pickle
from pymongo import MongoClient
from bson import json_util
import json

client = MongoClient('localhost', 27017)

db = client['mydatabase']

file_path_task_2 = 'task_2_item.pkl'
with open(file_path_task_2, 'rb') as file_task_2:
    data_task_2 = pickle.load(file_task_2)

collection_name = 'mycollection'
collection = db[collection_name]

collection.insert_many(data_task_2)

result_salary_stats = collection.aggregate([
    {"$group": {
        "_id": None,
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
with open('result_salary_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_salary_stats), json_file, default=json_util.default, ensure_ascii=False)

result_profession_count = collection.aggregate([
    {"$group": {
        "_id": "$profession",
        "count": {"$sum": 1}
    }}
])
with open('result_profession_count.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_profession_count), json_file, default=json_util.default, ensure_ascii=False)

result_salary_stats_by_city = collection.aggregate([
    {"$group": {
        "_id": "$city",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
with open('result_salary_stats_by_city.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_salary_stats_by_city), json_file, default=json_util.default, ensure_ascii=False)

result_salary_stats_by_profession = collection.aggregate([
    {"$group": {
        "_id": "$profession",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
with open('result_salary_stats_by_profession.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_salary_stats_by_profession), json_file, default=json_util.default, ensure_ascii=False)

result_age_stats_by_city = collection.aggregate([
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
])
with open('result_age_stats_by_city.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_age_stats_by_city), json_file, default=json_util.default, ensure_ascii=False)

result_age_stats_by_profession = collection.aggregate([
    {"$group": {
        "_id": "$profession",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
])
with open('result_age_stats_by_profession.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_age_stats_by_profession), json_file, default=json_util.default, ensure_ascii=False)

result_max_salary_at_min_age = list(collection.find().sort([("age", 1), ("salary", -1)]).limit(1))
with open('result_max_salary_at_min_age.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_max_salary_at_min_age, json_file, default=json_util.default, ensure_ascii=False)

result_min_salary_at_max_age = list(collection.find().sort([("age", -1), ("salary", 1)]).limit(1))
with open('result_min_salary_at_max_age.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_min_salary_at_max_age, json_file, default=json_util.default, ensure_ascii=False)

result_age_stats_by_city_with_salary_filter = collection.aggregate([
    {"$match": {"salary": {"$gt": 50000}}},
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }},
    {"$sort": {"_id": -1}}
])
with open('result_age_stats_by_city_with_salary_filter.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_age_stats_by_city_with_salary_filter), json_file, default=json_util.default, ensure_ascii=False)

result_salary_stats_custom_filter = collection.aggregate([
    {"$match": {"$and": [
        {"$or": [
            {"age": {"$gt": 18, "$lt": 25}},
            {"age": {"$gt": 50, "$lt": 65}}
        ]},
        {"city": "Барселона"},
        {"job": {"$in": ["Учитель", "Строитель", "Программист"]}}
    ]}},
    {"$group": {
        "_id": None,
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
with open('result_salary_stats_custom_filter.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_salary_stats_custom_filter), json_file, default=json_util.default, ensure_ascii=False)

result_custom_aggregation = collection.aggregate([
    {"$match": {"job": {"$in": ["Учитель", "Строитель"]}}},
    {"$group": {
        "_id": "$city",
        "avg_salary": {"$avg": "$salary"}
    }},
    {"$sort": {"avg_salary": -1}}
])
with open('result_custom_aggregation.json', 'w', encoding='utf-8') as json_file:
    json.dump(list(result_custom_aggregation), json_file, default=json_util.default, ensure_ascii=False)

client.close()
