# Generated by Django 4.1.2 on 2022-10-23 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_rename_end_date_usereducation_end_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
    ]