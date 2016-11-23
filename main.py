from flask import Flask
from flask import render_template
from masnavi.predictor import predict
from masnavi.scraper.scraper import read_poems
from flask.json import jsonify
from random import shuffle
import os

app = Flask(__name__)
masnavi_poems = read_poems('data/moulavi/masnavi/poems')
shahname_poems = read_poems('data/ferdousi/shahname/poems')
hemistichs = []
CACHE_TIMEOUT = 300
for poem in masnavi_poems:
    for i in xrange(0, len(poem), 2):
        hemistich1 = poem[i].strip()
        hemistich2 = poem[i+1].strip()
        hemistichs.append((hemistich1, hemistich2))

for poem in shahname_poems:
    for i in xrange(0, len(poem), 2):
        hemistich1 = poem[i].strip()
        hemistich2 = poem[i+1].strip()
        hemistichs.append((hemistich1, hemistich2))
indices = range(0, len(hemistichs))


@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/generate', methods=["GET"])
def generate(wait=True):
    shuffle(indices)
    verse = hemistichs[indices[0]][0] + '.' + hemistichs[indices[0]][1] + '.'
    poem = predict(verse)
    print(poem)
    result = []
    parts = poem.split(".")
    if len(parts) % 2 != 0:
        parts = parts[0:10]
    for i in range(0, len(parts) - 2, 2):
        result.append([parts[i], parts[i+1]])
    return jsonify({'poem': result})


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
