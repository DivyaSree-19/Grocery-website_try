# Generated by Django 5.0.2 on 2025-02-20 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Grocery_app1', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact_no',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
