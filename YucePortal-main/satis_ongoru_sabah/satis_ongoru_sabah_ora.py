import oracledb
from config import dsn


def return_fatura_adetleri_fromOraDB(start_date, end_date):
    connection = oracledb.connect(dsn)
    query = f"""
        SELECT
        TOPMODEL_DEFINITION,
        ACTIVITY_DATE,
        SUM(CASE WHEN EXTRACT(YEAR FROM ACTIVITY_DATE) = EXTRACT(YEAR FROM SYSDATE) THEN COUNT_CHASSIS ELSE 0 END) THIS_YEAR_COUNT_CHASSIS
        FROM (
        SELECT DISTINCT
            VSYS.FIRM_CODE,
            VSYS.ACTIVITY_DATE,
            CASE WHEN VEH_VEHICLE.RESERVER_CODE <> 'Özel Satışlar' THEN 'Perakende' ELSE VEH_VEHICLE.RESERVER_CODE END RESERVER_CODE,
            CASE WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Octavia Combi' THEN 'Octavia' 
                WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Yeni Superb' THEN 'Superb' 
                WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Superb Combi' THEN 'Superb' 
                WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Fabia Combi' THEN 'Fabia' 
                ELSE MODEL_CATALOG.TOPMODEL_DEFINITION 
            END TOPMODEL_DEFINITION,
            COUNT(DISTINCT VSYS.CHASSIS) COUNT_CHASSIS
        FROM YUCE_DM.TBL_DW_VEH_RPT_VEHICLE_SALES_YS VSYS
        INNER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE VEH_VEHICLE ON (VSYS.VEHICLE_ID = VEH_VEHICLE.VEHICLE_ID)
        LEFT JOIN YUCE_DM.TBL_DW_VEH_MODEL_CATALOG MODEL_CATALOG ON (MODEL_CATALOG.COUNTRYMODEL_ID = VEH_VEHICLE.FK_COUNTRYMODEL_ID)
        WHERE VSYS.ACTIVITY_DATE BETWEEN TO_DATE('{start_date}', 'DD.MM.YYYY') AND TO_DATE('{end_date}', 'DD.MM.YYYY')
        GROUP BY
            VSYS.FIRM_CODE,
            VSYS.ACTIVITY_DATE,
            CASE WHEN VEH_VEHICLE.RESERVER_CODE <> 'Özel Satışlar' THEN 'Perakende' ELSE VEH_VEHICLE.RESERVER_CODE END,
            CASE WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Octavia Combi' THEN 'Octavia' 
                WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Yeni Superb' THEN 'Superb' 
                WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Superb Combi' THEN 'Superb' 
                WHEN MODEL_CATALOG.TOPMODEL_DEFINITION = 'Fabia Combi' THEN 'Fabia' 
                ELSE MODEL_CATALOG.TOPMODEL_DEFINITION 
            END
        )
        GROUP BY
        TOPMODEL_DEFINITION,
        ACTIVITY_DATE
    """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    models_list = []
    for result in results:
        if result[0] not in models_list:
            models_list.append(result[0])
    
    models_dict = {}
    for model in models_list:
        models_dict[model] = 0
        
    for result in results:
        if result[0] in models_dict:
            models_dict[result[0]] += result[2]
    
    return models_dict

def return_baglanti_adetleri_fromOraDB(start_date, end_date):
    connection = oracledb.connect(dsn)
    query = f"""
        SELECT
            MAX(tdvrvscm.BRAND_DEFINITION) AS BRAND_DEFINITION,
            SUM(tdvrvscm.CONFIRMED_INVOICES) AS TOTAL_CONFIRMED_INVOICES,
            SUM(tdvrvscm.PENDING_INVOICES) AS TOTAL_PENDING_INVOICES,
            SUM(tdvrvscm.EXPECTED_INVOICES) AS TOTAL_EXPECTED_INVOICES,
            SUM(tdvrvscm.SUM) AS TOTAL_SUM,
            tdvrvscm.ENTRY_DATE
        FROM YUCE_DM.TBL_DW_VEH_RPT_VEHICLE_SALES_CONNECTION_MANAGEMENT tdvrvscm
        WHERE tdvrvscm.ENTRY_DATE >= TO_DATE('{start_date}', 'DD.MM.YYYY') AND tdvrvscm.ENTRY_DATE <= TO_DATE('{end_date}', 'DD.MM.YYYY')
        GROUP BY tdvrvscm.BRAND_DEFINITION,
                tdvrvscm.ENTRY_DATE

    """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    models_list = []
    for result in results:
        if result[0] not in models_list:
            models_list.append(result[0])
    
    models_dict = {}
    for model in models_list:
        models_dict[model] = 0
        
    for result in results:
        if result[0] in models_dict:
            models_dict[result[0]] += result[4]
    
    return models_dict