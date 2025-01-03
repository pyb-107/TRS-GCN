import tensorflow.compat.v1 as tf
import numpy as np

# 该类是对GCN网络参数的初始化
# uniform(shape, scale=0.05, name=None)：使用均匀分布初始化变量。
# glorot(shape, name=None)：使用Glorot初始化方法（也称为Xavier初始化）来初始化变量，适合深度神经网络中的权重初始化。
# zeros(shape, name=None)：将变量初始化为全零。
# ones(shape, name=None)：将变量初始化为全一。
def uniform(shape, scale=0.05, name=None):
    """Uniform init."""
    initial = tf.random_uniform(shape, minval=-scale, maxval=scale, dtype=tf.float32)
    return tf.Variable(initial, name=name)


def glorot(shape, name=None):
    """Glorot & Bengio (AISTATS 2010) init."""
    init_range = np.sqrt(6.0/(shape[0]+shape[1]))
    initial = tf.random_uniform(shape, minval=-init_range, maxval=init_range, dtype=tf.float32)
    return tf.Variable(initial, name=name)


def zeros(shape, name=None):
    """All zeros."""
    initial = tf.zeros(shape, dtype=tf.float32)
    return tf.Variable(initial, name=name)


def ones(shape, name=None):
    """All ones."""
    initial = tf.ones(shape, dtype=tf.float32)
    return tf.Variable(initial, name=name)