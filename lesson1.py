import importlib
import logging
import re
import string
import sys
import os
from pathlib import Path
from dotenv import dotenv_values
from django.conf import settings
from django.core.management import execute_from_command_line
from django.shortcuts import render, redirect
from django.urls import path, re_path
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseBadRequest
import random
import this
import subprocess
import db.dbconn as dbconn

ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = "sdasdas"

APP_PATH = Path(__file__).parent.absolute()
URLS_MAP = {}
SHR_RND = 5
DOT_ENV = dotenv_values(APP_PATH.joinpath(".env"))

log_file = DOT_ENV['LOG_FILE']
level = logging.DEBUG
log_format = '%(asctime)s : %(levelname)s : %(message)s'
logs_dir = DOT_ENV['LOG_DIR']

Path(logs_dir).mkdir(parents=True, exist_ok=True)
handlers = [logging.FileHandler(logs_dir + '/' + log_file), logging.StreamHandler()]
logging.basicConfig(level=level, format=log_format, handlers=handlers)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APP_PATH.joinpath("templates")],
    },
]

text = ''.join(this.d.get(c, c) for c in this.s)

title, _, *quotes = text.splitlines()


def single_quote(_):
    return render(_, 'docs.html', {'html': random.choice(quotes), 'template': TEMPLATES})


def _modules():
    list = [str(m) for m in sys.modules]
    packages = [m for m in list if not m.startswith("_") and m.find('.') == -1]
    return ["<div><a href=\"/doc/" + d + "\" > " + d + "</a></div>" for d in packages]


def _rnd_string(min_limit, max_limit):
    chars = string.ascii_letters.join(string.digits)
    str_range = random.randint(min_limit, max_limit)
    return ''.join(random.choice(chars) for i in range(str_range))


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
    return render(_, 'docs.html', {'html': ''.join(_modules()), 'template': TEMPLATES})


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


def short_links(request):
    try:
        if request.method == 'POST' and re.match(r"^(http|ftp)s?://", request.POST.get('url', '')):
            url = request.POST.get('url', '')
            rnd_key = _rnd_string(5, 5)
            slug_url = DOT_ENV['APP_URL'] + "/" + rnd_key
            dbconn.insert_data(rnd_key, url)
        elif request.method == 'GET':
            return render(request, 'short_urls.html', {'template': TEMPLATES})
        else:
            msg = "provided URL's protocol isn't supported request is empty<br>  supported protocols are: "
            error_msg = "http(s) and ftp(s)"
            return render(request, 'error.html', {'error': msg, 'desc': error_msg, 'template': TEMPLATES})
    except Exception as ex:
        logging.error(ex)
        return HttpResponseBadRequest("Something went very wrong please check")

    return render(request, 'short_urls.html',
                  {'html': slug_url, 'slug_url': slug_url, 'url': rnd_key, 'template': TEMPLATES})


def shorturl(request, key):
    if len(key) > 5:
        return ''

    url_pair = dbconn.get_key_from_db(key)
    if request.method == 'GET' and len(url_pair) == 1:
        return redirect(url_pair[key])
    return redirect('index')

dbconn.create_db()
dbconn.mysql_db_create_tbl()

urlpatterns = [

    path('', single_quote, name='index'),
    path('quote', single_quote),
    path('short', short_links),
    path('doc', show_all_moduls),
    path('doc/', show_all_moduls),
    path('doc/<str:module>', docs),
    path('doc/<str:module>/<str:meth>', documentation),
    re_path(r'(?P<key>\w{5,5}$)', shorturl, name='shorturl'),

]

execute_from_command_line(sys.argv)
