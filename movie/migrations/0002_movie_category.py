# Generated by Django 3.0.2 on 2021-02-08 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
