# Generated by Django 4.2.9 on 2024-02-04 08:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="img/", verbose_name="Изображение"
            ),
        ),
    ]
