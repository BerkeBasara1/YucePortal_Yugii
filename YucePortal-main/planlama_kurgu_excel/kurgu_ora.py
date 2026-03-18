import oracledb
from config import dsn


#Returns "TOPTAN"
def return_modelKirilimli1_fromOraDB(start_date, end_date):
    connection = oracledb.connect(dsn)
    query = f"""
        SELECT DISTINCT
            CASE 
                WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
            END AS TOPMODEL_DEFINITION,
            -- YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION,
            CASE 
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
            END AS BASEMODEL_DEFINITION,
            COUNT(YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS ORDER_COUNT
            FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK 
            RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR > 2022)
            LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
            LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID = YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
            WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL 
            AND  YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.DS_DATE BETWEEN TO_DATE('{start_date}', 'DD.MM.YYYY') AND TO_DATE('{end_date}', 'DD.MM.YYYY')
            
            
            AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
            GROUP BY 
                CASE 
                WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
            END ,
            CASE 
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
            END
            ORDER BY 
                CASE 
                WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
            END 
    """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    return results

# Returns "Perakende"
def return_modelKirilimli2_fromOraDB(start_date, end_date):
    connection = oracledb.connect(dsn)
    query = f"""
            SELECT DISTINCT
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END AS TOPMODEL_DEFINITION,
                -- YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END AS BASEMODEL_DEFINITION,
                COUNT(YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS ORDER_COUNT
                FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK 
                RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR > 2022)
                LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID = YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
                WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL 
                AND  YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.YS_DATE BETWEEN TO_DATE('{start_date}', 'DD.MM.YYYY') AND TO_DATE('{end_date}', 'DD.MM.YYYY')
                AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
                GROUP BY 
                    CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END ,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END
                ORDER BY 
                    CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END 
       
    """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    return results

# Returns "YS_stok"
def return_modelKirilimli3_fromOraDB():
    connection = oracledb.connect(dsn)
    query = f"""
            SELECT DISTINCT
                CASE
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION
                END AS TOPMODEL_DEFINITION,
                -- YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION,
                CASE
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION
                END AS BASEMODEL_DEFINITION,
                COUNT(DISTINCT YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS ORDER_COUNT
                
                FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK
                RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR > 2022)
                LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID = YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
                WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL
                AND YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.OEM_STATUS_EXPLANATION IN ('YSStok','Faturalandı','Fatura Bekliyor')
                AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
                
                GROUP BY
                    CASE
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION
                END ,
                CASE
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION
                END
                
                ORDER BY
                    CASE
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION
                END
    """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    return results

# Returns "Stok_Fiktif"
def return_modelKirilimli4_fromOraDB(yolda_status_excluded):
    connection = oracledb.connect(dsn)
    if yolda_status_excluded == False:
        query = f"""
            SELECT DISTINCT
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END AS TOPMODEL_DEFINITION,
                -- YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END AS BASEMODEL_DEFINITION,
                COUNT(YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS ORDER_COUNT
                FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK 
                RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR > 2022)
                LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID = YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
                WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL 
                AND YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.OEM_STATUS_EXPLANATION IN ('Stok','Fiktif')
                AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
                GROUP BY 
                    CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END ,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END
                ORDER BY 
                    CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END 
        """
    else:
        query = f"""
            SELECT DISTINCT 
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END AS TOPMODEL_DEFINITION,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END AS BASEMODEL_DEFINITION,

                COUNT (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS "Geliş" ,
                YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.STATUS

                FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK 
                RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE  ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO  = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR  > 2022)
                LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO  = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID =YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C ON (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO = YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.ORDER_NO)
                WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL 
                AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
                AND YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.OEM_STATUS_EXPLANATION NOT IN ('MüşFatura','YSStok','Fatura Bekliyor','Faturalandı','Stok','Fiktif')
                AND YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.STATUS IS NOT NULL 
                AND  EXTRACT (MONTH FROM YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.UPDATE_DATE) = EXTRACT (MONTH FROM SYSDATE)
                GROUP BY 
                YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.STATUS,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END
             
        """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    return results

