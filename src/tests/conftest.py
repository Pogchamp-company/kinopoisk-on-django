import pytest
from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session')
def django_db_setup():
    print('sasasasadsadasd')
    from django.conf import settings

    original_db = settings.DATABASES['default']['NAME']
    test_db = settings.DATABASES['tests']['NAME']

    run_sql(f'DROP {test_db} IF EXISTS {test_db}')
    run_sql(f'CREATE DATABASE {test_db} TEMPLATE {original_db}')

    yield

    for connection in connections.all():
        connection.close()

    run_sql(f'DROP {test_db} IF EXISTS {test_db}')
