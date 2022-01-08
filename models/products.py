from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)
    most_lead_time = db.Column(db.Integer)
    lead_time = db.Column(db.Integer)

    def check_available_quantity(self):
        status_dict = {}
        if self.quantity <= 0:
            status_dict["status"] = "not_available"
            status_dict["available_quantity"] = self.quantity

            return status_dict

        status_dict["status"] = "available"
        status_dict["available_quantity"] = self.quantity

        return status_dict

    def check_ordered_quantity(self, ordered_quantity):
        if ordered_quantity > self.quantity:
            return True
