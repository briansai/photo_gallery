import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product
from decouple import config

params = pika.URLParameters(config('AMQP_URL'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
  print('Received in admin')
  id = json.loads(body)
  product = Product.objects.get(id=id)
  product.likes += 1
  product.save()
  print('Product likes increased by 1')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()