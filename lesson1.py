import importlib
import inspect
import sys
import os
import csv
import pkg_resources
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound, Http404
import random
import this
import subprocess


ROOT_URLCONF=__name__
DEBUG=True
SECRET_KEY="sdasdas"


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
    list = [str(m) for m in sys.modules]
    packages=[m for m in list if not m.startswith("_") and m.find('.') == -1]
    return ["<div><a href=\"/doc/" + d + "\" > " + d + "</a></div>" for d in packages]


def docs(_, module):
    modules = [str(m) for m in sys.modules]
    if (module not in modules):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    import_mod = importlib.import_module(module)
    getmembers = dir(import_mod)
    mem = ["<div><a href=\"/doc/" + module + "/" + i + "\" > " + i + "</a></div>" for i in getmembers if
           not i.startswith("_")]
    return HttpResponse(template.format(title="All methods", html=''.join(mem)))


def show_all_moduls(_):
    return HttpResponse(template.format(title="All modules", html=''.join(_modules())))


def documentation(_, module, meth=""):
    if meth == "":
        file_html = module
    else:
        file_html = module + "." + meth
    cmd = 'pydoc -w ' + file_html,
    subprocess.check_output(cmd, shell=True).decode("ascii", errors="ignore")
    doc_html_file = file_html + ".html"
    if os.path.exists(doc_html_file):
        with open(doc_html_file, "r", encoding='utf-8') as f:
            text = f.read()
        response = HttpResponse(template.format(title=file_html, html=text))
        os.remove(doc_html_file)
    else:
        response = Http404()
    return response


urlpatterns = [
    path('', hey),
    path('doc', show_all_moduls),
    path('doc/', show_all_moduls),
    path('doc/<str:module>', docs),
    path('doc/<str:module>/<str:meth>', documentation),
]

execute_from_command_line(sys.argv)
