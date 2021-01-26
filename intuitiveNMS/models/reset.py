from intuitiveNMS import db

from intuitiveNMS.models.Device import Device
from intuitiveNMS.models.DeviceStatus import DeviceStatus
from intuitiveNMS.models.DeviceFacts import DeviceFacts
from intuitiveNMS.models.Compliance import Compliance
from intuitiveNMS.models.Host import Host
from intuitiveNMS.models.HostStatus import HostStatus
from intuitiveNMS.models.Service import Service
from intuitiveNMS.models.ServiceStatus import ServiceStatus
from intuitiveNMS.models.Event import Event
from intuitiveNMS.models.Capture import Capture
from intuitiveNMS.models.apis import import_devices, import_services, import_compliance


def reset_devices():
    db.session.query(Device).delete()
    db.session.query(DeviceFacts).delete()
    db.session.query(DeviceStatus).delete()
    db.session.query(Compliance).delete()
    db.session.commit()

    import_devices(filename="devices.yaml", filetype="yaml")
    import_compliance(filename="compliance.yaml")
    return


def reset_hosts():
    db.session.query(HostStatus).delete()
    db.session.query(Host).delete()
    db.session.commit()

    return


def reset_services():
    db.session.query(ServiceStatus).delete()
    db.session.query(Service).delete()
    db.session.commit()
    import_services(filename="services.yaml")
    db.session.commit()

    return


def reset_events():
    db.session.query(Event).delete()
    db.session.commit()

    return


def reset_capture():
    db.session.query(Capture).delete()
    db.session.commit()

    return
