import inspect
import sys
import csv
import pkg_resources
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from django.http import HttpResponse
import random
import this
import pydoc

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="sdasdas"
)
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
    modules = ['random', 'sys', 'csv', 'this', 'pydoc', 'pkg_resources']
    installed_packages = ["<div><a href=\"/doc/" + d + "\" > " + d + "</a></div>" for d in
                          modules]
    return installed_packages


def docs(_, module):
    getmembers = inspect.getmembers(eval(module))
    mem = ["<div><a href=\"/doc/" + module + "/" + i[0] + "\" > " + i[0] + "</a></div>" for i in getmembers if
           not i[0].startswith("_")]
    return HttpResponse(template.format(title="All methods", html=''.join(mem)))


def show_all_moduls(_):
    return HttpResponse(template.format(title="All modules", html=''.join(_modules())))


def methods(_, module, meth):
    return HttpResponse(template.format(title="All modules", html=pydoc.render_doc(module + "." + meth, "Help on %s")))


urlpatterns = [
    path('', hey),
    path('doc', show_all_moduls),
    path('doc/<str:module>', docs),
    path('doc/<str:module>/<str:meth>', methods),
]

execute_from_command_line(sys.argv)
