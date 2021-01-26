# ---- Worker application --------------------------------

import pika
import json
from CaptureThread import CaptureThread
import argparse
import os
import threading
import sys
import time

from WorkerThread import WorkerThread

if os.geteuid() != 0:
    exit("You must have root privileges to run this script, try using 'sudo'.")

parser = argparse.ArgumentParser(description="Remote worker for intuitiveNMS")
parser.add_argument(
    "-Q",
    "--intuitiveNMS",
    required=True,
    help="intuitiveNMS hostname or IP, required for heartbeat",
)
parser.add_argument(
    "-W",
    "--workertype",
    required=True,
    help="Type of worker, currently 'capture', 'portscan', or 'traceroute'",
)
parser.add_argument(
    "-C",
    "--connectiontype",
    default="rabbitmq",
    help="Connection type, currently 'rabbitmq' or 'http'",
)
parser.add_argument(
    "-S", "--serialno", required=True, help="A preferably unique id of worker"
)
parser.add_argument(
    "-H",
    "--heartbeat",
    default="30",
    help="Frequency of heartbeats sent to intuitiveNMS server, in seconds",
)

args = parser.parse_args()

intuitiveNMS = args.intuitiveNMS
worker_type = args.workertype
connection_type = args.connectiontype
serial_no = args.serialno
heartbeat = args.heartbeat

if (
    worker_type not in {"capture", "portscan", "traceroute"}
    or connection_type not in {"rabbitmq", "http",}
    or not heartbeat.isnumeric()
):
    parser.print_help()
    exit()

print(f"intuitiveNMS worker: {worker_type}")
print(f"    ---- intuitiveNMS: {intuitiveNMS}")
print(f"    ---- serial: {serial_no}")
print(f"    ---- connection: {connection_type}")
print(f"    ---- heartbeat: {heartbeat}")
print()

workerThread = WorkerThread(intuitivenms=intuitiveNMS,
                            worker_type=worker_type,
                            serial_no=serial_no,
                            connection_type=connection_type,
                            heartbeat=heartbeat)

# try:
workerThread.start()


def shutdown():

    print(f"\n\n\n---> {worker_type} worker: Entering shutdown sequence")
    workerThread.terminate = True
    workerThread.join()
    print(f"\n---> {worker_type} worker: all worker threads shut down, terminating.")


import atexit
atexit.register(shutdown)


# except BaseException as e:
# except KeyboardInterrupt as e:
#     print(f"\nintuitiveNMS_worker: {worker_type} worker: begin shutting down")
#     worker.terminate = True
#     worker.join()
#     print(f"\nintuitiveNMS_worker: {worker_type} worker: successfully shut down")
    # worker.channel.close()
