"""Peewee migrations -- 001_calibration.py.

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
    class CalibrationType(pw.Model):
        name = pw.TextField(primary_key=True)

        class Meta:
            table_name = "calibration_type"

    migrator.python(set_default_calibration_types, database, migrator)

    @migrator.create_model
    class Calibration(pw.Model):
        calibration_ts = pw.BigIntegerField(primary_key=True)
        type = pw.ForeignKeyField(CalibrationType)

        class Meta:
            table_name = "calibration"

    migrator.python(set_default_calibration, database, migrator)

    @migrator.create_model
    class CalibrationPoint(pw.Model):
        calibration = pw.ForeignKeyField(Calibration, backref="points")
        point_ts = pw.BigIntegerField(primary_key=True, index=True)

        class Meta:
            table_name = "calibration_point"
    migrator.python(set_calibration_point, database, migrator)

    @migrator.create_model
    class CalibrationMeasurement(pw.Model):
        point = pw.ForeignKeyField(CalibrationPoint, backref="measurements")
        sensor_name = pw.TextField(index=True)
        count = pw.IntegerField()

        class Meta:
            primary_key = pw.CompositeKey('point', 'sensor_name')
            table_name = "calibration_measurement"
    migrator.python(set_calibration_measurement, database, migrator)


def set_default_calibration_types(database, migrator):
    calibration_type = migrator.orm['calibration_type']
    data_to_save = [
        {
            'name': 'zeroing'
        },
        {
            'name': 'value_linear'
        },
        {
            'name': 'laser_zeroing'
        },
    ]
    with database.atomic():
        calibration_type.insert_many(data_to_save).execute()


def set_default_calibration(database, migrator):
    calibration = migrator.orm['calibration']
    data_to_save = [
        {
            'calibration_ts': 1,
            'type': 'value_linear'
        },
        {
            'calibration_ts': 2,
            'type': 'value_linear'
        },
        {
            'calibration_ts': 3,
            'type': 'value_linear'
        }
    ]
    with database.atomic():
        calibration.insert_many(data_to_save).execute()


def set_calibration_point(database, migrator):
    calibration_point = migrator.orm['calibration_point']
    data_to_save = [
        {
            'calibration': 1,
            'point_ts': 10001
        },
        {
            'calibration': 2,
            'point_ts': 20002
        },
        {
            'calibration': 3,
            'point_ts': 30003
        }
    ]
    with database.atomic():
        calibration_point.insert_many(data_to_save).execute()


def set_calibration_measurement(database, migrator):
    calibration_measurement = migrator.orm['calibration_measurement']
    data_to_save = [
        {
            'point': 10001,
            'sensor_name': 'dv',
            'count': 10
        },
        {
            'point': 20002,
            'sensor_name': 'dv',
            'count': 20
        },
        {
            'point': 30003,
            'sensor_name': 'psi',
            'count': 30
        }
    ]
    with database.atomic():
        calibration_measurement.insert_many(data_to_save).execute()
