# Generated by Django 2.2.7 on 2019-12-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_auto_20191213_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='login_user',
            name='facebook_login',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='login_user',
            name='gmail_login',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='login_user',
            name='normal_login',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='login_user',
            name='uid',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='login_user',
            name='phone_number',
            field=models.BigIntegerField(null=True),
        ),
    ]
