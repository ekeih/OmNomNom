import emoji

VEGGIE = emoji.emojize(':ear_of_corn:')
MEAT = emoji.emojize(':poultry_leg:')


class Canteen:
    def __init__(self, id_, name, url, update, website=False):
        self.id_ = id_
        self.name = name
        self.url = url
        self.update = update
        self.website = website or url

    def __str__(self):
        return 'Canteen: %s' % self.name
