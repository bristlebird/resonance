# Generated by Django 4.2.16 on 2024-11-25 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0011_remove_episode_creator_remove_podcast_creator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='artwork',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='artwork',
        ),
    ]