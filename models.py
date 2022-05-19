from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Device(Base):
    __tablename__ = 'devices'
    dev_id = Column(String, primary_key=True, index=True, autoincrement=False)
    dev_type = Column(String)

    endpoints = relationship('Endpoint', backref='device', lazy='joined', passive_deletes=True)


class Endpoint(Base):
    __tablename__ = 'endpoints'

    endpoint_id = Column(Integer, index=True, primary_key=True)
    endpoint = Column(String)
    device_id = Column(String, ForeignKey('devices.dev_id', ondelete='CASCADE'))
