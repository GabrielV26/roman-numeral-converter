from django.db import models

from .choices import DataTypeChoices


class DataInput(models.Model):
    data_type = models.CharField(
        max_length=1,
        choices=DataTypeChoices.choices,
        default=DataTypeChoices.TEXT,
        verbose_name="Tipo de Conversão",
    )
    value = models.CharField(max_length=32, verbose_name="Entrada")

    def __str__(self):
        return f"{self.get_data_type_display()}: {self.value}"
