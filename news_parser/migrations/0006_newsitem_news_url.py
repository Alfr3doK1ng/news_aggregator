# Generated by Django 5.0.1 on 2024-01-15 22:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news_parser", "0005_newsitem_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsitem",
            name="news_url",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
