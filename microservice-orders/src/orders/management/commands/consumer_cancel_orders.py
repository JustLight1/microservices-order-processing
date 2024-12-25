from orders.models import Order
from .base_consumer import BaseKafkaConsumerCommand


class Command(BaseKafkaConsumerCommand):
    help = 'Consume cancelled orders from Kafka and update statuses in db'
    topic = 'cancel_orders'

    def handle_message(self, message):
        order_data = message.value
        order_id = order_data.get('order_id')

        if not order_id:
            self.stdout.write(self.style.WARNING(
                'Order ID is missing in the message'))
            return

        try:
            order = Order.objects.get(id=order_id)
            order.status = 'cancelled'
            self.stdout.write(self.style.SUCCESS(
                f'Order {order_id} has been cancelled'))
            order.save()
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'Order {order_id} not found in the database'))
