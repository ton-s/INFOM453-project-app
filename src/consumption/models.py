from django.db import models


class HeatingPrices(models.Model):
    date = models.DateField(unique=True)
    price = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.price}"
