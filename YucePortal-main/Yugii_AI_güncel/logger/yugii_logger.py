from functools import wraps


class YugiiLogger:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def log_db_query(self, sql, params=None):
        return None

    def write_plain(self, text):
        return None


def log_process_message(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
