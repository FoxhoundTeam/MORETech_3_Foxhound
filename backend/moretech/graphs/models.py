from django.db import models

Type_OF_ELEMENTS = (
    ('J', 'join'),
    ('O', 'operation'),
    ('F', 'filter'),
    ('T', 'output'),
)


# Create your models here.
class Operation(models.Model):
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=128)
    type_element = models.CharField(max_length=1, choices=Type_OF_ELEMENTS)
    many = models.BooleanField()
    inputs = models.TextField()
    outputs = models.TextField()


class Feature(models.Model):
    name = models.CharField(max_length=512)
    data = models.TextField()
    user_id = models.IntegerField()
    price = models.IntegerField()


class DataTable(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    icon = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    size = models.CharField(max_length=256)
    tag = models.TextField()
    loaddate = models.CharField(max_length=256)
