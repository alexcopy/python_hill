from django.db import models
from django.db.models import *


class testCsv(models.Model):
    temp_immunization_id = IntegerField(blank=False)
    legal_entity_id = CharField(max_length=54, blank=False)
    division_id = CharField(max_length=54, blank=True)
    status = CharField(max_length=34, blank=False)
    not_given = BooleanField()
    vaccine_code = CharField(max_length=21, blank=False)
    immunization_date = DateField()
    patient_age_group = CharField(max_length=12, blank=False)
    patient_gender = CharField(max_length=12, blank=False)
    manufacturer = CharField(max_length=120, blank=True)
    lot_number = CharField(max_length=12, blank=True)
    expiration_date = CharField(max_length=15, blank=True)
    dose_quantity_unit = CharField(max_length=3, blank=True)
    dose_quantity_value = CharField(max_length=4, blank=True)
    vaccination_protocols = CharField(max_length=237, blank=True)
    inserted_at = DateField()
    updated_at = DateField()
