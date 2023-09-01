# Models go here
import peewee

db = peewee.SqliteDatabase("database.db")


class Product(peewee.Model):
    name = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    price_per_unit_cents = peewee.IntegerField()
    quantity = peewee.IntegerField()

    class Meta:
        database = db


class User(peewee.Model):
    name = peewee.CharField()
    address = peewee.CharField()
    billing_info = peewee.CharField()
    products = peewee.ManyToManyField(Product)

    class Meta:
        database = db


class Tag(peewee.Model):
    name = peewee.CharField()
    products = peewee.ManyToManyField(Product)

    class Meta:
        database = db


class Transaction(peewee.Model):
    purchased_by_user = peewee.ForeignKeyField(User)
    purchased_product = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField()

    class Meta:
        database = db


UserProducts = User.products.get_through_model()
TagProducts = Tag.products.get_through_model()
