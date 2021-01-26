from flask import Flask
from flask_cors import CORS

from intuitiveNMS.controller.utils import log_console


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Get configuration from environment variables
import os

interval = os.environ.get("DEVICE_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    device_monitor_interval = max(10, int(interval))
else:
    device_monitor_interval = 60
interval = os.environ.get("COMPLIANCE_MONITOR_INTERVAL", default="300")
if interval.isnumeric():
    compliance_monitor_interval = max(10, int(interval))
else:
    compliance_monitor_interval = 300
interval = os.environ.get("CONFIGURATION_MONITOR_INTERVAL", default="300")
if interval.isnumeric():
    configuration_monitor_interval = max(10, int(interval))
else:
    configuration_monitor_interval = 300
interval = os.environ.get("HOST_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    host_monitor_interval = max(10, int(interval))
else:
    host_monitor_interval = 60
interval = os.environ.get("SERVICE_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    service_monitor_interval = max(10, int(interval))
else:
    service_monitor_interval = 60
interval = os.environ.get("DISCOVERY_INTERVAL", default="3600")
if interval.isnumeric():
    discovery_interval = max(10, int(interval))
else:
    discovery_interval = 3600
interval = os.environ.get("WORKER_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    worker_monitor_interval = max(10, int(interval))
else:
    worker_monitor_interval = 60

from flask_sqlalchemy import SQLAlchemy

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///intuitive-nms"
db = SQLAlchemy(app)

import intuitiveNMS.views.ui_views
import intuitiveNMS.views.device_views
import intuitiveNMS.views.capture_views
import intuitiveNMS.views.portscan_views
import intuitiveNMS.views.traceroute_views
import intuitiveNMS.views.worker_views

import intuitiveNMS.models
db.create_all()

from intuitiveNMS.models.apis import (
    import_devices,
    import_compliance,
    import_services,
    import_workers,
)
from intuitiveNMS.models.apis import get_all_devices, set_facts
from intuitiveNMS.models.Host import Host

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")
import_services(filename="services.yaml")
import_workers(filename="workers.yaml", filetype="yaml")

# Host.query.delete()

# Reset time-series data tables
from intuitiveNMS.models.DeviceStatus import DeviceStatus
from intuitiveNMS.models.HostStatus import HostStatus
from intuitiveNMS.models.ServiceStatus import ServiceStatus

db.session.commit()

from intuitiveNMS.controller.ThreadManager import ThreadManager
ThreadManager.start_device_threads(
    device_monitor_interval=device_monitor_interval,
    compliance_monitor_interval=compliance_monitor_interval,
    configuration_monitor_interval=configuration_monitor_interval,
)

ThreadManager.start_service_thread(service_monitor_interval)
ThreadManager.start_discovery_thread(discovery_interval)
ThreadManager.start_host_thread(host_monitor_interval)
ThreadManager.start_summaries_thread()
ThreadManager.start_worker_thread(worker_monitor_interval)
ThreadManager.start_db_maintenance_thread()

from intuitiveNMS.controller.CaptureManager import CaptureManager

capture_manager = CaptureManager()
from intuitiveNMS.controller.PortscanManager import PortscanManager

portscan_manager = PortscanManager()
from intuitiveNMS.controller.TracerouteManager import TracerouteManager

traceroute_manager = TracerouteManager()


def shutdown():

    log_console("\n\n\n---> Entering shutdown sequence")

    ThreadManager.initiate_terminate_all_threads()

    ThreadManager.stop_discovery_thread()
    ThreadManager.stop_host_thread()
    ThreadManager.stop_service_thread()
    ThreadManager.stop_summaries_thread()
    ThreadManager.stop_worker_thread()
    ThreadManager.stop_device_threads()
    ThreadManager.stop_db_maintenance_thread()

    log_console("\n---> all threads shut down, terminating.")


import atexit

atexit.register(shutdown)
# import intuitiveNMS.views.ui_views
# from flask_sqlalchemy import SQLAlchemy
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
#
#
# class Device(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, unique=True, nullable=False)
#     ip_address = db.Column(db.Text)
#     vendor = db.Column(db.Text)
#     os = db.Column(db.Text)
#     hostname = db.Column(db.Text)
#
#
# db.create_all()
#
# from intuitiveNMS.controller.utils import import_devices
#
# for device in import_devices():
#     device_obj = Device(**device)
#     db.session.add(device_obj)
#
# db.session.commit()
