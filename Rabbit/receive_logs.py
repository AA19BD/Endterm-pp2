import pika
import sys
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()
channel.exchange_declare(exchange='logs',exchange_type='fanout')

result=channel.queue_declare(queue='',exclusive=True)#create the name with random name of queue
#exclusive ---if consumer connection is closed,queue is deleted
names_of_queue=result.method.queue #contains random queue name 
channel.queue_bind(exchange='logs',queue=names_of_queue)
print('[x] Waiting for logs ')

def callback(ch,method,properties,body):
    print("[x] Received %r" % body)
channel.basic_consume(queue=names_of_queue,on_message_callback=callback,auto_ack=True)

channel.start_consuming()
