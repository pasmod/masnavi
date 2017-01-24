# -- coding: UTF-8 --
from keras.callbacks import ModelCheckpoint
from bidi.algorithm import get_display
from predictor import predict
import arabic_reshaper
import numpy as np
import keras_utils
import loader
import random

# Maximum sequence length
maxlen = 35
# Step size for moving over the text
step = 1

text = loader.load(poems=['masnavi', 'shahname'])
X, y, char_indices, indices_char = keras_utils.encode(text=text,
                                                      maxlen=maxlen,
                                                      step=1)
np.save("models/char_indices.npy", char_indices)
np.save("models/indices_char.npy", indices_char)
np.save("models/props.npy", {"seqlen": maxlen, "chars": char_indices.keys()})

model = keras_utils.create_model(seqlen=maxlen, vocab=char_indices.keys())
model.compile(loss='categorical_crossentropy', optimizer='adam')
filepath = "models/weights.hdf5"
checkpoint = ModelCheckpoint(filepath,
                             monitor='loss',
                             verbose=1,
                             save_best_only=True,
                             mode='min')
callbacks_list = [checkpoint]


for iteration in range(1, 100):
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=512, nb_epoch=1, callbacks=callbacks_list)
    print("Fit finished!")
    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.1, 0.2, 0.3, 0.4]:
        print('----- diversity:', diversity)
        sentence = text[start_index: start_index + maxlen]
        generated = predict(sentence, diversity=diversity)
        reshaped_text = arabic_reshaper.reshape(generated)
        print(get_display(reshaped_text))
