"""Peewee migrations -- 006_update_calibrations_add_sensors.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""
import peewee as pw

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Sensor(pw.Model):
        name = pw.TextField(primary_key=True, index=True)
        unit = pw.TextField()

        class Meta:
            table_name = 'sensor'

    migrator.python(insert_sensors, database, migrator)


def insert_sensors(db, migrator):
    sensor = migrator.orm['sensor']
    data_to_insert = [
        {'name': 'dv',        'unit': 'volt'},
        {'name': 'temp1',     'unit': 'celsius'},
        {'name': 'temp2',     'unit': 'celsius'},
        {'name': 'pressure',  'unit': 'volt'},
        {'name': 'flow',      'unit': 'volt'},
        {'name': 'sg',        'unit': 'dimensionless'},
        {'name': 'tared_sg',  'unit': 'dimensionless'},
        {'name': 'dv_in_si',  'unit': 'meter'},
        {'name': 'dv_shift',  'unit': 'meter'}
    ]
    with db.atomic():
        sensor.insert_many(data_to_insert).execute()
