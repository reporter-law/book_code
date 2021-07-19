# 损失函数loss
这里列出了常见的损失函数与使用范围

回归问题  
| 全写 | 缩写 | 应用范围 |  
| ---- | ---- | ---- |  
| mean_squared_error | mse | 均方误差 |  
| mean_absolute_error | mae | 平均绝对误差 |   
| mean_absolute_precentage_error | mape | 平均绝对百分比误差 |  
| mean_squared_logarithmic_error | msle | 均方对数误差 |  


分类问题  
| 全写 | 缩写 | 应用范围 |  
| ---- | ---- | ---- |  
| hinge | | 铰链损失函数/最大间隔分类（SVM用的）|  
| binary_crossentropy | | （二分类）交叉熵损失函数 |  
| categorical_crossentropy | | （多分类）交叉熵损失函数【y是one-hot后的】 |  
| sparse_categorical_crossentropy | | （多分类）交叉熵损失函数【y是原始整数数据】 |  
| logcosh | | 预测误差的双曲余弦对数 |  


如何使用：  
```python
model.compile(loss='mean_squared_error', optimizer='sgd')  
model.compile(loss='mse', optimizer='sgd')  
```

后面可以使用自定义的损失函数：  
```python
def myLoss(y_pred, y_true):
    loss_value = np.abs(y_pred - y_true) ** 3  
    return loss_value
    
model.compile(loss=myLoss, optimizer='sgd') # 允许直接传入函数句柄 
```


