import csv
import json
import numpy as np

origin_pool_path = "origin_pool.csv"
test_dataset_path = "test_dataset.json"

# with open(origin_pool_path, mode="r", encoding="utf-8") as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         embedding = row["embedding"]
#         embedding_data = np.array(json.loads(embedding))  # 假设 embedding 是 JSON 格式
#         print(type(embedding))

with open(test_dataset_path, mode="r", encoding="utf-8") as json_file:
    test_dataset = json.load(json_file)

questions = [item[0]["en"] for item in test_dataset[:5]]

print(questions)