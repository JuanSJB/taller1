# Generated by Django 5.1.5 on 2025-02-26 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Holiwi1', '0002_movie_genre_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
