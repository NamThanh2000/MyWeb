# Generated by Django 3.2.12 on 2022-03-05 04:57

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='title'),
        ),
    ]
