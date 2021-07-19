# 评价函数 metrics

| 函数 | 使用范围 |  
| ---- | ----- |  
| accuracy | （普适）准确率 |  
| binary_accuracy | （二分类）准确率【y是one-hot】 |  
| categorical_accuracy | （多分类）准确率【y是one-hot】 |  
| top_k_categorical_accuracy | （多分类）准确率【y是one-hot】 |  
| sparse_categorical_accuracy | （多分类）准确率【y是整数数据】 |  
| sparse_top_k_categorical_accuracy | （多分类）准确率【y是整数数据】 |  


如何使用
```python
model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])
```
