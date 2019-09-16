import peewee as pw
from ..test_remove import db


class BaseModel(pw.Model):
    class Meta:
        database = db

    @classmethod
    def get_database(cls):
        return cls._meta.database

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name
