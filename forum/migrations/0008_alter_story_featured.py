# Generated by Django 3.2.12 on 2022-03-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_alter_story_num_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
