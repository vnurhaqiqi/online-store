from app import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    order_date = db.Column(db.TIMESTAMP)
    status = db.Column(db.String(120), nullable=False)
    payment_date = db.Column(db.TIMESTAMP)
    amount = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.TIMESTAMP)
    updated_date = db.Column(db.TIMESTAMP)

    def confirm_order(self):
        self.status = "payment_confirmed"
