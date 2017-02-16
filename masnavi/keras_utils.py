from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
import numpy as np


def create_model(seqlen=None, vocab=None):
    """Returns a keras model consisting of multiple LSTMs.

    Args:
        seqlen: maximum length of sequences as the input for LSTMs.
        vocab: vocabulary (in this case consisting of characters).
    Returns:
        model: an uncompiled keras model
    """
    model = Sequential()
    model.add(LSTM(512, input_shape=(seqlen, len(vocab)),
                   return_sequences=True))
    model.add(LSTM(256, input_shape=(seqlen, len(vocab))))
    model.add(Dense(len(vocab)))
    model.add(Activation('softmax'))
    return model


def load_trained_model(weights_path, seqlen=None, vocab=None):
    """Loads a saved keras model.

    Args:
        weights_path: path to the weigts file of the model (.hdf5 file).
        seqlen: maximum sequence length. This is required as the model
                architecture has to be constructed again.
        vocab: vocabulary consisting of characters.
               Needed for model construction.
    Returns:
        a keras model
    """
    model = create_model(seqlen=seqlen, vocab=vocab)
    model.load_weights(weights_path)
    return model


def encode(text=None, maxlen=None, step=None):
    """Encodes the text in a format that can be read by keras models.

    Args:
        text: string to be encoded.
        maxlen: maximum sequence length.
        step: the step size for moving over the text.
    Returns:
        X: input vectors
        y: output vectors
        char_indices: mapping from characters to indices
        indices_char: mapping from indices to characters

    """
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
