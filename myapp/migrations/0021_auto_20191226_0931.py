# Generated by Django 2.2.7 on 2019-12-26 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_settable'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Folder'),
        ),
        migrations.AddField(
            model_name='category',
            name='settbl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.SetTable'),
        ),
    ]
