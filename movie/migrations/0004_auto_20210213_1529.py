# Generated by Django 3.0.2 on 2021-02-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_movie_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
    ]