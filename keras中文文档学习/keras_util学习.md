

#keras.utils.CustomObjectScope()
==custom_objects
即自定义层的加载方式

#keras.utils.HDF5Matrix
一种数据格式，与numpy数据格式一样

#keras.utils.normalize
好像是数据缩放，如0-1之间？？

#keras.utils.get_file
下载数据集>>>requests

#keras.utils.plot_model
将 Keras 模型转换为 dot 格式并保存到文件中。

#multi_gpu_model
将模型复制到不同的 GPU 上。

具体来说，该功能实现了单机多 GPU 数据并行性。 它的工作原理如下：

将模型的输入分成多个子批次。
在每个子批次上应用模型副本。 每个模型副本都在专用 GPU 上执行。
将结果（在 CPU 上）连接成一个大批量。
例如， 如果你的 batch_size 是 64，且你使用 gpus=2， 那么我们将把输入分为两个 32 个样本的子批次， 在 1 个 GPU 上处理 1 个子批次，然后返回完整批次的 64 个处理过的样本。

这实现了多达 8 个 GPU 的准线性加速。

此功能目前仅适用于 TensorFlow 后端

关于模型保存

要保存多 GPU 模型，请通过模板模型（传递给 multi_gpu_model 的参数）
调用 .save(fname) 或 .save_weights(fname) 以进行存储，
而不是通过 multi_gpu_model 返回的模型。

parallel_model = multi_gpu_model(model, gpus=8)

parallel_model.compile(loss='categorical_crossentropy',
                       optimizer='rmsprop')

这个 `fit` 调用将分布在 8 个 GPU 上。
由于 batch size 是 256, 每个 GPU 将处理 32 个样本。

parallel_model.fit(x, y, epochs=20, batch_size=256)

通过模版模型存储模型（共享相同权重）：

model.save('my_model.h5')
