import numpy as np
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras

WEIGHTS_DIR = 'weights'


class SnakeModel:

    def __init__(self):
        self.model = self._get_model()
        self._generate_initial_weights()

    def _get_model(self):
        model = keras.Sequential()
        model.add(keras.layers.InputLayer(input_shape=(7,)))
        model.add(keras.layers.Dense(7, activation=keras.activations.relu))
        model.add(keras.layers.Dense(14, activation=keras.activations.relu))
        model.add(keras.layers.Dense(3, activation=keras.activations.softmax))
        model.compile(optimizer='adam', loss=keras.losses.MAE, metrics=['acc'])
        return model

    def _generate_initial_weights(self):
        weights = self.model.get_weights()
        weights = [(np.random.rand(w.size).reshape(w.shape) * 2 - 1) for w in weights]
        self.model.set_weights(weights)

    def predict(self, state: np.array) -> np.ndarray:
        return self.model.predict(state.reshape(1, state.shape[0])).reshape(3)

    def save_weights(self, file_name, folder_name):
        os.makedirs(folder_name, exist_ok=True)
        self.model.save_weights(os.path.join(folder_name, file_name + '.w'))
