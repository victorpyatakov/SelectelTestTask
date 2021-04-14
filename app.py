from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from functools import wraps

app = Flask(__name__)

# database = 'database'
database = '0.0.0.0'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://testdbuser:testdbpass@{database}:5432/testdb'
db = SQLAlchemy(app)


######## deco

def info_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} was called.")
        return func(*args, **kwargs)

    return wrapper


def change_dec(last_arg_change=1):
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            *el, last = args
            last *= last_arg_change
            args = *el, last
            return func(*args, **kwargs)

        return wrapper

    return dec


@app.route('/api/sum', methods=['POST'])
def get_sum():
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_sum(*args, reverse=False):
        if reverse:
            args = args[::-1]
        res = args[0]
        for el in args[1:]:
            res += el
        return res

    is_reversed = eval(content['reverse'])
    args = content['args']
    result = my_sum(*args, reverse=is_reversed)
    response = {
        'result': result
    }
    return jsonify(response)

@app.route('/api/dif', methods=['POST'])
def get_dif():
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_dif(*args, reverse=False):
        if reverse:
            args = args[::-1]
        res = args[0]
        for el in args[1:]:
            res -= el
        return res

    is_reversed = eval(content['reverse'])
    args = content['args']
    result = my_dif(*args, reverse=is_reversed)
    response = {
        'result': result
    }
    return jsonify(response)

@app.route('/api/prod', methods=['POST'])
def get_prod():
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_prod(*args, reverse=False):
        if reverse:
            args = args[::-1]
        res = args[0]
        for el in args[1:]:
            res *= el
        return res

    is_reversed = eval(content['reverse'])
    args = content['args']
    result = my_prod(*args, reverse=is_reversed)
    response = {
        'result': result
    }
    return jsonify(response)

@app.route('/api/div', methods=['POST'])
def get_div():
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_div(*args, reverse=False):
        if reverse:
            args = args[::-1]
        res = args[0]
        try:
            for el in args[1:]:
                res /= el
            return res
        except ZeroDivisionError as error:
            return f"Error: {error}"

    is_reversed = eval(content['reverse'])
    args = content['args']
    result = my_div(*args, reverse=is_reversed)
    response = {
        'result': result
    }
    return jsonify(response)
########

@app.route('/api/busy_racks')
def get_busy_racks():
    sql_racks = text(
        "select rk.id,rk.name, rm.name, ctr.name "
        "from public.rack rk join public.room rm on rm.id = rk.room_id "
        "join public.customer ctr on ctr.id = rk.customer_id "
        "where state like 'occupied'"
    )
    result = db.engine.execute(sql_racks).fetchall()
    json = {}
    for i in range(len(result)):
        json[i] = {
            'rack_id': result[i][0],
            'rack_name': result[i][1],
            'room_name': result[i][2],
            'customer_name': result[i][3],
        }
    return jsonify(json)


@app.route('/api/customers_in_rooms')
def get_customers_in_rooms():
    sql_rooms = text(
        "select distinct rm.id, rm.name  "
        "from public.rack "
        "join public.room  rm on rack.room_id = rm.id "
        "where state like 'occupied'"
    )
    rooms = db.engine.execute(sql_rooms).fetchall()
    json = {}
    for i in range(len(rooms)):
        sql_rooms_customer = text(
            "select distinct customer_id  "
            "from public.rack "
            f"where room_id = {rooms[i][0]} and state like '%occupied%' "
        )
        rooms_customers = db.engine.execute(sql_rooms_customer).fetchall()
        json[i] = {
            'room_id': rooms[i][0],
            'room_name': rooms[i][1],
            'customers_id': [c[0] for c in rooms_customers]
        }
    return jsonify(json)


@app.route('/api/racks_with_max_size')
def get_racks_with_max_size():
    sql_rooms_with_max_size_racks = text(
        "select room_id, max(size) "
        "from public.rack  "
        "group by room_id"
    )
    rooms_with_max_size_racks = db.engine.execute(sql_rooms_with_max_size_racks).fetchall()
    json = {}
    for i in range(len(rooms_with_max_size_racks)):
        sql_id_racks_with_max_size = text(
            "select id  "
            "from public.rack "
            f"where room_id={rooms_with_max_size_racks[i][0]} and size={rooms_with_max_size_racks[i][1]} "
            "limit 1"
        )
        id_racks_with_max_size = db.engine.execute(sql_id_racks_with_max_size).fetchone()
        json[i] = {
            'room_id': rooms_with_max_size_racks[i][0],
            'rack_id': id_racks_with_max_size[0],
            'rack_size': rooms_with_max_size_racks[i][1]
        }
    return jsonify(json)


