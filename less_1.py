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


execute_from_command_line(sys.argv)
