# Generated by Django 5.0.4 on 2024-04-12 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('briansclub', '0008_billing_order_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainAPIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255)),
                ('api_key', models.CharField(max_length=255)),
            ],
        ),
    ]
