import datetime
import emoji

FISH = emoji.emojize(':fish:')
MEAT = emoji.emojize(':poultry_leg:')
VEGAN = emoji.emojize(':seedling:')
VEGGIE = emoji.emojize(':ear_of_corn:')


def get_week_range(day):
    return [day + datetime.timedelta(days=i) for i in range(0 - day.weekday(), 7 - day.weekday())]


def get_current_week():
    return get_week_range(datetime.date.today())


def get_next_week():
    today = datetime.date.today()
    return get_week_range(today + datetime.timedelta(days=(7 - today.weekday())))
