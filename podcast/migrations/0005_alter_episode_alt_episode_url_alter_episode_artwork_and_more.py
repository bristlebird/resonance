# Generated by Django 4.2.16 on 2024-11-01 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0004_alter_podcast_options_podcast_artwork_episode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='alt_episode_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='episode',
            name='artwork',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='episode',
            name='author',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='episode',
            name='episode_number',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='keywords',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='episode',
            name='video_url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
