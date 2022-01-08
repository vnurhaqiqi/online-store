from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.TIMESTAMP, default=datetime.now())
    status = db.Column(db.String(120), default="draft")
    created_date = db.Column(db.TIMESTAMP)
    updated_date = db.Column(db.TIMESTAMP)

    def total_amount(self):
        # function to get all total amount from details
        order_details = OrderDetail.query.filter_by(order_id=self.id).all()
        total_amount = 0.0

        for detail in order_details:
            amount = detail.quantity * detail.price
            total_amount += amount

        return total_amount


class OrderDetail(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    created_date = db.Column(db.TIMESTAMP)
    updated_date = db.Column(db.TIMESTAMP)
