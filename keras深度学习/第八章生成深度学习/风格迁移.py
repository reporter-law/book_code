"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:缺陷必须风格图像风格独特不需要较高层次的细节即大致在中等层次可以体现其纹理，因而风格需要独特
import os,warnings
warnings.filterwarnings("ignore")

#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""原理，不同层采样不同图像内容，顶部全局，底部局部图像，故综合两者实现分割迁移"""
from keras.preprocessing.image import load_img, img_to_array

# 内容图像
target_image_path = 'J:\PyCharm项目\学习进行中\keras深度学习\data\农村.jpg'
style_reference_image_path = 'J:\PyCharm项目\学习进行中\keras深度学习\data\星月夜.jpg'

# 生成图片的尺寸。400像素
width, height = load_img(target_image_path).size
img_height = 400
img_width = int(width * img_height / height)

"""基础函数"""
import numpy as np
from keras.applications import vgg19

"""#数组化"""
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(img_height, img_width))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img

def deprocess_image(x):
    """通过平均像素去除零中心"""
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    # 'BGR'->'RGB'
    x = x[:, :, ::-1]
    x = np.clip(x, 0, 255).astype('uint8')
    return x
from keras import backend as K

target_image = K.constant(preprocess_image(target_image_path))
style_reference_image = K.constant(preprocess_image(style_reference_image_path))

# 该占位符将包含我们生成的图像
"""应该是空载体"""
combination_image = K.placeholder((1, img_height, img_width, 3))

#我们将3张图片合并为一个批次
input_tensor = K.concatenate([target_image, style_reference_image,combination_image], axis=0)

# 我们以3批图像作为输入来构建VGG19网络。该模型将加载预训练的ImageNet权重。
model = vgg19.VGG19(input_tensor=input_tensor,
                    weights='imagenet',
                    include_top=False)
print('Model loaded.')


#计算内容损失
"""似乎是平方差"""
def content_loss(base, combination):
    return K.sum(K.square(combination - base)) #
#计算格拉姆矩阵
"""格拉姆矩阵理解：使值极化"""
#格拉姆矩阵为某一层特征图的内积，该内积可以理解成表示该层特征之间相互关系的映射
def gram_matrix(x):
    features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram
#计算风格损失
def style_loss(style, combination):
    S = gram_matrix(style)
    C = gram_matrix(combination)
    channels = 3
    size = img_height * img_width
    return K.sum(K.square(S-C) / (4. * (channels ** 2) * (size ** 2)))
#总变量方差，计算总的loss值
"""理解就是正则化损失，使损失不过大"""
def total_variation_loss(x):
    a = K.square(x[:, :img_height-1, : img_width-1, :] - x[:, 1:, : img_width-1, :])
    b = K.square(x[:, :img_height-1, : img_width-1, :] - x[:, :img_height-1, 1: ,:])
    return K.sum(K.pow(a+b, 1.25))



"""预训练层命名"""
outputs_dict = dict([(layer.name, layer.output) for layer in model.layers])
content_layer = 'block5_conv2' #用于内容损失的层
#用于风格损失的层
style_layers = ['block1_conv1',
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1']
#损失分量加权平均使用的权重
"""自定义权重"""
total_variation_weight = 1e-4
style_weight = 1.
content_weight = 0.025

"""#总的loss值"""
loss = K.variable(0.)
layer_features = outputs_dict[content_layer]
target_image_features = layer_features[0, :, :, :]
combination_features = layer_features[2, :, :, :]
"""#计算内容损失"""
loss += content_weight * content_loss(target_image_features,
                                      combination_features)
""""#添加每个目标层风格损失风量"""
for layer_name in style_layers:
    layer_features = outputs_dict[layer_name]
    style_reference_features = layer_features[1, :, :, :]
    combination_features = layer_features[2, :, :, :]
    sl = style_loss(style_reference_features, combination_features)
    loss += (style_weight / len(style_layers)) * sl

""" # 总的损失值"""
loss += total_variation_weight * total_variation_loss(combination_image)

"""# 获取损失相对于生成图像的梯度"""
grads = K.gradients(loss, combination_image)[0]
"""# 同于获取当前损失值和当前梯度值的函数,函数化"""
fetch_loss_and_grads = K.function([combination_image], [loss, grads])

"""小结：定义找到风格、内容的loss,计算总loss，计算loss的梯度"""

"""# 获取损失和梯度，同时考虑两者的计算效率更高，但是这不是必须即可以分开计算"""
from scipy.optimize import fmin_l_bfgs_b
from scipy.misc import imsave
import time
class Evaluator(object):

    def __init__(self):
        self.loss_value = None
        self.grads_values = None

    def loss(self, x):
        assert self.loss_value is None
        x = x.reshape((1, img_height, img_width, 3))
        outs = fetch_loss_and_grads([x])
        loss_value = outs[0]
        grad_values = outs[1].flatten().astype('float64')
        self.loss_value = loss_value
        self.grad_values = grad_values
        return self.loss_value

    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grad_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values

"""实例化获取函数"""
evaluator = Evaluator()
result_prefix = 'J:\PyCharm项目\学习进行中\keras深度学习\data'
iterations = 20
x = preprocess_image(target_image_path) #加载原图像
for i in range(iterations):
    print('Start of iteration', i)
    start_time = time.time()
    """#运行L-BFGS最优化，将loss最小，这是计算梯度与损失的优化scipy"""
    x, min_val, info = fmin_l_bfgs_b(evaluator.loss, x,
                                     fprime=evaluator.grads, maxfun=20)
    """求得后的损失与梯度"""
    print('Current loss value:', min_val)
    img = x.copy().reshape((img_height, img_width, 3))
    img = deprocess_image(img)
    fname = result_prefix + '_at_iteration_%d.png' % i
    imsave(fname, img)
    end_time = time.time()
    print('Image saved as', fname)
    print('Iteration %d completed in %ds' % (i, end_time - start_time))