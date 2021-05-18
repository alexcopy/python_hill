import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from django.http import HttpResponse
from random import choice
import this

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="sdasdas"
)
template = """

<!DOCTYPE html>
 <html >

    <head>{title}</head>
    <body>
 
    <h2>{quote}</h2>
    </body>

</html>

"""
text = ''.join(this.d.get(c, c) for c in this.s)

title, _, *quotes = text.splitlines()


def hey(_):
    return HttpResponse(template.format(title=title, quote=choice(quotes)))


def universe(_):
    return HttpResponse('New Page about')


urlpatterns = [
    path('', hey),
    path('retro', universe)
]

execute_from_command_line(sys.argv)