# 
def return_modelKirilimli5_fromOraDB(yolda_status_excluded):
    connection = oracledb.connect(dsn)
    if yolda_status_excluded == False:
        query = f"""
            SELECT DISTINCT 
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END AS TOPMODEL_DEFINITION,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END AS BASEMODEL_DEFINITION,

                COUNT (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS "Geliş" ,
                YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.STATUS

                FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK 
                RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE  ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO  = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR  > 2022)
                LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO  = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID =YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C ON (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO = YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.ORDER_NO)
                WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL 
                AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
                AND YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.OEM_STATUS_EXPLANATION NOT IN ('MüşFatura','YSStok','Fatura Bekliyor','Faturalandı','Stok','Fiktif')
                AND YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.STATUS IS NOT NULL 
                AND  EXTRACT (MONTH FROM YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.UPDATE_DATE) = EXTRACT (MONTH FROM SYSDATE)
                GROUP BY 
                YUCE_DM.TBL_DW_VEH_SHIP_ARRIVAL_LIST_C.STATUS,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END
        """
    else:
        query = f"""
            SELECT DISTINCT
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END AS TOPMODEL_DEFINITION,
                -- YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END AS BASEMODEL_DEFINITION,
                COUNT(YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO) AS ORDER_COUNT
                FROM YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK 
                RIGHT OUTER JOIN YUCE_DM.TBL_DW_VEH_VEHICLE ON (YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO = YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO AND YUCE_DM.TBL_DW_VEH_VEHICLE.MODEL_YEAR > 2022)
                LEFT OUTER JOIN YUCE_DM.TBL_DW_VEH_ORDER tdvo ON (tdvo.ORDER_NO = YUCE_DM.TBL_DW_VEH_VEHICLE.ORDER_NO)
                LEFT JOIN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL ON (YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.PK_VEHICLE_ID = YUCE_DM.TBL_DW_VEH_VEHICLE.VEHICLE_ID)
                WHERE YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.ORDER_NO IS NOT NULL 
                AND YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.OEM_STATUS_EXPLANATION IN ('Stok','Fiktif','Yolda')
                AND (YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE NOT IN ('FİLO Rezervli') OR YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.RESERVE IS NULL)
                GROUP BY 
                    CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END ,
                CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Kodiaq RS 2,0 TSI 245 PS DSG 4x4', 'Kodiaq Laurin & Klement Crystal 1,5 TSI ACT 150 PS DSG') THEN 'Kodiaq (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Octavia Combi Scout 1,5 TSI E-Tec 150 PS DSG', 'Octavia Combi Sportline 1,5 TSI E-Tec 150 PS DSG','') THEN 'Octavia (Diğer)'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION IN ('Superb Combi Scout 1,5 TSI ACT 150 PS DSG', 'Superb Combi Sportline 1,5 TSI ACT 150 PS DSG','Yeni Superb Combi Laurin & Klement 1,5 TSI mHEV 150 PS DSG','Yeni Superb Combi Prestige 1,5 TSI mHEV 150 PS DSG','Yeni Superb Laurin & Klement Crystal 2,0 TDI 193 PS DSG 4x4','Yeni Superb Laurin & Klement Crystal 2,0 TSI 265 PS DSG 4x4') THEN 'Superb (Diğer)'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.BASEMODEL_DEFINITION 
                END
                ORDER BY 
                    CASE 
                    WHEN YUCE_DM.TBL_DW_VEH_YS_SALES_STOCK.TOPMODEL_DEFINITION IN ('Octavia Combi') THEN 'Octavia'
                    WHEN YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION IN ('Superb Combi','Yeni Superb Combi') THEN 'Yeni Superb'
                    ELSE YUCE_DM.TBL_DW_VEH_VEHICLE_ALL.TOPMODEL_DEFINITION 
                END 
        """

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    return results

