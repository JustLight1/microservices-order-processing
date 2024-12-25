from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from payments.models import Payment, OutboxPayment
from .serializers import PaymentSerializer
from .producer import send_outbox_messages


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами.
    """
    queryset = Payment.objects.all().order_by('-create_at')
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод создания платежа для добавления в OutboxPayment.
        """
        order = Payment.objects.filter(status='pending').first()

        if not order:
            return Response(
                {'message': 'No pending orders to process.'},
                status=status.HTTP_200_OK
            )

        try:
            with transaction.atomic():
                order.status = 'paid'
                order.save()

                OutboxPayment.objects.create(
                    topic_name='payed_orders',
                    payment_id=order.id,
                    order_id=order.order_id
                )
                print(
                    f'Order {order.id} processed and added to OutboxPayment.')

            send_outbox_messages()
            print(f'Kafka message sent for order {order.id}')

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            order.status = 'failed'
            order.save()
            print(f'Failed to process order {order.id}: {str(e)}')
            return Response(
                {'message': f'Failed to process order {order.id}: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
