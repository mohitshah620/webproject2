# Generated by Django 2.2.3 on 2019-07-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursetask', '0003_auto_20190713_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurse',
            name='nid',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
