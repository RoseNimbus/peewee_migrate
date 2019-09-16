import peewee as pw
from tests.test_models.base_model import BaseModel


class CalibrationType(BaseModel):
    name = pw.TextField(primary_key=True)
    description=pw.TextField(null=True)

    class Meta:
        table_name = "calibration_type"


class Calibration(BaseModel):
    calibration_ts = pw.BigIntegerField(primary_key=True)
    type = pw.ForeignKeyField(CalibrationType)
    note=pw.TextField(null=True)
    is_active=pw.BooleanField(default=False)

    class Meta:
        table_name = "calibration"


class CalibrationPoint(BaseModel):
    calibration = pw.ForeignKeyField(Calibration, backref="points")
    point_ts = pw.BigIntegerField(primary_key=True, index=True)
    value_name=pw.TextField(index=True, null=True)
    value_unit=pw.TextField(null=True)
    note=pw.TextField(null=True)

    class Meta:
        table_name = "calibration_point"


class Sensor(BaseModel):
    name = pw.TextField(primary_key=True, index=True)
    unit = pw.TextField()

    class Meta:
        table_name = 'sensor'


class CalibrationMeasurement(BaseModel):
    point = pw.ForeignKeyField(CalibrationPoint, backref="measurements")
    sensor = pw.ForeignKeyField(Sensor)
    count = pw.IntegerField()

    class Meta:
        primary_key = pw.CompositeKey('point', 'sensor')
        table_name = "calibration_measurement"
