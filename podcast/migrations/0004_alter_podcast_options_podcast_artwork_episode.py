# Generated by Django 4.2.16 on 2024-11-01 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcast', '0003_podcast_explicit_content_warning'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='podcast',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='podcast',
            name='artwork',
            field=models.CharField(default='path/to/image/file', max_length=200),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('author', models.CharField(max_length=200)),
                ('keywords', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('Normal', 'Normal'), ('Trailer', 'Trailer'), ('Bonus', 'Bonus')], default='Normal')),
                ('season_number', models.IntegerField(default=1)),
                ('episode_number', models.IntegerField()),
                ('description', models.TextField()),
                ('artwork', models.CharField(max_length=200)),
                ('alt_episode_url', models.CharField(max_length=200)),
                ('video_url', models.CharField(max_length=200)),
                ('explicit_content_warning', models.BooleanField(default=False)),
                ('publish_date', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_episodes', to=settings.AUTH_USER_MODEL)),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='podcast_episodes', to='podcast.podcast')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]