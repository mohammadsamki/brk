# Generated by Django 5.0.4 on 2024-05-04 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('briansclub', '0014_alter_billing_amount_btc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='amount_btc',
            field=models.DecimalField(decimal_places=10, max_digits=10, null=True),
        ),
    ]
