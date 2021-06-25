import re
import os
import csv, sys
from typing import Dict, Union
from dateutil import parser as date_parser
from datetime import datetime

model_path = 'model.py'
csv_file = sys.argv[1].strip()
if not csv_file:
    csv_file = input("Please enter path to CSV file with data: ").strip()

reader = csv.DictReader(open(csv_file))
# fieldnames = dict.fromkeys(reader.fieldnames, "CharField(max_length=291)")
fieldnames = dict.fromkeys(reader.fieldnames)
field_types = {}
unchecked_list = {}

field_types: Dict[str, Dict[str, Union[None, int, bool]]] = {}
list_data = list(reader)


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def checkIfDuplicates(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def is_date_parsing(date_str):
    try:
        return bool(date_parser.parse(date_str))
    except ValueError:
        return False


def is_parsible(date_str):
    try:
        return bool(datetime.strptime(date_str, '%Y-%m-%d'))
    except ValueError:
        return False


for i in fieldnames:
    fieldnames[i] = []
    field_types[i] = {"Type": "", "length": 0, 'nullable': False}
d = {}
for row in list_data:
    for k in fieldnames:
        field_type = field_types[k]
        cel_val = row[k].strip()

        if cel_val == '':
            field_type['nullable'] = True

        if field_type['Type'].startswith("CharField"):
            str_len = int(len(cel_val) * 1.5)
            field_type["length"] = str_len if str_len > field_type["length"] else field_type["length"]
            field_type['Type'] = "CharField({})".format(
                'max_length=' + str(field_type["length"]) + ', blank=' + str(field_type['nullable']))


        elif cel_val.isdigit():
            field_type['Type'] = "IntegerField({})".format('blank=' + str(field_type['nullable']))
            cel_val = int(cel_val)
            field_type["length"] = cel_val if cel_val > field_type["length"] else field_type["length"]
            fieldnames[k].append(cel_val)

        elif cel_val.isdecimal():
            field_type['Type'] = "FloatField({})".format('blank=' + str(field_type['nullable']))
            cel_val = float(cel_val)
            field_type["length"] = cel_val if cel_val > field_type["length"] else field_type["length"]
            fieldnames[k].append(cel_val)

        elif cel_val.lower() in ['true', 'false']:
            field_type['Type'] = "BooleanField()"
            fieldnames[k].append(cel_val)

        elif is_parsible(cel_val):
            field_type['Type'] = "DateField()"
            fieldnames[k].append(cel_val)

        else:
            str_len = int(len(cel_val) * 1.5)
            field_type["length"] = str_len if str_len > field_type["length"] else field_type["length"]
            field_type['Type'] = "CharField({})".format(
                'max_length=' + str(field_type["length"]) + ', blank=' + str(field_type['nullable']))

base = os.path.basename(csv_file)
name, _ = os.path.splitext(base)
eol = "\n"
data = "from django.db import models" + eol
data += "from django.db.models import *" + eol * 3
data += 'class {}(models.Model):'.format(to_camel_case(name)) + eol

for i in field_types:
    data += "    " + "{} = {}".format(i, field_types[i]['Type']) + eol

with open(model_path, "w") as f:
    f.write(data)

# TextField()
# URLField
# TimeField
# URLField
# UUIDField
# PositiveBigIntegerField
# JSONField
# IntegerField
# FloatField
# FilePathField
# EmailField
# DateTimeField
# DateField
# BooleanField
# AutoField
