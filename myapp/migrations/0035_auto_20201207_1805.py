# Generated by Django 2.2.7 on 2020-12-07 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0034_folder_recent_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardcontent',
            name='recent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='recent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='settable',
            name='recent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
