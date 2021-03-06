# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-18 13:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('flickr_id', models.CharField(max_length=200, verbose_name='Flickr Photo ID')),
                ('title', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('url', models.URLField(verbose_name='Flickr Photo url')),
            ],
            options={
                'verbose_name_plural': 'Photos',
                'verbose_name': 'Photo',
            },
        ),
        migrations.CreateModel(
            name='PhotoGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('flickr_id', models.CharField(max_length=200, verbose_name='Flickr Group ID')),
                ('name', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('no_of_photos', models.IntegerField(default=0)),
                ('url', models.URLField(verbose_name='Flickr Group Icon url')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Photo Groups',
                'verbose_name': 'Photo Group',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.AddField(
            model_name='photo',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='flickr.PhotoGroup'),
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(to='flickr.Tag'),
        ),
    ]
