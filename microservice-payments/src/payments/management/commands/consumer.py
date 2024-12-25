from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from payments.models import Payment, OutboxPayment
import json
from django.db import transaction


class Command(BaseCommand):
    help = 'Consume orders from Kafka and save them to the database.'

    def handle(self, *args, **kwargs):
        consumer = KafkaConsumer(
            'new_orders',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        )

        self.stdout.write(self.style.SUCCESS('Kafka consumer started...'))

        try:
            with transaction.atomic():
                for message in consumer:
                    order_data = message.value
                    self.stdout.write('Received order data: {order_data')

                    order_id = order_data.get('order_id')

                    if order_id:
                        Payment.objects.create(order_id=order_id)
                        OutboxPayment.objects.create(order_id=order_id)
                        self.stdout.write(
                            'Saved order_id {order_id} to the database'
                        )
                    else:
                        self.stdout.write(
                            'Order ID is missing in the message.'
                        )

        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Kafka consumer stopped.'))
