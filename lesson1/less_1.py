import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from django.http import HttpResponse
from random import choice
import this

ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = "sdasdas"

template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css">
  </head>
  <body>
  <section class="section">
    <div class="container">
         <div class="box">
          {quote}
        </div>
         <div class="box">
          {quote_two}
        </div>
    </div>
  </section>
  </body>
</html>
"""
text = ''.join(this.d.get(c, c) for c in this.s)

title, _, *quotes = text.splitlines()


def hey(_):
    return HttpResponse(template.format(title=title, quote=choice(quotes), quote_two=choice(quotes)))


def universe(_):
    return HttpResponse('New Page about')


urlpatterns = [
    path('', hey),
    path('retro', universe)
]

execute_from_command_line(sys.argv)
