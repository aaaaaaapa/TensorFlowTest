#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Python version: 3.5.4
'''
@File    :   tf_data_generator.py
@Time    :   2021/11/04 16:11:19
@Author  :   Wu Xueru
@Version :   1.0
@Contact :   t01051@163.com
@License :
@Desc    :
'''

# here put the import lib
import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
from time import strftime


my_dataset_path = 'datasets/training'
my_image_size = (33,101)
my_input_shape = my_image_size + (3,)
# 指定训练次数
my_train_epochs = 2
# 指定batch
my_batch = 32
# shuffle buffer size
my_shuffle_buffer_size = 1000

AUTOTUNE = tf.data.experimental.AUTOTUNE

# 获取所有文件路径
dataset_path = pathlib.Path(my_dataset_path)
all_images_paths = [str(path) for path in list(dataset_path.glob('*'))]
print('所有文件的路径:', all_images_paths)
print('文件总数:', len(all_images_paths))

# 获取标签名称
label_name =[i.split('\\')[2].split('.')[0] for i in all_images_paths]
print('标签名称:', label_name)
# 因为训练时参数必须为数字，因此为标签分配数字索引
label_index = dict((name,int(name))for index,name in enumerate(label_name))
print('为标签分配数字索引:', label_index)

# 将图片与标签的数字索引进行配对(number encodeing)
number_encodeing = [label_index[i.split('\\')[2].split('.')[0]]for i in all_images_paths]
print('number_encodeing:', number_encodeing, type(number_encodeing))
label_one_hot = tf.keras.utils.to_categorical(number_encodeing)
print('label_one_hot:', label_one_hot)


def process(path,label):
    # 读入图片文件
    image = tf.io.read_file(path)
    # 将输入的图片解码为gray或者rgb
    image = tf.image.decode_jpeg(image, channels=my_input_shape[2])
    # 调整图片尺寸以满足网络输入层的要求
    image = tf.image.resize(image, my_image_size)
    # 归一化
    image /= 255.
    return image,label

# 将数据与标签拼接到一起
path_ds = tf.data.Dataset.from_tensor_slices((all_images_paths, tf.cast(label_one_hot, tf.int32)))
image_label_ds = path_ds.map(process, num_parallel_calls=AUTOTUNE)
print('image_label_ds:', image_label_ds)
steps_per_epoch=tf.math.ceil(len(all_images_paths)/my_batch).numpy()
print('steps_per_epoch', steps_per_epoch)

# 打乱dataset中的元素并设置batch
image_label_ds = image_label_ds.shuffle(my_shuffle_buffer_size).batch(my_batch)


if __name__ == '__main__':
    # 定义模型
    # 输入层
    input_data = tf.keras.layers.Input(shape=my_input_shape)
    # 第一层
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(input_data)
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.MaxPool2D(pool_size=[2,2], strides=2, padding='same')(middle)
    # 第二层
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.MaxPool2D(pool_size=[2,2], strides=2, padding='same')(middle)
    # 第三层
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.Conv2D(128, kernel_size=[3,3], strides=(1,1), padding='same', activation=tf.nn.relu)(middle)
    middle = tf.keras.layers.MaxPool2D(pool_size=[2,2], strides=2, padding='same')(middle)

    # 铺平
    dense = tf.keras.layers.Flatten()(middle)
    dense = tf.keras.layers.Dropout(0.1)(dense)
    dense = tf.keras.layers.Dense(60, activation='relu')(dense)
    # 输出
    # 输出层
    output_data = tf.keras.layers.Dense(len(label_name), activation='softmax')(dense)
    # 确认输入位置和输出位置
    model = tf.keras.Model(inputs=input_data, outputs=output_data)

    # 定义模型的梯度下降和损失函数
    model.compile(optimizer=tf.optimizers.Adam(1e-4),
                loss=tf.losses.categorical_crossentropy,
                metrics=['accuracy'])

    # 打印模型结构
    model.summary()

    # 开始训练
    start_time = strftime("%Y-%m-%d %H:%M:%S")
    history = model.fit(
        image_label_ds,
        epochs=my_train_epochs,
        verbose=1,
        steps_per_epoch=int(steps_per_epoch))

    end_time = strftime("%Y-%m-%d %H:%M:%S")
    print('开始训练的时间：', start_time)
    print('结束训练的时间：', end_time)
