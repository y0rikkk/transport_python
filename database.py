from peewee import *
import datetime

db = SqliteDatabase("transport.db")


class Transport(Model):
    id = AutoField(primary_key=True)
    type = CharField()
    capacity = FloatField()
    length = FloatField()
    width = FloatField()
    height = FloatField()
    date_of_reservation = CharField()

    class Meta:
        database = db


db.create_tables([Transport])
# try:
#     Transport.create(id=1, type="Газель", capacity=2, length=3, width=2, height=2.2, date_of_reservation="Нет")
# except IntegrityError:
#     pass
# try:
#     Transport.create(id=2, type="Бычок", capacity=3, length=5, width=2.2, height=2, date_of_reservation="Нет")
# except IntegrityError:
#     pass
# try:
#     Transport.create(id=3, type="MAN-10", capacity=10, length=8, width=2.45, height=2.7, date_of_reservation="Нет")
# except IntegrityError:
#     pass
# try:
#     Transport.create(id=4, type="Фура", capacity=20, length=13.6, width=2.46, height=2.6, date_of_reservation="Нет")
# except IntegrityError:
#     pass


def get_all_transport():
    result = []
    for transport in Transport.select():
        result.append(
            [transport.id, transport.type, transport.capacity, transport.length,
             transport.width, transport.height,
             transport.date_of_reservation])
    return result


def create_new(type, capacity, length, width, height):
    Transport.create(type=type, capacity=capacity, length=length, width=width,
                     height=height, date_of_reservation="Нет")


def transport_exists(id):
    try:
        Transport.get(Transport.id == id)
        return True
    except Transport.DoesNotExist:
        return False


def destroy_transport(id):
    Transport.get(Transport.id == id).delete_instance()


def add_reservation(id):
    t = Transport.get(Transport.id == id)
    t.date_of_reservation = datetime.datetime.now().strftime("%d.%m.%Y\n%H:%M:%S")
    t.save()


def cancel_reservation(id):
    t = Transport.get(Transport.id == id)
    t.date_of_reservation = "Нет"
    t.save()


def is_reserved(id):
    t = Transport.get(Transport.id == id)
    if t.date_of_reservation == "Нет":
        return False
    else:
        return True