@app.route('/')
def index():
    main_page_text = "<h1>Urls:</h1>" \
                     "<ul>" \
                     "<li><h3>/api/rooms</h3></li>" \
                     "<li><h3>/api/rooms/pk</h3></li>" \
                     "<li><h3>/api/customers</h3></li>" \
                     "<li><h3>/api/customers/pk</h3></li>" \
                     "<li><h3>/api/racks</h3></li>" \
                     "<li><h3>/api/racks/pk</h3></li>" \
                     "<li><h3>/api/busy_racks</h3></li>" \
                     "<li><h3>/api/racks_with_max_size</h3></li>" \
                     "<li><h3>/api/customers_in_rooms</h3></li>" \
                     "</ul>"
    return main_page_text


@app.route('/api/rooms')
def get_rooms():
    rooms = Room.query.all()
    return jsonify({'rooms': [room.to_json() for room in rooms]})


@app.route('/api/rooms/<int:id>')
def get_room(id):
    room = Room.query.get_or_404(id)
    return jsonify(room.to_json())


@app.route('/api/customers')
def get_customers():
    customers = Customer.query.all()
    return jsonify({'customers': [customer.to_json() for customer in customers]})


@app.route('/api/customers/<int:id>')
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_json())


@app.route('/api/racks')
def get_racks():
    racks = Rack.query.all()
    return jsonify({'racks': [rack.to_json() for rack in racks]})


@app.route('/api/racks/<int:id>')
def get_rack(id):
    rack = Rack.query.get_or_404(id)
    return jsonify(rack.to_json())


@app.route('/api/data_add/')
def data_add():
    try:
        db.create_all()
        room1 = Room(name="Room1")
        room2 = Room(name="Room2")
        room3 = Room(name="Room3")
        room4 = Room(name="Room4")
        db.session.add(room1)
        db.session.add(room2)
        db.session.add(room3)
        db.session.add(room4)
        db.session.commit()
        customer1 = Customer(name="Client-1")
        customer2 = Customer(name="Client-2")
        customer3 = Customer(name="Client-3")
        db.session.add(customer1)
        db.session.add(customer2)
        db.session.add(customer3)
        db.session.commit()
        rack1 = Rack(name='Rack1',
                     size='42',
                     state='occupied',
                     customer_id=customer1.id,
                     room_id=room1.id
                     )
        rack2 = Rack(name='Rack2',
                     size='42',
                     state='occupied',
                     customer_id=customer2.id,
                     room_id=room1.id
                     )
        rack3 = Rack(name='Rack3',
                     size='21',
                     state='free',
                     customer_id=customer3.id,
                     room_id=room1.id
                     )
        rack4 = Rack(name='Rack4',
                     size='42',
                     state='occupied',
                     customer_id=customer1.id,
                     room_id=room2.id
                     )
        rack5 = Rack(name='Rack5',
                     size='42',
                     state='free',
                     customer_id=customer1.id,
                     room_id=room2.id
                     )
        rack6 = Rack(name='Rack6',
                     size='47',
                     state='free',
                     customer_id=customer2.id,
                     room_id=room3.id
                     )
        rack7 = Rack(name='Rack7',
                     size='42',
                     state='occupied',
                     customer_id=customer1.id,
                     room_id=room3.id
                     )
        rack8 = Rack(name='Rack8',
                     size='21',
                     state='occupied',
                     customer_id=customer1.id,
                     room_id=room3.id
                     )
        db.session.add(rack1)
        db.session.add(rack2)
        db.session.add(rack3)
        db.session.add(rack4)
        db.session.add(rack5)
        db.session.add(rack6)
        db.session.add(rack7)
        db.session.add(rack8)
        db.session.commit()
        return "<h1>succecful!</h1>"
    except Exception as e:
        return f"{e}"


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
