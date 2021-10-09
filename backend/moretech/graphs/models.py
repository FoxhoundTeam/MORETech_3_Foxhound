from django.db import models
from rest_framework import serializers

Type_OF_ELEMENTS = (
    ('N', 'Number'),
    ('S', 'String'),
    ('D', 'Date'),
    ('T', 'DateTime'),
    ('J', 'JOINNumber'),
)


class OperationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    description = serializers.CharField()
    number_of_elements = serializers.CharField()
    icon = serializers.CharField(max_length=256)
    type_elements = serializers.CharField(max_length=1)
    type_output = serializers.CharField(max_length=1)
    json_data = serializers.CharField()


class FunctionsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    description = serializers.CharField()
    params = serializers.CharField()
    icon = serializers.CharField(max_length=256)
    owner = serializers.CharField(max_length=256)
    owner_icon = serializers.CharField(max_length=256)
    type_output = serializers.CharField(max_length=1)
    price = serializers.IntegerField()


class DataTableSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    icon = serializers.CharField(max_length=256)
    owner = serializers.CharField(max_length=256)
    owner_icon = serializers.CharField(max_length=256)
    description = serializers.CharField()
    columns = serializers.CharField()
    price = serializers.IntegerField()


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
    type_elements = models.CharField(max_length=1, choices=Type_OF_ELEMENTS)
    type_output = models.CharField(max_length=1, choices=Type_OF_ELEMENTS)
    json_data = models.TextField()


class Functions(models.Model):
    name = models.CharField(max_length=40)
    params = models.TextField()
    description = models.TextField(default='')
    icon = models.CharField(max_length=256)
    type_output = models.CharField(max_length=1, choices=Type_OF_ELEMENTS)
    owner = models.CharField(max_length=256)
    owner_icon = models.CharField(max_length=256)
    price = models.IntegerField()


class DataTable(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=256)
    owner = models.CharField(max_length=256)
    owner_icon = models.CharField(max_length=256)
    description = models.TextField()
    columns = models.TextField()
    price = models.IntegerField()
