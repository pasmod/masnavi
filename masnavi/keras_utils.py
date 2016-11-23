from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM


def create_model(seqlen=None, chars=None):
    model = Sequential()
    model.add(LSTM(256, input_shape=(seqlen, len(chars)),
                   return_sequences=True))
    model.add(LSTM(128, input_shape=(seqlen, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))
    return model


def load_trained_model(weights_path, seqlen=None, chars=None):
    model = create_model(seqlen=seqlen, chars=chars)
    model.load_weights(weights_path)
    return model
