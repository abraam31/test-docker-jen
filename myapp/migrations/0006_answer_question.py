# Generated by Django 2.2.7 on 2019-11-27 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20191127_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Question')),
            ],
        ),
    ]