import matplotlib.pyplot as plt
import numpy as np


models = ['DeepSeek-Coder (1.3B)', 'Qwen2.5-Coder (1.5B)', 'Llama 3.2 (1B)']

scores = [8.5, 9.0, 6.5]  


times = [12.5, 10.2, 5.8]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


colors = ['#4CAF50', '#2196F3', '#FF9800'] 
bars1 = ax1.bar(models, scores, color=colors)
ax1.set_title('So sánh Chất lượng Phân tích (Thang điểm 10)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Điểm số', fontsize=12)
ax1.set_ylim(0, 10.5)
ax1.grid(axis='y', linestyle='--', alpha=0.7)


for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}', ha='center', va='bottom', fontsize=12, fontweight='bold')


bars2 = ax2.bar(models, times, color=['#8BC34A', '#03A9F4', '#FFC107'])
ax2.set_title('Tốc độ phản hồi trung bình (Giây)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Thời gian (s)', fontsize=12)
ax2.grid(axis='y', linestyle='--', alpha=0.7)


for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}s', ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show() 