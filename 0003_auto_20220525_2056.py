# Generated by Django 4.0.4 on 2022-05-25 20:56

from django.db import migrations
from django.core import serializers

fixture_filename = 'fixtures/groups.json'


def load_initial_data(apps, schema_editor):

    fixture = open(fixture_filename, 'rb')

    # get our model
    # get_model(appname, modelname)
    auth_group = apps.get_model('auth', 'Group')
    for obj in auth_group:
        obj.save()
    fixture.close()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
