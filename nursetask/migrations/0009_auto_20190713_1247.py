# Generated by Django 2.2.3 on 2019-07-13 17:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursetask', '0008_auto_20190713_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tdate',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
