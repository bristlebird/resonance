# Generated by Django 4.2.16 on 2024-11-28 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0014_podcast_excerpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='alt_episode_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='video_url',
            field=models.URLField(blank=True),
        ),
    ]
