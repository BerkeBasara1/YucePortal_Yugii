import pypyodbc
import pyodbc

from db_funcs import QueryToDB
from config import YA_2El_AracSatis


def Write_Log_ToDB(username, request_type, requested_link, Return_code, details=None):
    if not isinstance(YA_2El_AracSatis, str) or not YA_2El_AracSatis.strip():
        return

    if details:
        query = f"INSERT INTO [Yuce_Portal].[dbo].[YP_users_log] (Username, RequestType, RequestLink, RequestedDateTime, ReturnCode, details) VALUES ('{username}', '{request_type}', '{requested_link}', GETDATE(), {Return_code}, '{details}');"
    else:
        query = f"INSERT INTO [Yuce_Portal].[dbo].[YP_users_log] (Username, RequestType, RequestLink, RequestedDateTime, ReturnCode) VALUES ('{username}', '{request_type}', '{requested_link}', GETDATE(), {Return_code});"
    try:
        QueryToDB(YA_2El_AracSatis, query)
    except Exception:
        # Logging should never block the main request flow.
        return
