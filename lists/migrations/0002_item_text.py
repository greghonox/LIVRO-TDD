# Generated by Django 3.1.7 on 2021-04-06 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='text',
            field=models.TextField(default=str),
            preserve_default=False,
        ),
    ]
