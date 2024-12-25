from kafka import KafkaProducer
from orders.models import OutboxOrder
import json


def send_outbox_messages():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

    pending_messages = OutboxOrder.objects.filter(status='pending')
    for message in pending_messages:
        try:
            producer.send(
                'new_orders',
                value={
                    'order_id': message.order_id,
                    'user': message.user,
                    'status': message.status,
                },
            )
            producer.flush()
            message.status = 'shipped'
            message.save()
        except Exception as e:
            print(f'Failed to send message {message.id}: {str(e)}')
            message.status = 'cancelled'
            message.save()
