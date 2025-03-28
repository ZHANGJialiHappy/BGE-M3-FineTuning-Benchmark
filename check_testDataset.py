
import csv
import json

# from urllib.parse import unquote


# csv_file_path = "embedding_text.csv"  
# uri_column_name = "source_uri"  

# matches = []
# with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         uri = row[uri_column_name]
#         if unquote(uri).split("/")[-1] == "C1 0288 3.2.4-01.html" :
#             print(uri)




# 文件路径
test_dataset_path = "test_dataset.json"
origin_pool_path = "origin_pool.csv"

# 加载 test_dataset.json
with open(test_dataset_path, mode="r", encoding="utf-8") as json_file:
    test_dataset = json.load(json_file)

# 加载 origin_pool.csv 的 source_uri 列
source_uris = set()
with open(origin_pool_path, mode="r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        source_uris.add(row["source_uri"])

# 检查每个 answer 是否存在于 source_uris 中
missing_answers = []
for item in test_dataset:
    answers = item[1]  # 获取 answer 列表
    for answer in answers:
        # 检查 answer 是否存在于 source_uris 的任何一项中
        if not any(answer in uri  for uri in source_uris):
            missing_answers.append(answer)

# 打印未找到的 answers
if missing_answers:
    print("Missing answers:")
    for answer in missing_answers:
        print(answer)
else:
    print("All answers are present in origin_pool.csv.")

