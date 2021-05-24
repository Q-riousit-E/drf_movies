# Generated by Django 3.2.3 on 2021-05-24 05:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_simplerating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailedrating',
            name='characters',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='detailedrating',
            name='cinematography',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='detailedrating',
            name='entertainment_value',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='detailedrating',
            name='music_score',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='detailedrating',
            name='originality',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='detailedrating',
            name='plot',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
