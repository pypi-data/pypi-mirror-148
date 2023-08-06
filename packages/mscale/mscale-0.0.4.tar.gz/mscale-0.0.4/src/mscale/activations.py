from numpy import pi
import tensorflow as tf


def srelu(x):
    """srelu activation function defined in: 1910.11710

    Parameters
    ----------
    x : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return tf.nn.relu(-(x-1)) * tf.nn.relu(x)


def srelun(x, n):
    """generalisation of srelu. Raises srelu to the power n.

    Parameters
    ----------
    x : _type_
        _description_
    n : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return srelu(x)**n


def srelu2(x):
    """srelu squared

    Parameters
    ----------
    x : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return srelun(x, 2)


def srelu3(x):
    """srelu cubed

    Parameters
    ----------
    x : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return srelun(x, 3)


def s2relu(x):
    """sin-srelu
    presented in 2009.14597

    Parameters
    ----------
    x : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return tf.sin(2*pi*x)*srelu(x)
