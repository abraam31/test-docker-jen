# Generated by Django 2.2.7 on 2020-01-09 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_cardcontent_file_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVoiceInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_input', models.FileField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('cc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.CardContent')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Login_User')),
            ],
        ),
    ]
