from django.db import models


# Create your models here.
class Operation(models.Model):
    # кол-во элементов внутри оператора
    NUMBER_OF_ELEMENTS = (
        ('O', 'ONE'),
        ('T', 'TWO'),
        ('M', 'MANY'),
    )
    name = models.CharField(max_length=20)
    number_of_elements = models.CharField(max_length=1, choices=NUMBER_OF_ELEMENTS)
    json_data = models.TextField()
