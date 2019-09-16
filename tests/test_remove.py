from playhouse.sqlite_ext import SqliteExtDatabase
import logging
from peewee_migrate.router import Router, load_models
from peewee_migrate.auto import diff_many
import tests.test_models


# Init database
db = SqliteExtDatabase(
    '/tmp/test_db',
    pragmas=(
        ('cache_size', -1024 * 64),  # 64MB page-cache
        ('journal_mode', 'wal'),     # Use WAL-mode
    )
)


def run_db_migration(database):
    router = Router(
        database,
        migrate_dir='tests/test_migrations',
        migrate_table='migration',
        ignore=['basemodel']
    )
    print('Run migrations..')

    router.run()

    # check migrations
    src_models = load_models(tests.test_models)
    if router.ignore:
        src_models = [m for m in src_models if m.get_table_name() not in router.ignore]
    # print('run_db_migration: src_models={}'.format(src_models))
    # src_calibration_measurement_model = [m for m in src_models if m._meta.table_name == 'calibration_measurement'][0]
    # print('run_db_migration: src_CalibrationMeasurement.fields={}'.format(src_calibration_measurement_model._meta.fields))

    db_models = router.migrator.orm.values()
    # print('run_db_migration: db_models={}'.format(db_models))
    # db_calibration_measurement_model = router.migrator.orm['calibration_measurement']
    # print('run_db_migration:  db_CalibrationMeasurement.fields={}'.format(db_calibration_measurement_model._meta.fields))

    diff_found = diff_many(src_models, db_models, router.migrator, reverse=False)

    if len(diff_found) > 0:
        # logging.warning('migrations diff_found={}'.format(diff_found))
        print('migrations diff_found={}'.format(diff_found))
        raise RuntimeError('Check db migrations is failed')



if __name__ == '__main__':

    run_db_migration(db)

