# Generated by Django 5.1.6 on 2025-03-06 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
