# preeti_converter.py

PREETI_MAP = {
"k|f=": "प्रा",
"sfof": "का",
"sf]": "को",
"df": "मा",
"jf": "वा",
"g": "न",
"l": "ि",
"o": "े",
"u": "ु",
"f": "ा",
"k": "प",
"v": "भ",
"x": "ह",
"z": "श",
"c": "च",
"d": "द",
"e": "ए",
"j": "ज",
"t": "त",
"y": "य",
"b": "ब",
"m": "म",
"n": "न",
"p": "प",
"r": "र",
"s": "स",
"w": "व"
}

def preeti_to_unicode(text):
    for k, v in PREETI_MAP.items():
        text = text.replace(k, v)
    return text