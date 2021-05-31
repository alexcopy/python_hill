import inspect
import sys
import csv
import pkg_resources
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound
import random
import this
import pydoc

ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = "sdasdas"
MODULES_LIST = ['random', 'sys', 'csv', 'this', 'pydoc', 'pkg_resources']

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
          {html}
        </div>
    </div>
  </section>
  </body>
</html>
"""
text = ''.join(this.d.get(c, c) for c in this.s)

title, _, *quotes = text.splitlines()


def hey(_):
    return HttpResponse(template.format(title=title, html=random.choice(quotes)))


def _modules():
    packages = ["<div><a href=\"/doc/" + d + "\" > " + d + "</a></div>" for d in
                MODULES_LIST]
    return packages


def docs(_, module):
    if (module not in MODULES_LIST):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    getmembers = inspect.getmembers(eval(module))
    mem = ["<div><a href=\"/doc/" + module + "/" + i[0] + "\" > " + i[0] + "</a></div>" for i in getmembers if
           not i[0].startswith("_")]
    return HttpResponse(template.format(title="All methods", html=''.join(mem)))


def show_all_moduls(_):
    return HttpResponse(template.format(title="All modules", html=''.join(_modules())))


def methods(_, module, meth):
    return HttpResponse(pydoc.render_doc(module + "." + meth, "%s"))


urlpatterns = [
    path('', hey),
    path('doc', show_all_moduls),
    path('doc/<str:module>', docs),
    path('doc/<str:module>/<str:meth>', methods),
]

execute_from_command_line(sys.argv)
