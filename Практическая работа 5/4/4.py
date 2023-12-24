# https://www.kaggle.com/datasets/bhavikjikadara/heart-failure-prediction
# https://www.kaggle.com/datasets/matviyamchislavskiy/1990-2019-depression-and-gdp-per-capita-everywhere

import pandas as pd
from pymongo import MongoClient
from bson import json_util

client = MongoClient()
db = client['health_data']
collection_heart = db['heart_data']
collection_depressive = db['depressive_data']

heart_data = pd.read_csv('heart_failure_clinical_records.csv')
heart_data = heart_data.to_dict(orient='records')
collection_heart.insert_many(heart_data)

import json

with open('depressive-disorders-prevalence-vs-gdp-per-capita.json', 'r') as file:
    depressive_data = json.load(file)

collection_depressive.insert_many(depressive_data)

# выборка данных
query_1_heart = list(collection_heart.find({"age": {"$gt": 60}}))
query_1_depressive = list(collection_depressive.find({"Year": 2015}))

# выборка с агрегацией
query_2_heart = list(collection_heart.aggregate([
    {"$group": {"_id": "$smoking", "count": {"$sum": 1}}}
]))
query_2_depressive = list(collection_depressive.aggregate([
    {"$group": {"_id": "$Continent", "count": {"$sum": 1}}}
]))

# обновление данных
collection_heart.update_many({"sex": 1}, {"$inc": {"ejection_fraction": 5}})
collection_depressive.update_many({"Entity": "Abkhazia"}, {"$set": {"Year": 2016}})

# удаление данных по условию
collection_heart.delete_many({"age": {"$lt": 40}})
collection_depressive.delete_many({"Year": {"$lt": 2015}})

# группировка данных
query_5_heart = list(collection_heart.aggregate([
    {"$group": {"_id": "$smoking", "average_age": {"$avg": "$age"}}}
]))
query_5_depressive = list(collection_depressive.aggregate([
    {"$group": {"_id": "$Continent", "total_entries": {"$sum": 1}}}
]))

# выборка данных
query_6_heart = list(collection_heart.find({"sex": 0}).limit(3))
query_6_depressive = list(collection_depressive.find({"Year": 2016}).limit(3))

# выборка с агрегацией
query_7_heart = list(collection_heart.aggregate([
    {"$group": {"_id": "$diabetes", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 2}
]))
query_7_depressive = list(collection_depressive.aggregate([
    {"$group": {"_id": "$Continent", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 2}
]))

# обновление данных
collection_heart.update_many({"diabetes": 0}, {"$inc": {"creatinine_phosphokinase": 50, "serum_sodium": 3}})
collection_depressive.update_many({"Entity": "Afghanistan"}, {"$set": {"Year": 2017}})

# удаление данных по условию
collection_heart.delete_many({"time": {"$lt": 50}})
collection_depressive.delete_many({"Year": {"$gt": 2016}})

# группировка данных
query_10_heart = list(collection_heart.aggregate([
    {"$group": {"_id": "$diabetes", "average_ejection_fraction": {"$avg": "$ejection_fraction"}}}
]))
query_10_depressive = list(collection_depressive.aggregate([
    {"$group": {"_id": "$Continent", "total_entries": {"$sum": 1}}}
]))

results = {
    "Query 1 Heart": json.loads(json_util.dumps(query_1_heart)),
    "Query 1 Depressive": json.loads(json_util.dumps(query_1_depressive)),
    "Query 2 Heart": json.loads(json_util.dumps(query_2_heart)),
    "Query 2 Depressive": json.loads(json_util.dumps(query_2_depressive)),
    "Query 5 Heart": json.loads(json_util.dumps(query_5_heart)),
    "Query 5 Depressive": json.loads(json_util.dumps(query_5_depressive)),
    "Query 6 Heart": json.loads(json_util.dumps(query_6_heart)),
    "Query 6 Depressive": json.loads(json_util.dumps(query_6_depressive)),
    "Query 7 Heart": json.loads(json_util.dumps(query_7_heart)),
    "Query 7 Depressive": json.loads(json_util.dumps(query_7_depressive)),
    "Query 10 Heart": json.loads(json_util.dumps(query_10_heart)),
    "Query 10 Depressive": json.loads(json_util.dumps(query_10_depressive)),
}

with open('query_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)

client.close()