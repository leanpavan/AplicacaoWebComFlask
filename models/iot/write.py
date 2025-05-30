from models.db import db
from models.iot.devices import Device
from models.iot.actuators import Actuator
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuators_id = db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable=False)
    value = db.Column(db.String(50), nullable=False)

    def add_write(topic, value):
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        device = Device.query.filter(Device.id == actuator.devices_id).first()

        if (actuator is not None) and (device.is_active == True):
            write = Write(
                write_datetime = datetime.now(),
                actuators_id = actuator.id,
                value = value
            )

            db.session.add(write)
            db.session.commit()

    def get_write(device_id, start, end):
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        write = Write.query.filter(
            Write.actuators_id == actuator.id,
            Write.write_datetime > start,
            Write.write_datetime < end
        ).all()

        return write