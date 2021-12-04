import pika
import json
from decouple import config
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_microservices.settings")
django.setup()


params = pika.URLParameters(config('RABBITMQ_KEY'))

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='return_historical')
queue_name = 'return_historical'


def callback(ch, method, properties, body):
    body = json.loads(body)
    load_data_historical(body)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Started consume wait return historical')
channel.start_consuming()
