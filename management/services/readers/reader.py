import locale


class Reader:
    # Setea la variable LC_ALL al conjunto de UTF-8 con descripción español España
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    def __init__(self):
        self.dictionary = {"article": [], "gallery": [], "video": []}

    def save_item(self, itemdictionary, type):
        self.dictionary[type].append(itemdictionary)

    @classmethod
    def translate_keys(cls, dictionary):
        return {"notas": dictionary["article"],
                "galerias": dictionary["gallery"],
                "videos": dictionary["video"]}
