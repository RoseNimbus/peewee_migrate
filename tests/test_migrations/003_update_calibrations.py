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
from tests.test_models.base_model import BaseModel

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    migrator.add_fields('calibration_type', description=pw.TextField(null=True))

    migrator.add_fields(
        'calibration',
        note=pw.TextField(null=True),
        is_active=pw.BooleanField(default=False)
    )

    migrator.add_fields(
        'calibration_point',
        value_name=pw.TextField(index=True, null=True),
        value_unit=pw.TextField(null=True),
        note=pw.TextField(null=True)
    )

    sensor_table = migrator.orm['sensor']
    calibration_point = migrator.orm['calibration_point']

    calibration_measurement = migrator.orm['calibration_measurement']
    table_data = calibration_measurement.select().dicts()[:]
    for measurement in table_data:
        sensor_name = measurement.pop('sensor_name')
        measurement.update({'sensor': sensor_name})

    # migrator.drop_index(calibration_measurement, ('point', 'sensor_name',))
    # migrator.change_columns(calibration_measurement, sensor_name=pw.ForeignKeyField(sensor_table))
    # migrator.change_columns(calibration_measurement, sensor_name=pw.TextField(primary_key=False))
    # migrator.rename_field(calibration_measurement, 'sensor_name', 'sensor')

    # migrator.rename_field(calibration_measurement, 'sensor_name', 'sensor')
    # migrator.remove_fields('calibration_measurement', 'sensor_name')
    # migrator.remove_model('calibration_measurement', cascade=True)
    migrator.remove_model('calibration_measurement')

    @migrator.create_model
    class CalibrationMeasurement(pw.Model):
        point = pw.ForeignKeyField(calibration_point)
        sensor = pw.ForeignKeyField(sensor_table)
        count = pw.IntegerField()

        class Meta:
            primary_key = pw.CompositeKey('point', 'sensor')
            table_name = 'calibration_measurement'

    migrator.python(test_action, database, migrator, table_data)


def test_action(db, migrator, table_data):
    calibration_measurement = migrator.orm['calibration_measurement']
    with db.atomic():
        calibration_measurement.insert_many(table_data).execute()
