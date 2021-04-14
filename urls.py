from flask import Blueprint, jsonify, request
from sqlalchemy import text

from utils import change_dec, info_dec

urls = Blueprint('urls', __name__)


@urls.route('/')
def index():
    main_page_text = "<h1>Urls:</h1>" \
                     "<ul>" \
                     "<li><h3>GET: /api/rooms</h3></li>" \
                     "<li><h3>GET: /api/rooms/pk</h3></li>" \
                     "<li><h3>GET: /api/customers</h3></li>" \
                     "<li><h3>GET: /api/customers/pk</h3></li>" \
                     "<li><h3>GET: /api/racks</h3></li>" \
                     "<li><h3>GET: /api/racks/pk</h3></li>" \
                     "<li><h3>GET: /api/busy_racks</h3></li>" \
                     "<li><h3>GET: /api/racks_with_max_size</h3></li>" \
                     "<li><h3>GET: /api/customers_in_rooms</h3></li>" \
                     "<li><h3>POST: /api/sum</h3></li>"\
                     "<li><h3>POST: /api/dif</h3></li>" \
                     "<li><h3>POST: /api/prod</h3></li>" \
                     "<li><h3>POST: /api/div</h3></li>" \
                     "</ul>"
    return main_page_text


@urls.route('/api/rooms')
def get_rooms():
    """ Получаем json всех комнат """
    from models import Room
    rooms = Room.query.all()
    return jsonify({'rooms': [room.to_json() for room in rooms]})


@urls.route('/api/rooms/<int:id>')
def get_room(id):
    from models import Room
    room = Room.query.get_or_404(id)
    return jsonify(room.to_json())


@urls.route('/api/racks')
def get_racks():
    """ Получаем json всех стоек """
    from models import Rack
    racks = Rack.query.all()
    return jsonify({'racks': [rack.to_json() for rack in racks]})


@urls.route('/api/racks/<int:id>')
def get_rack(id):
    from models import Rack
    rack = Rack.query.get_or_404(id)
    return jsonify(rack.to_json())


@urls.route('/api/customers')
def get_customers():
    """ Получаем json всех клиентов """
    from models import Customer
    customers = Customer.query.all()
    return jsonify({'customers': [customer.to_json() for customer in customers]})


@urls.route('/api/customers/<int:id>')
def get_customer(id):
    from models import Customer
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_json())


@urls.route('/api/busy_racks')
def get_busy_racks():
    """ Получаем список занятых (status == ‘occupied’) стоек с именем комнаты,
        в которой каждая стойка находится, и именем клиента,
        которому она принадлежит """
    from app import db
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


@urls.route('/api/customers_in_rooms')
def get_customers_in_rooms():
    """ Получаем список всех комнат
        с прикреплённым к каждой массивом из ID тех клиентов,
        у которых есть занятые (status == ‘occupied’) стойки в этой комнате. """
    from app import db
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


@urls.route('/api/racks_with_max_size')
def get_racks_with_max_size():
    """ Получаем список всех комнат
        и для каждой определить стойку внутри неё,
        у которой поле size имеет наибольшее значение """
    from app import db
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


@urls.route('/api/sum', methods=['POST'])
def get_sum():
    """ Получаем сумму пераданных аргументов, в зависимости от порядка и множителя """
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_sum(*args: list, reverse: bool = False) -> int:
        """
        Вычисляется сумма переданных аргументов
        :param args: список аргументов
        :param reverse: флаг, для определения порядка вычисления
        :return: полученная сумма
        """
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


@urls.route('/api/dif', methods=['POST'])
def get_dif():
    """ Получаем разность пераданных аргументов, в зависимости от порядка и множителя """
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_dif(*args: list, reverse: bool = False) -> int:
        """
        Вычисляется разность переданных аргументов
        :param args: список аргументов
        :param reverse: флаг, для определения порядка вычисления
        :return: полученная сумма
        """
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


@urls.route('/api/prod', methods=['POST'])
def get_prod():
    """ Получаем произведение пераданных аргументов, в зависимости от порядка и множителя """
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_prod(*args: list, reverse: bool = False) -> int:
        """
        Вычисляется произведение переданных аргументов
        :param args: список аргументов
        :param reverse: флаг, для определения порядка вычисления
        :return: полученная сумма
        """
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


@urls.route('/api/div', methods=['POST'])
def get_div():
    """ Получаем частное пераданных аргументов, в зависимости от порядка и множителя """
    content = request.json
    last_arg_multiplier = content['last_arg_multiplier']

    @change_dec(last_arg_change=last_arg_multiplier)
    @info_dec
    def my_div(*args: list, reverse: bool = False) -> int:
        """
        Вычисляется деление переданных аргументов
        :param args: список аргументов
        :param reverse: флаг, для определения порядка вычисления
        :return: полученная сумма
        """
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
