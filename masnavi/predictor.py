import numpy as np
import loader


def load_numpy_model(modelpath):
    """Loads the stored numpy objects.

    Args:
        modelpath: path to the model files.
    Returns:
        numpy object containing the model.
    """
    return np.load(modelpath).item()


# Load all stored models
props = load_numpy_model("models/props.npy")
seqlen = props["seqlen"]
chars = props["chars"]
char_indices = load_numpy_model("models/char_indices.npy")
indices_char = load_numpy_model("models/indices_char.npy")
model = loader.load_trained_model("models/weights.hdf5",
                                  seqlen=seqlen, chars=chars)


def sample(preds, temperature=1.0):
    """Samples from a probability distribution.

    Args:
        preds: probabilities returned by the softmax layer.
        temperature: higher temperatures result in higher creativity!
    Returns:
        the maximum of preds
    """
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def predict(poem, diversity=0.3):
    """Given a model, predict the rest of the poem.

    Args:
        poem: starting point for poem generation.
        diversity: higher diversity results in higher creativity!
    Returns:
        generated: the generated poem
    """
    generated = ''
    sentence = poem[0: seqlen]
    generated += sentence
    for i in range(400):
        x = np.zeros((1, seqlen, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char
    return generated
