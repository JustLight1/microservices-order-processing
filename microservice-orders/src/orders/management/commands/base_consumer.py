import json

from kafka import KafkaConsumer
from django.core.management.base import BaseCommand


class BaseKafkaConsumerCommand(BaseCommand):
    """
    Базовый класс для Kafka-потребителей.
    """
    topic = None

    def create_consumer(self):
        """
        Создает Kafka-потребитель для указанного топика.
        """
        if not self.topic:
            raise ValueError('Topic must be defined in the child class.')

        return KafkaConsumer(
            self.topic,
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        )

    def handle_message(self, message):
        """
        Обрабатывает сообщение Kafka.
        Должен быть переопределен в дочернем классе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def handle(self, *args, **kwargs):
        """
        Основной метод для обработки сообщений.
        """
        consumer = self.create_consumer()
        self.stdout.write(self.style.SUCCESS(
            f'Kafka consumer for topic "{self.topic}" started...'))

        try:
            for message in consumer:
                self.handle_message(message)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS(
                f'Kafka consumer for topic "{self.topic}" stopped'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Unexpected error occurred: {str(e)}'))
