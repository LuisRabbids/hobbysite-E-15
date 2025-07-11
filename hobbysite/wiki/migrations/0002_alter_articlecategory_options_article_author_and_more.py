# Generated by Django 5.2.1 on 2025-05-09 03:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'Article Categories'},
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wiki_articles', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='wiki_header_images/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='wiki.articlecategory'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='wiki.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wiki_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
