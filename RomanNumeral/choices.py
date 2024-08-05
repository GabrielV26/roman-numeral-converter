# results/choices.py
from django.db import models


class DataTypeChoices(models.TextChoices):
    FLOAT = 'F', 'Real para Romano'
    TEXT = 'T', 'Romano para Real'
