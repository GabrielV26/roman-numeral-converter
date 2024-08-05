from django.db import models
from .choices import DataTypeChoices


class DataInput(models.Model):
    data_type = models.CharField(
        max_length=1,
        choices=DataTypeChoices.choices,
        default=DataTypeChoices.TEXT,
        verbose_name="Tipo de Conversão"
    )
    value = models.TextField(verbose_name="Entrada")

    def save(self, *args, **kwargs):
        if self.data_type == DataTypeChoices.TEXT:
            self.value = int(self.value)
        elif self.data_type == DataTypeChoices.FLOAT:
            self.value = float(self.value)
        super().save(*args, **kwargs)
