from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ]
    order_id = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment {self.id} for Order {self.order_id}'


class OutboxPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled')
    ]
    topic_name = models.CharField(max_length=50)
    order_id = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'Message {self.topic_name}, status {self.status} '
                'for order {self.order_id}')
