# Generated by Django 4.2.16 on 2024-12-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0019_alter_episode_episode_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='episode_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='season_number',
            field=models.IntegerField(default=1),
        ),
    ]
