
import tensorflow as tf
from mscale.layers import make_scale_tensor, ScaleLayer


def build_subnetwork(
    input_tensor,
    output_shape,
    units,
    output_name,
    activation="relu",
    n_blocks=1,
    layers_per_block=3,
):
    """subnetwork with the option of skip-connections

    n_blocks >= 1

    Parameters
    ----------
    input_tensor : _type_
        _description_
    output_shape : _type_
        _description_
    units : _type_
        _description_
    output_name : _type_
        _description_
    activation : str, optional
        _description_, by default "relu"
    n_blocks : int, optional
        _description_, by default 1
    layers_per_block : int, optional
        _description_, by default 3

    Returns
    -------
    _type_
        _description_
    """
    assert n_blocks >= 1, f"n_blocks must be >=1, got {n_blocks}"

    # x = tf.keras.layers.Dense(units, activation=activation)(input_tensor)
    x = input_tensor

    for _ in range(n_blocks):
        for _ in range(layers_per_block):
            x = tf.keras.layers.Dense(units, activation=activation)(x)

    # single output here?
    x = tf.keras.layers.Dense(
        output_shape, activation="linear", name=output_name)(x)

    return x


def build_model(
    input_shape=1,
    output_shape=1,
    units=[128],
    activation="relu",
    scale_activation="relu",
    n_blocks=[1],
    scales=[1],
    layers_per_block=3,
    scale_dimension=0,
    dtype=None,
    final_dense=False,
):
    """
    implementing something similar multi-scale DNN MscaleDNN version 2
    e.g. 2007.11207, 2009.12729

    But with one important difference, the scale is only applied
    to the time dimension which is assumed to be the 0-th dimension,
    other dimensions are left alone.


    Parameters
    ----------
    input_shape : int, optional
        _description_, by default 1
    output_shape : int, optional
        _description_, by default 1
    units : list, optional
        _description_, by default [128]
    activation : str, optional
        _description_, by default "relu"
    scale_activation : str, optional
        _description_, by default "relu"
    n_blocks : list, optional
        _description_, by default [1]
    scales : list, optional
        _description_, by default [1]
    layers_per_block : int, optional
        _description_, by default 3
    scale_dimension : int, optional
        _description_, by default 0
    dtype : _type_, optional
        _description_, by default None
    final_dense : bool, optional
        _description_, by default False

    Returns
    -------
    _type_
        _description_
    """

    assert (
        len(scales) == len(n_blocks) == len(units)
    ), "units, n_blocks, scales must have same length"

    input_layer = tf.keras.Input(shape=(input_shape,))

    # create sub-networks
    xs = []
    for i, scale in enumerate(scales):
        scale_tensor = make_scale_tensor(
            input_shape, scale_dimension, scale, dtype=dtype
        )
        scaled_input = ScaleLayer(scale_tensor)(input_layer)
        scaled_input = tf.keras.layers.Dense(units[i], activation=scale_activation)(
            scaled_input
        )
        xs.append(
            build_subnetwork(
                input_tensor=scaled_input,
                output_shape=output_shape,
                units=units[i],
                activation=activation,
                n_blocks=n_blocks[i],
                layers_per_block=layers_per_block,
                output_name=f"outputs_{i}",
            )
        )

    if len(xs) > 1:
        output_layer = tf.keras.layers.add([x for x in xs])
    else:
        output_layer = xs[0]

    if final_dense:
        output_layer = tf.keras.layers.Dense(output_shape, activation="linear")(
            output_layer
        )
    model = tf.keras.models.Model(inputs=input_layer, outputs=output_layer)
    return model
