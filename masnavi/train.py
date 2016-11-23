# -- coding: UTF-8 --
import arabic_reshaper
from bidi.algorithm import get_display
from keras.callbacks import ModelCheckpoint
import loader
import numpy as np
from random import shuffle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def load_poems(path, verses=[], text=""):
    poems = read_poems(path)
    for poem in poems:
        for i in xrange(0, len(poem), 2):
            hemistich1 = poem[i].strip()
            hemistich2 = poem[i+1].strip()
            verse = hemistich1 + u'.' + hemistich2 + u'.'
            verses.append(verse)
            text = text + verse
    return text, verses


text, verses = load_poems("data/moulavi/masnavi/poems", verses=[], text="")
text, verses = load_poems("data/ferdousi/shahname/poems", verses=verses,
                          text=text)


def sort_poems(verse):
    mydic = {}
    for verse in verses:
        if verse[-2] not in mydic:
            mydic[verse[-2]] = []
        mydic[verse[-2]].append(verse)
    text = ""
    for k in mydic.keys():
        for v in mydic[k]:
            text = text + v
    return text

text = sort_poems(verses)

max_verses_length = 60
max_hemistichs_length = 30

maxlen = max_hemistichs_length + 5
max_verses_length = maxlen
step = 1

padded_verses = []
for verse in verses:
    diff = max_verses_length - len(verse)
    padded_verse = verse
    for i in range(1, diff):
        padded_verse = padded_verse
    padded_verses.append(padded_verse)

chars = sorted(list(set(text)))
print('Vocabulary size', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
np.save("char_indices.npy", char_indices)
np.save("indices_char.npy", indices_char)

step = 1
sentences = []
next_chars = []
for verse in padded_verses:
    for i in range(0, len(verse) - max_hemistichs_length, step):
        sentences.append(verse[i: i + max_hemistichs_length])
        next_chars.append(verse[i + max_hemistichs_length])

sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

print('Vectorization...')
X = np.zeros((len(sentences), max_verses_length, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

model = loader.create_model(seqlen=maxlen, chars=chars)

model.compile(loss='categorical_crossentropy', optimizer='adam')
filepath = "weights-improvement-{epoch:02d}-{loss:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                             save_best_only=True,
                             mode='min')
callbacks_list = [checkpoint]


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

props = {"seqlen": maxlen, "chars": chars}
np.save("props.npy", props)
indices = range(0, len(verses))
shuffle(indices)
for iteration in range(1, 100):
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=512, nb_epoch=1, callbacks=callbacks_list)
    print("Fit finished!")

    for diversity in [0.1, 0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)
        for index in indices[0:3]:
            generated = ''
            sentence = verses[index][0: maxlen]
            generated += sentence
            reshaped_text = arabic_reshaper.reshape(sentence)
            bidi_text = get_display(reshaped_text)
            print('----- Generating with seed: "' + bidi_text + '"')

            for i in range(100):
                x = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(sentence):
                    x[0, t, char_indices[char]] = 1

                preds = model.predict(x, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = indices_char[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char
            reshaped_text = arabic_reshaper.reshape(generated)
            bidi_text = get_display(reshaped_text)
            print(bidi_text)
