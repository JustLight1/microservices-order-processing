from orders.models import Order
from .base_consumer import BaseKafkaConsumerCommand


class Command(BaseKafkaConsumerCommand):
    help = 'Consume shipped orders from Kafka and update statuses in database'
    topic = 'sent_orders'

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
                order.status = 'shipped'
                self.stdout.write(self.style.SUCCESS(
                    f'Order {order_id} has been shipped'))
            elif order_data.get('status') == 'delivered':
                order.status = 'delivered'
                self.stdout.write(self.style.SUCCESS(
                    f'Order {order_id} has been delivered'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Unknown delivery status for order {order_id}'))

            order.save()
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'Order {order_id} not found in the database'))
