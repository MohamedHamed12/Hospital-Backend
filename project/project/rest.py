from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
cursor = connection.cursor()
database_name = 'test_<FAILING_DB_NAME>'
cursor.execute(
    "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity "
    "WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();", [database_name])