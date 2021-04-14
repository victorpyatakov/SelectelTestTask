from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from models import Room, Customer, Rack

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def db_create():
    """ Создаем таблицы и заполняем данными"""
    db.create_all()

    # insert rooms
    room1 = Room(name="Room1")
    room2 = Room(name="Room2")
    room3 = Room(name="Room3")
    room4 = Room(name="Room4")
    db.session.add(room1)
    db.session.add(room2)
    db.session.add(room3)
    db.session.add(room4)
    db.session.commit()

    # insert customers
    customer1 = Customer(name="Client-1")
    customer2 = Customer(name="Client-2")
    customer3 = Customer(name="Client-3")
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.commit()

    # insert racks
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

    # commit the changes
    db.session.commit()


if __name__ == '__main__':
    manager.run()