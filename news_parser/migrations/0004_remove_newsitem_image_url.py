# Generated by Django 5.0.1 on 2024-01-15 19:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("news_parser", "0003_alter_newsitem_image_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newsitem",
            name="image_url",
        ),
    ]
