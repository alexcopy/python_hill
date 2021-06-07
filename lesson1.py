import importlib
import inspect
import sys
import os
import csv
import pkg_resources
from django.conf import settings
from django.core.management import execute_from_command_line
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound, Http404
import random
import this
import subprocess

ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = "sdasdas"

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/Users/alexredko/Projects/Python/Hillel/'],

    },
]

text = ''.join(this.d.get(c, c) for c in this.s)

title, _, *quotes = text.splitlines()


def hey(_):
    return render(_, 'index.html', {'html': random.choice(quotes), 'template': TEMPLATES})


def _modules():
    list = [str(m) for m in sys.modules]
    packages = [m for m in list if not m.startswith("_") and m.find('.') == -1]
    return ["<div><a href=\"/doc/" + d + "\" > " + d + "</a></div>" for d in packages]


def docs(_, module):
    modules = [str(m) for m in sys.modules]
    if (module not in modules):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    import_mod = importlib.import_module(module)
    getmembers = dir(import_mod)
    mem = ["<div><a href=\"/doc/" + module + "/" + i + "\" > " + i + "</a></div>" for i in getmembers if
           not i.startswith("_")]
    return render(_, 'clean.html', {'html': ''.join(mem), 'template': TEMPLATES})


def show_all_moduls(_):
    return render(_, 'index.html', {'html': ''.join(_modules()), 'template': TEMPLATES})


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
        response = render(_, 'clean.html', {'html': text, 'template': TEMPLATES})
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
