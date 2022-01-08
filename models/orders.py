from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.TIMESTAMP, default=datetime.now())
    status = db.Column(db.String(120), default="draft")
    created_date = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_date = db.Column(db.TIMESTAMP, default=datetime.now())


class OrderDetail(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    created_date = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_date = db.Column(db.TIMESTAMP, default=datetime.now())
