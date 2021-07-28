import pika
from decouple import config

params = pika.URLParameters(config('AMQP_URL'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
  properties = pika.BasicProperties(method)
  channel.basic_publish(exchange='', routing_key='main', body='hello2')

