# Generated by Django 5.0.2 on 2024-06-30 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Grocery_app1', '0004_delete_quantityvariant'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuantityVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=100)),
            ],
        ),
    ]