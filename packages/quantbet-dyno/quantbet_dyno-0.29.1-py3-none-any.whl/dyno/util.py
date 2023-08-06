"""Utilities that don't belong anywhere else"""

import inspect
import sys

from typing import Any

import numpy as np
import tensorflow as tf

from tensorflow.types.experimental import TensorLike
from tensorflow_probability.python.internal import prefer_static as ps


def module_classes(module: str) -> list[Any]:
    """List all the classes in the module by string"""

    return inspect.getmembers(sys.modules[module], inspect.isclass)


def pad_leading_dimension(tensor: TensorLike, size: TensorLike):
    """pad tensor with `np.nan`"""

    paddings = tf.scatter_nd(
        indices=[[0, 1]],
        updates=[size - ps.shape(tensor)[0]],
        shape=[tf.rank(tensor), 2],
    )

    return tf.pad(
        tensor=tensor, paddings=paddings, mode="CONSTANT", constant_values=np.nan
    )


def remove_leading_padding(tensor: TensorLike) -> tf.Tensor:
    """remove `np.nan` padding"""

    mask = ~tf.reduce_all(tf.math.is_nan(tensor), axis=tf.range(1, tf.rank(tensor)))

    return tf.boolean_mask(tensor=tensor, mask=mask, axis=0)
