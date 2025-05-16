import ast
import numpy as np
import matplotlib.pyplot as plt

losses = []
with open('loss.jsonl', 'r') as f:
    for line in f:
        data = ast.literal_eval(line)
        losses.append(data['loss'])

bucket_size = 100
num_buckets = len(losses) // bucket_size
avg_losses = [np.mean(losses[i * bucket_size:(i + 1) * bucket_size]) for i in range(num_buckets)]
plt.plot(range(len(avg_losses)), avg_losses)
plt.xlabel('Batch Number')
plt.ylabel('Average Loss')
plt.title('Loss Trend')
plt.show()