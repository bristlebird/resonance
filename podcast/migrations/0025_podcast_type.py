# Generated by Django 4.2.16 on 2024-12-12 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0024_alter_podcast_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='type',
            field=models.CharField(choices=[('Episodic', 'episodic'), ('Serial', 'serial')], default='episodic'),
        ),
    ]