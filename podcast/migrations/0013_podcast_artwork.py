# Generated by Django 4.2.16 on 2024-11-27 14:24

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0012_remove_episode_artwork_remove_podcast_artwork'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='artwork',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image'),
        ),
    ]