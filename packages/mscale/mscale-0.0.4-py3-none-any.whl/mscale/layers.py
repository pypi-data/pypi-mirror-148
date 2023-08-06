import tensorflow as tf
import numpy as np


def make_scale_tensor(input_shape, scale_dimension: int, scale, dtype=None):
    """Creates a 1D tensor of ones with shape 'input_shape'. One of the dimensions
    of this tensor, given by 'scale_dimension', gets set to the value 'scale'.

    Parameters
    ----------
    input_shape : _type_
        _description_
    scale_dimension : int
        _description_
    scale : _type_
        _description_
    dtype : _type_, optional
        _description_, by default None

    Returns
    -------
    _type_
        _description_
    """
    scales = np.ones(shape=(input_shape,), dtype=dtype)
    scales[scale_dimension] = scale
    return scales


class ScaleLayer(tf.keras.layers.Layer):
    """A class to represent a neural network layer that
    does element-wise multiplication of the inputs with a scale tensor
    of the same dimension.
    """

    def __init__(self, scale_tensor, **kwargs):
        """_summary_

        Parameters
        ----------
        scale_tensor : _type_
            This can be generated using `make_scale_tensor`
        """
        super(ScaleLayer, self).__init__()
        self.scale_tensor = scale_tensor

    def call(self, inputs):
        return tf.math.multiply(inputs, self.scale_tensor)

    def get_config(self):
        config = super(ScaleLayer, self).get_config()
        config.update({"scale_tensor": self.scale_tensor})
        return config
