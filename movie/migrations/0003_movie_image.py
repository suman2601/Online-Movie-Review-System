# Generated by Django 3.0.2 on 2021-02-08 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.URLField(default=None, null=True),
        ),
    ]
