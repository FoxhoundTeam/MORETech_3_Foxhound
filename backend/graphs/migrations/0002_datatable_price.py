# Generated by Django 3.2.7 on 2021-10-09 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datatable',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
