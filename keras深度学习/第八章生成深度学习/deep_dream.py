"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:反向卷积附加
import os,warnings
warnings.filterwarnings("ignore")

#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras.applications import inception_v3
from keras import backend as K

# 我们不会训练模型，因此我们使用此命令禁用所有训练专用的操作
K.set_learning_phase(0)

# 建立InceptionV3网络。该模型将加载预训练的ImageNet权重。
model = inception_v3.InceptionV3(weights='imagenet',include_top=False)
"""include_top=False意为不包含全连接层"""
#量化层的激活将对我们将要最大化的损耗造成多少影响。请注意，这些是图层名称，因为它们出现在内置的InceptionV3应用程序中。您可以使用`model.summary（）`列出所有图层名称。
"""随意确定的比重"""
model.summary()
layer_contributions = { 'mixed2': 0.2,'mixed3': 3., 'mixed4': 2.,'mixed5': 1.5,}
# 获取每个“关键”层的符号输出（我们给它们指定了唯一的名称）。
"""对每一层进行命名"""
layer_dict = dict([(layer.name, layer) for layer in model.layers])

# Define the loss.
loss = K.variable(0.)
"""创建一个浮点数占位变量，之后在每一层的输出中，计算均方差，其和记为loss"""
for layer_name in layer_contributions:
    # 将图层特征的L2范数添加到损失中。
    coeff = layer_contributions[layer_name]
    """# 获取权重"""
    activation = layer_dict[layer_name].output
    """ # 获取层激活"""

    #通过仅在损失中涉及非边界像素，我们避免了边界伪影。
    scaling = K.prod(K.cast(K.shape(activation), 'float32'))
    """ # 获取层输出的张量大小,是执行 tensorflow 中的张量数据类型转换，
    比如读入的图片是int8类型的，一定要在训练的时候把图片的数据格式转换为float32.这样就能够将其转换成 0 或 1 的序列，
    进行one-hot encoding
    K.prod:实现矩阵转化"""
    loss += coeff * K.sum(K.square(activation[:, 2: -2, 2: -2, :])) / scaling
    """# 将该层特征的L2范数添加到loss中。L2范数是指向量各元素的平方和然后求平方根,即元素平均，实现dense效果？？？？？"""
# 这保存了我们生成的图像
dream = model.input

# 计算关于损失的梦的梯度。
grads = K.gradients(loss, dream)[0]

# 归一化渐变。
"""梯度标准化"""
grads /= K.maximum(K.mean(K.abs(grads)), 1e-7)

# 设置函数以在给定输入图像的情况下检索损耗和梯度的值。
outputs = [loss, grads]
"""获取损失与梯度"""
fetch_loss_and_grads = K.function([dream], outputs)

def eval_loss_and_grads(x):
    outs = fetch_loss_and_grads([x])
    loss_value = outs[0]
    grad_values = outs[1]
    return loss_value, grad_values

"""梯度上升"""
def gradient_ascent(x, iterations, step, max_loss=None):
    for i in range(iterations):
        loss_value, grad_values = eval_loss_and_grads(x)
        if max_loss is not None and loss_value > max_loss:
            break
        print('...Loss value at', i, ':', loss_value)
        x += step * grad_values
        """反加，原为减"""
    return x
"""八度就是上升梯度的微小细节融入待改变图（细节过于微小就会看不起因而放大40%，放大后会使待改变图丢失细节因而重新注入"""
#变化如下
import scipy
from keras.preprocessing import image


"""这些是通用的图像处理函数，大小缩放，图像保存、图像格式转化"""
def resize_img(img, size):
    img = np.copy(img)
    factors = (1,
               float(size[0]) / img.shape[1],
               float(size[1]) / img.shape[2],
               1)
    return scipy.ndimage.zoom(img, factors, order=1)


def save_img(img, fname):
    pil_img = deprocess_image(np.copy(img))
    scipy.misc.imsave(fname, pil_img)


def preprocess_image(image_path):
    # Util function to open, resize and format pictures
    # into appropriate tensors.
    img = image.load_img(image_path)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = inception_v3.preprocess_input(img)
    return img


def deprocess_image(x):
    # Util function to convert a tensor into a valid image.
    if K.image_data_format() == 'channels_first':
        x = x.reshape((3, x.shape[2], x.shape[3]))
        x = x.transpose((1, 2, 0))
    else:
        x = x.reshape((x.shape[1], x.shape[2], 3))
    x /= 2.
    x += 0.5
    x *= 255.
    x = np.clip(x, 0, 255).astype('uint8')
    return x


"""八度变换"""
import numpy as np

# 使用这些超参数还将使您获得新的效果

step = 0.1  #渐变上升步长
num_octave = 10  #进行梯度上升的刻度数量
octave_scale = 1.3  # 尺寸比
iterations = 20  # 每刻度上升步数

# 如果我们的损失大于10，我们将中断梯度上升过程，以避免出现丑陋的假象
max_loss = 10.
base_image_path = r'J:\PyCharm项目\学习进行中\keras深度学习\data\base.jpg'

# 将图像加载到Numpy数组中
img = preprocess_image(base_image_path)

# 我们准备了一个形状元组列表，定义了将运行梯度上升的不同比例
original_shape = img.shape[1:3]
successive_shapes = [original_shape]
for i in range(1, num_octave):
    shape = tuple([int(dim / (octave_scale ** i)) for dim in original_shape])
    """梯度上升值不同，因为维度不同"""
    successive_shapes.append(shape)

# 反向列出形状，以便它们按升序排列
successive_shapes = successive_shapes[::-1]

# 将图像的Numpy数组调整为最小尺寸
original_img = np.copy(img)
shrunk_original_img = resize_img(img, successive_shapes[0])

for shape in successive_shapes:
    print('Processing image shape', shape)
    img = resize_img(img, shape)
    """运行梯度上升"""
    img = gradient_ascent(img,
                          iterations=iterations,
                          step=step,
                          max_loss=max_loss)
    upscaled_shrunk_original_img = resize_img(shrunk_original_img, shape)
    same_size_original = resize_img(original_img, shape)
    lost_detail = same_size_original - upscaled_shrunk_original_img

    img += lost_detail
    """丢失细节重新注入"""
    shrunk_original_img = resize_img(original_img, shape)
    save_img(img, fname='dream_at_scale_' + str(shape) + '.png')

save_img(img, fname=r'J:\PyCharm项目\学习进行中\keras深度学习\第八章生成深度学习\image\final_dream2.png')
from matplotlib import pyplot as plt

plt.imshow(deprocess_image(np.copy(img)))
plt.show()