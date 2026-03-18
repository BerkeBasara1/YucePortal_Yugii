from datetime import datetime, timedelta, date
from db_funcs import *
from config import YuceDB


def return_banko_fromGivenDates(start_date, end_date):
    banko_query_mssql1 = f"""
    SELECT SUM([Parça Banko Satış Net Tutar]) AS Total_Sales
    FROM [YuceDashboard].[dbo].[ParcaVeIscilikSatisi009]
    WHERE [İş Emri Kabul Tarihi Saatsiz] BETWEEN '{start_date} 00:00:00.000' AND '{end_date} 23:59:59.999'
    """
    print(banko_query_mssql1)
    result = AssignDBContenttoListWithQuery(YuceDB,banko_query_mssql1)[0]

    return result 