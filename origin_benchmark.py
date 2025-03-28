import csv
import json
import numpy as np
import pandas as pd
from FlagEmbedding import BGEM3FlagModel
from urllib.parse import unquote

# 文件路径
test_dataset_path = "test_dataset.json"
pool_path = "pool.csv"
mix_output_csv_path = "origin_mix_incorrect_questions.csv"
dense_output_csv_path = "origin_dense_incorrect_questions.csv"
sparse_output_csv_path = "origin_sparse_incorrect_questions.csv"

# 加载 test_dataset.json
with open(test_dataset_path, mode="r", encoding="utf-8") as json_file:
    test_dataset = json.load(json_file)

# 提取 English questions
questions = [item[0]["en"] for item in test_dataset]

# 加载 fine_tune_pool.csv
embedding_texts = []
source_uris = []
with open(pool_path, mode="r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        embedding_texts.append(row["embedding_text"])
        source_uris.append(row["source_uri"])




# 初始化 bge-m3 模型
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)


# calculate Matrix of Dense

# Generate Dense Embedding List to English questions
dense_question_embeddings = model.encode(questions, batch_size=12)['dense_vecs']
dense_text_embddings = model.encode(embedding_texts, batch_size=12)['dense_vecs']

# 计算距离矩阵（余弦相似度）
distance_matrix = dense_question_embeddings @ dense_text_embddings.T

# 获取每个问题最近的 3 个索引
top_3_indices_dense = np.argsort(-distance_matrix, axis=1)[:, :3]  # 按相似度降序排序
# 获取每个问题最近的 5 个索引
top_5_indices_dense = np.argsort(-distance_matrix, axis=1)[:, :5] 



# calculate Matrix of Sparse

# 生成 sparse Embedding for English questions
sparse_question_embeddings = model.encode(questions, return_dense=True, return_sparse=True, return_colbert_vecs=False)['lexical_weights']
sparse_texts_embeddings = model.encode(embedding_texts, return_dense=True, return_sparse=True, return_colbert_vecs=False)['lexical_weights']


# create index matrix for sparse

top_2_indices_sparse = []
top_5_indices_sparse = []
for q_embedding in sparse_question_embeddings:
    distances = []
    for idx, p_embedding in enumerate(sparse_texts_embeddings):
        distance = model.compute_lexical_matching_score(q_embedding, p_embedding)
        distances.append((idx, distance))  # store index and distance
    # 按距离降序排列
    distances.sort(key=lambda x: x[1], reverse=True)
    # 提取前 2 项的索引
    top_2_indices = [item[0] for item in distances[:2]]
    top_2_indices_sparse.append(top_2_indices)

    # 提取前 5 项的索引
    top_5_indices = [item[0] for item in distances[:5]]
    top_5_indices_sparse.append(top_5_indices)




# 比对答案并统计得分
mix_score = 0
mix_incorrect_questions = []

dense_score=0
dense_incorrect_questions = []

sparse_score=0
sparse_incorrect_questions = []

for i, item in enumerate(test_dataset):
    answers = item[1]  # 获取答案列表

    mix_top_indices = set(top_3_indices_dense[i]) | set(top_2_indices_sparse[i])  # 获取最近的 3 +2  个索引

    top_mix_source_uris = [unquote(source_uris[idx]).split("/")[-1] for idx in mix_top_indices]  # 提取对应的 source_uri

    top_5_dense_source_uris = [unquote(source_uris[idx]).split("/")[-1] for idx in set(top_5_indices_dense[i])]  # 提取对应的 source_uri

    top_5_sparse_source_uris = [unquote(source_uris[idx]).split("/")[-1] for idx in set(top_5_indices_sparse[i])]  # 提取对应的 source_uri


    # 检查答案和最近的 source_uri 是否有交集

    if bool(set(answers) & set(top_mix_source_uris)):
        mix_score += 1
    else:
        mix_incorrect_questions.append({"question": item[0]["en"], "answers": answers, "top_uris": top_mix_source_uris})

    if bool(set(answers) & set(top_5_dense_source_uris)):
        dense_score += 1
    else:
        dense_incorrect_questions.append({"question": item[0]["en"], "answers": answers, "top_uris": top_mix_source_uris})

    if bool(set(answers) & set(top_5_sparse_source_uris)):
        sparse_score += 1
    else:
        sparse_incorrect_questions.append({"question": item[0]["en"], "answers": answers, "top_uris": top_mix_source_uris})

# 输出得分
total_questions = len(test_dataset)
print(f"origin_mix_score: {mix_score}/{total_questions}")
print(f"origin_dense_score: {dense_score}/{total_questions}")
print(f"origin_sparse_score: {sparse_score}/{total_questions}")

# 将3+2答错的题目保存到 CSV 文件
pd.DataFrame(mix_incorrect_questions).to_csv(mix_output_csv_path, index=False, encoding="utf-8")
print(f"Mixed method: Incorrect questions saved to {mix_output_csv_path}")

pd.DataFrame(dense_incorrect_questions).to_csv(dense_output_csv_path, index=False, encoding="utf-8")
print(f"Dense method: Incorrect questions saved to {dense_output_csv_path}")

pd.DataFrame(sparse_incorrect_questions).to_csv(sparse_output_csv_path, index=False, encoding="utf-8")
print(f"Sparse method: Incorrect questions saved to {sparse_output_csv_path}")

