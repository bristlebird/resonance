# Generated by Django 4.2.16 on 2024-12-10 17:55

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0016_episode_audiofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='audiofile',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='audio file'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
