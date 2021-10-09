from django.db import models


# Create your models here.
class TypeElements(models.Model):
    name = models.CharField(max_length=40)


# Create your models here.
class Operation(models.Model):
    # кол-во элементов внутри оператора
    NUMBER_OF_ELEMENTS = (
        ('O', 'ONE'),
        ('T', 'TWO'),
        ('M', 'MANY'),
    )
    name = models.CharField(max_length=20)
    description = models.TextField()
    number_of_elements = models.CharField(max_length=1, choices=NUMBER_OF_ELEMENTS)
    icon = models.CharField(max_length=256)
    type_elements = models.ManyToManyField(TypeElements)
    type_output = models.ManyToManyField(TypeElements)
    json_data = models.TextField()


class Params(models.Model):
    name = models.CharField(max_length=20)
    # Обязательность параметра
    type_object = models.ForeignKey(TypeElements, on_delete=models.CASCADE)
    obligatory = models.BooleanField()


class Functions(models.Model):
    name = models.CharField(max_length=40)
    params = models.ManyToManyField(Params)
    icon = models.CharField(max_length=256)
    type_output = models.ManyToManyField(TypeElements)


class DataTable(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=256)
    owner = models.CharField(max_length=256)
    owner_icon = models.CharField(max_length=256)
    columns = models.ManyToManyField(TypeElements)
    price = models.IntegerField()
