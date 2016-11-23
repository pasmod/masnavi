from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
import numpy as np


def create_model(seqlen=None, vocab=None):
    model = Sequential()
    model.add(LSTM(256, input_shape=(seqlen, len(vocab)),
                   return_sequences=True))
    model.add(LSTM(128, input_shape=(seqlen, len(vocab))))
    model.add(Dense(len(vocab)))
    model.add(Activation('softmax'))
    return model


def load_trained_model(weights_path, seqlen=None, chars=None):
    model = create_model(seqlen=seqlen, chars=chars)
    model.load_weights(weights_path)
    return model


def encode(text=None, maxlen=None, step=None):
    sentences = []
    next_chars = []
    vocab = sorted(list(set(text)))
    char_indices = dict((c, i) for i, c in enumerate(vocab))
    indices_char = dict((i, c) for i, c in enumerate(vocab))
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    X = np.zeros((len(sentences), maxlen, len(vocab)), dtype=np.bool)
    y = np.zeros((len(sentences), len(vocab)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1
    return X, y, char_indices, indices_char
