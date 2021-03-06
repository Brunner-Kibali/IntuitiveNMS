# ---- Worker application to scan host ports etc. --------------------------------

import pika
import json
from PortscanThread import PortscanThread

serial_no = "5CD8095MMW"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='portscan_queue', durable=True)
print('\n\n [*] Portscan Worker: waiting for messages.')


def receive_portscan_request(portscan_channel, method, properties, body):

    print(f"portscan worker: received message")
    portscan_info = json.loads(body)
    print(f"portscan info: {portscan_info}")

    channel.basic_ack(delivery_tag=method.delivery_tag)

    if "host_ip" not in portscan_info or "host_name" not in portscan_info or "token" not in portscan_info:
        print(f"portscan worker: missing information in portscan_info: {portscan_info}")
    else:
        if "intuitiveNMS" not in portscan_info:
            intuitive_nms_ip = "localhost"
        else:
            intuitivenms_ip = portscan_info["intuitiveNMS"]

        portscan_thread = PortscanThread(intuitivenms_ip, serial_no, portscan_info)
        portscan_thread.start()

    print('\n\n [*] Portscan Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_portscan_request, queue='portscan_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nPortscan worker shutting down")
    connection.close()