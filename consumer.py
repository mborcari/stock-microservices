import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_microservices.settings")
import django
django.setup()
#Need set variabel on heroku container
# heroku config:set DJANGO_SETTINGS_MODULE=stocks_microservices.settings -a <appcontainername>
import pika
import json
from decouple import config
from stocks.views import load_data_historical

params = pika.URLParameters(config('RABBITMQ_KEY'))
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='return_historical', durable=True)
queue_name = 'return_historical'

def callback(ch, method, properties, body):
    print(f'Receive message from {queue_name}')
    body = json.loads(body)
    load_data_historical(body)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(f'Started consume waiting message from queue {queue_name}')
channel.start_consuming()
