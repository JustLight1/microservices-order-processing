# Generated by Django 5.1.4 on 2024-12-23 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_outboxpayment_order_id_alter_payment_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outboxpayment',
            name='payment_id',
        ),
        migrations.AlterField(
            model_name='outboxpayment',
            name='order_id',
            field=models.PositiveIntegerField(),
        ),
    ]
