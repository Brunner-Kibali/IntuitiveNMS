# ---- Worker application to capture packets --------------------------------

import pika
import json
from CaptureThread import CaptureThread

serial_no = "5CD8095MMW"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='capture_queue', durable=True)
print('\n\n [*] Capture Worker: waiting for messages.')


def receive_capture_request(capture_channel, method, properties, body):

    print(f"capture worker: received message")
    capture_info = json.loads(body)
    print(f"capture info: {capture_info}")

    channel.basic_ack(delivery_tag=method.delivery_tag)

    if "intuitiveNMS" not in capture_info:
        intuitivenms_ip = "localhost"
    else:
        intuitive_nms_ip = capture_info["intuitiveNMS"]

    capture_thread = CaptureThread(intuitive_nms_ip, serial_no, capture_info)
    capture_thread.start()

    print('\n\n [*] Capture Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_capture_request, queue='capture_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nCapture worker shutting down")
    connection.close()
