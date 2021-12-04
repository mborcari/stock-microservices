import pika
from decouple import config


params = pika.URLParameters(config('RABBITMQ_KEY'))
connection = pika.BlockingConnection(params)
channel = connection.channel()
queue_name = 'get_historical'


def publish(dict_data):
    print(f'Publish queue: {queue_name}')
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=dict_data)
