# 优化器 Optimizer

这些优化器都在 tensorflow.keras.optimizers 下

---------------

## SGD 【常用】
```python
SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
```
参数  
* lr: float >= 0. 学习率。
* momentum: float >= 0. 参数，用于加速 SGD 在相关方向上前进，并抑制震荡。
* decay: float >= 0. 每次参数更新后学习率衰减值。
* nesterov: boolean. 是否使用 Nesterov 动量。

-----------------

## RMSprop 【常用】
```python
RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
```
参数  
* lr: float >= 0. 学习率。
* rho: float >= 0. RMSProp梯度平方的移动均值的衰减率.
* epsilon: float >= 0. 模糊因子. 若为 None, 默认为 K.epsilon()。
* decay: float >= 0. 每次参数更新后学习率衰减值。

------------------

## Adam 【常用】
```python
Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
```
参数  
* lr: float >= 0. 学习率。
* beta_1: float, 0 < beta < 1. 通常接近于 1。
* beta_2: float, 0 < beta < 1. 通常接近于 1。
* epsilon: float >= 0. 模糊因子. 若为 None, 默认为 K.epsilon()。
* decay: float >= 0. 每次参数更新后学习率衰减值。
* amsgrad: boolean. 是否应用此算法的 AMSGrad 变种，来自论文 "On the Convergence of Adam and Beyond"。

--------------------

## Adagrad
```python
Adagrad(lr=0.01, epsilon=None, decay=0.0)
```
参数  
* lr: float >= 0. 学习率.
* epsilon: float >= 0. 若为 None, 默认为 K.epsilon().
* decay: float >= 0. 每次参数更新后学习率衰减值.

---------------

## Adadelta
```python
Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
```
参数  
* lr: float >= 0. 学习率，建议保留默认值。
* rho: float >= 0. Adadelta梯度平方移动均值的衰减率。 
* epsilon: float >= 0. 模糊因子. 若为 None, 默认为 K.epsilon()。
* decay: float >= 0. 每次参数更新后学习率衰减值。

------------

## Adamax
```python
Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
```
参数  
* lr: float >= 0. 学习率。
* beta_1/beta_2: floats, 0 < beta < 1. 通常接近于 1。
* epsilon: float >= 0. 模糊因子. 若为 None, 默认为 K.epsilon()。
* decay: float >= 0. 每次参数更新后学习率衰减值。

--------------------

## Nadam
```python
Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
```

参数  
* lr: float >= 0. 学习率。
* beta_1/beta_2: floats, 0 < beta < 1. 通常接近于 1。
* epsilon: float >= 0. 模糊因子. 若为 None, 默认为 K.epsilon()。





