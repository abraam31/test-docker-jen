# Generated by Django 2.2.7 on 2019-12-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20191213_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login_user',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]
