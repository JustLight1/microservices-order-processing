# Generated by Django 5.1.4 on 2024-12-16 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outboxpayment',
            name='order_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_id',
            field=models.PositiveIntegerField(),
        ),
    ]
