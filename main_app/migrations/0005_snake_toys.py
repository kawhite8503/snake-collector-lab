# Generated by Django 4.1 on 2022-08-06 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_toy_alter_feeding_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='snake',
            name='toys',
            field=models.ManyToManyField(to='main_app.toy'),
        ),
    ]