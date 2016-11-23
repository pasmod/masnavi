from scraper import read_poems


MAPPING = {'masnavi': 'data/moulavi/masnavi/poems',
           'shahname': 'data/ferdousi/shahname/poems'}


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


def sort_poems(verses):
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


def load(poems=['masnavi', 'shahname']):
    verses = []
    text = ""
    for poem in poems:
        if poem in MAPPING.keys():
            text, verses = load_poems(MAPPING[poem],
                                      verses=verses, text=text)
        else:
            raise KeyError("Poem {} is not found!".format(poem))
    return sort_poems(verses)
