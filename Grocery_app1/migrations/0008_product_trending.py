# Generated by Django 5.0.2 on 2024-07-08 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Grocery_app1', '0007_rename_image_product_image2'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='trending',
            field=models.BooleanField(default=False),
        ),
    ]