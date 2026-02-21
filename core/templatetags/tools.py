# from django.contrib.humanize.templatetags.humanize import intcomma
# from modules.auths.models import Account
# from django import template
# import pyshorteners
# from num2words import num2words

# register = template.Library()

# @register.filter(name="to_words")
# def to_words(value):
#     return num2words(value, lang='es').upper()

# @register.filter(name="get_complete_name")
# def get_complete_name(username):
#     if username is not None:
#         account = Account.getAccount(username)
#         if account is not None:
#             return account.complete_name
#     return "&nbsp;"

# @register.simple_tag(takes_context=True)
# def get_short_url(context, relative_url):
#     s = pyshorteners.Shortener()
#     absolute_url = ''
#     absolute_url += context.request.environ['wsgi.url_scheme']
#     absolute_url +=  '://'
#     absolute_url += context.request.environ['HTTP_HOST']
#     absolute_url += relative_url
#     short_url = s.tinyurl.short(absolute_url)
#     return short_url
