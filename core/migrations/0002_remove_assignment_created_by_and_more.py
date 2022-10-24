# Generated by Django 4.1.2 on 2022-10-23 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='breakingnews',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='breakingnews',
            name='story',
        ),
        migrations.RemoveField(
            model_name='breakingnews',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='filepreview',
            name='article',
        ),
        migrations.RemoveField(
            model_name='filepreview',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='filepreview',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='rtg',
            name='story',
        ),
        migrations.RemoveField(
            model_name='rtg',
            name='vo',
        ),
        migrations.RemoveField(
            model_name='rundown',
            name='articles',
        ),
        migrations.RemoveField(
            model_name='rundown',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='rundown',
            name='set_by',
        ),
        migrations.RemoveField(
            model_name='rundown',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='category',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='on_air_cat',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='reporter',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='voiceover',
            name='story',
        ),
        migrations.RemoveField(
            model_name='window',
            name='story',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Assignment',
        ),
        migrations.DeleteModel(
            name='BreakingNews',
        ),
        migrations.DeleteModel(
            name='FilePreview',
        ),
        migrations.DeleteModel(
            name='RTG',
        ),
        migrations.DeleteModel(
            name='Rundown',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.DeleteModel(
            name='Ticker',
        ),
        migrations.DeleteModel(
            name='VoiceOver',
        ),
        migrations.DeleteModel(
            name='Window',
        ),
    ]
