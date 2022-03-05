# Generated by Django 3.2.12 on 2022-03-05 06:04

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=True, max_length=255, populate_from='title', unique=True),
        ),
    ]
