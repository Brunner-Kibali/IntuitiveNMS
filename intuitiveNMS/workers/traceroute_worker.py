# ---- Worker application to traceroute packets --------------------------------

import pika
import json
from TracerouteThread import TracerouteThread

serial_no = "5CD8095MMW"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='traceroute_queue', durable=True)
print('\n\n [*] Traceroute Worker: waiting for messages.')


def receive_traceroute_request(traceroute_channel, method, properties, body):

    print(f"traceroute worker: received message")
    traceroute_info = json.loads(body)
    print(f"traceroute info: {traceroute_info}")

    channel.basic_ack(delivery_tag=method.delivery_tag)

    if "intuitiveNMS" not in traceroute_info:
        intuitivenms_ip = "localhost"
    else:
        intuitivenms_ip = traceroute_info["intuitiveNMS"]

    traceroute_thread = TracerouteThread(intuitivenms_ip, serial_no, traceroute_info)
    traceroute_thread.start()

    print('\n\n [*] Traceroute Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_traceroute_request, queue='traceroute_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nTraceroute worker shutting down")
    connection.close()