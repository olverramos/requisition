from django.utils.safestring import mark_safe
from modules.phrases.models import Phrase
from django import template


register = template.Library()

@register.filter(name='getrange') 
def getrange(number):
    return range(1, number + 1)

@register.simple_tag
def random_phrase():
    text_phrase = ""
    phrase = Phrase.getRandom()
    if phrase is not None:
        text_phrase = f'"{phrase.text}" - <i>{phrase.author}</i>'
    return mark_safe(text_phrase)

@register.filter
def get_item(dictionary, key):
    if dictionary is not None:
        return dictionary.get(key)
