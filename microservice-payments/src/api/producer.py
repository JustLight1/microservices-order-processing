
from kafka import KafkaProducer
from payments.models import OutboxPayment
import json


def send_outbox_messages():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

    pending_messages = OutboxPayment.objects.filter(status='pending')
    for message in pending_messages:
        try:
            message.status = 'shipped'
            producer.send(
                'payed_orders',
                value={
                    'order_id': message.order_id,
                    'status': message.status,
                },
            )
            producer.flush()

            message.save()
        except Exception as e:
            print(f'Failed to send message {message.id}: {str(e)}')
            message.status = 'cancelled'
            message.save()
