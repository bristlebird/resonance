# Generated by Django 4.2.16 on 2024-11-01 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0007_remove_episode_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='episode_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]