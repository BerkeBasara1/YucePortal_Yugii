import pymysql
from pymysql.cursors import DictCursor


Error = pymysql.MySQLError
InterfaceError = pymysql.InterfaceError
OperationalError = pymysql.OperationalError
ProgrammingError = pymysql.ProgrammingError


class _ConnectionWrapper:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self, dictionary=False, buffered=False, prepared=False, *args, **kwargs):
        cursor_cls = DictCursor if dictionary else None
        return self._connection.cursor(cursor=cursor_cls)

    def is_connected(self):
        try:
            self._connection.ping(reconnect=False)
            return True
        except Exception:
            return False

    def reconnect(self, attempts=1, delay=0):
        self._connection.ping(reconnect=True)

    def ping(self, reconnect=False, attempts=1, delay=0):
        self._connection.ping(reconnect=reconnect)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def __getattr__(self, item):
        return getattr(self._connection, item)


def connect(*args, **kwargs):
    params = dict(kwargs)
    if "database" not in params and "db" in params:
        params["database"] = params.pop("db")

    params.pop("dictionary", None)
    params.pop("buffered", None)
    params.pop("prepared", None)
    params.setdefault("charset", "utf8mb4")

    connection = pymysql.connect(*args, **params)
    return _ConnectionWrapper(connection)
