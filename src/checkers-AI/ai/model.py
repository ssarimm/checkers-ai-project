import tensorflow as tf

def build_q_network(input_shape, output_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(output_size, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model
