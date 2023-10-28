import csv

name = "text_4_var_48"
var = 48
age = 25 + (var % 10)

avg_salary = 0
data = list()

with open(name, newline="\n", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        item = {
            "number": int(row[0]),
            "name": row[2] + ' ' + row[1],
            "age": int(row[3]),
            "salary": int(row[4][0:-1])
        }

        avg_salary += item["salary"]
        data.append(item)

avg_salary /= len(data)

sorted = sorted(filter(lambda item: item["salary"] > avg_salary and item["age"] > age, data), key=lambda item: item["number"])

for item in sorted:
    item["salary"] = str(item["salary"]) + "₽"

with open("result_" + name, 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in sorted:
        writer.writerow(item.values())
