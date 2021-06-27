"""Data models."""
# from . import db
from uuid import uuid4
import datetime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config.from_object("config.Config")

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

def generateUUID():
    return str(uuid4())


class Customer(db.Model):
    """Data model for user accounts."""

    __tablename__ = "customers"
    id = db.Column(db.String(80), primary_key=True, default=generateUUID)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Service(db.Model):
    """ Data models for the services being rendered"""

    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=False, unique=True, nullable=False)
    duration = db.Column(db.Integer, index=False, nullable=False)


class WorkOrder(db.Model):
    """A work order for a time period"""

    __tablename__ = "work_orders"
    id = db.Column(db.String(80), primary_key=True, default=generateUUID)
    name = db.Column(db.String(80), nullable=True)
    customer_id = db.Column(db.String(80), db.ForeignKey('customers.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    customer = relationship("Customer", back_populates="work_orders")
    service = relationship("Service", back_populates="work_orders")
    start_time = db.Column(db.DateTime, index=False, nullable=False)
    end_time = db.Column(db.DateTime, index=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # created = db.Column(db.DateTime, index=False, unique=False, nullable=False)



Customer.work_orders = relationship("WorkOrder", order_by = WorkOrder.id, back_populates = "customer")
Service.work_orders = relationship("WorkOrder", order_by = WorkOrder.id, back_populates = "service")


class CustomerSchema(ma.Schema):
    class Meta:
       fields = ('id', 'username', 'email', 'created')
    
    # id = ma.auto_field()
    # username = ma.auto_field()
    # email = ma.auto_field()
    # created = ma.auto_field()



class ServiceSchema(ma.Schema):
    class Meta:
       fields = ('id', 'name', 'duration')
    

# class WorkOrderSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = WorkOrder
    
#     id = ma.auto_field()
#     name = ma.auto_field()
#     start_time = ma.auto_field()
#     end_time = ma.auto_field()
#     created_at = ma.auto_field()
