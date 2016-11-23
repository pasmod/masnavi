# -- coding: UTF-8 --
import arabic_reshaper
from bidi.algorithm import get_display
from keras.callbacks import ModelCheckpoint
import keras_utils
import loader
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


text = loader.load(poems=['masnavi', 'shahname'])

maxlen = 35
step = 1

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
np.save("models/char_indices.npy", char_indices)
np.save("models/indices_char.npy", indices_char)


def encode(text=None, maxlen=None, step=None):
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1
    return X, y

X, y = encode(text=text, maxlen=maxlen, step=1)

model = keras_utils.create_model(seqlen=maxlen, chars=chars)

model.compile(loss='categorical_crossentropy', optimizer='adam')
filepath = "weights-improvement-{epoch:02d}-{loss:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                             save_best_only=True,
                             mode='min')
callbacks_list = [checkpoint]


props = {"seqlen": maxlen, "chars": chars}
np.save("props.npy", props)
for iteration in range(1, 100):
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=512, nb_epoch=1, callbacks=callbacks_list)
    print("Fit finished!")
    import random
    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.1, 0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)
        sentence = text[start_index: start_index + maxlen]
        from predictor import predict
        generated = predict(sentence, diversity=diversity)
        reshaped_text = arabic_reshaper.reshape(generated)
        bidi_text = get_display(reshaped_text)
        print(bidi_text)
