# Generated by Django 3.1.13 on 2021-11-23 11:37

from django.db import migrations, models
import todos.models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='day',
            field=models.CharField(default=todos.models.getday, max_length=50, unique=True),
        ),
    ]
