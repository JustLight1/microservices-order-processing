from orders.models import Order
from .base_consumer import BaseKafkaConsumerCommand


class Command(BaseKafkaConsumerCommand):
    help = 'Consume paid orders from Kafka and update statuses in the database'
    topic = 'payed_orders'

    def handle_message(self, message):
        order_data = message.value
        order_id = order_data.get('order_id')

        if not order_id:
            self.stdout.write(self.style.WARNING(
                'Order ID is missing in the message'))
            return

        try:
            order = Order.objects.get(id=order_id)

            if order_data.get('status') == 'shipped':
                order.status = 'paid'
                self.stdout.write(self.style.SUCCESS(
                    f'Order {order_id} has been paid'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Unknown payment status for order {order_id}'))

            order.save()
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'Order {order_id} not found in the database'))
