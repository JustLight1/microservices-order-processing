from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from orders.models import Order, OutboxOrder
from .serializers import OrderSerializer
from .producer import send_outbox_messages


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами.
    """
    queryset = Order.objects.all().order_by('-create_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод создания заказа для добавления в OutboxOrder.
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                order = serializer.save()

                OutboxOrder.objects.create(
                    topic_name='new_orders',
                    order_id=order.id,
                    user=order.user
                )
                print(f'Order {order.id} created and added to OutboxOrder')

                send_outbox_messages()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f'Failed to process order {order.id}: {str(e)}')
            return Response(
                {'message': 'Failed to create order.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
