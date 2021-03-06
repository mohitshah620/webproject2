# Generated by Django 2.2.3 on 2019-07-13 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursetask', '0007_auto_20190713_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurse',
            name='password',
            field=models.CharField(default='pass', max_length=10),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='nid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
