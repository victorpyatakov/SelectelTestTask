from app import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    def to_json(self):
        json_room = {
            'id': self.id,
            'name': self.name
        }
        return json_room

    def __repr__(self):
        return f"<room {self.id}>"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    def to_json(self):
        json_customer = {
            'id': self.id,
            'name': self.name
        }
        return json_customer

    def __repr__(self):
        return f"<customer {self.id}>"


class Rack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    size = db.Column(db.Integer)
    state = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def to_json(self):
        json_room = {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'state': self.state,
            'customer_id': self.customer_id,
            'room_id': self.room_id
        }
        return json_room

    def __repr__(self):
        return f"<customer {self.id}>"
