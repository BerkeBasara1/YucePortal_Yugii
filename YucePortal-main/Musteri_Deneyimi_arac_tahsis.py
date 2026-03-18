# Excel Tablo Değerleri
sheet_list = ['Geçici Araç Durum Özeti', 'Geçici Araç Tahsis Takip 2024']
table_list = ['GeciciAracDurumOzeti2024', 'GeciciAracTahsisi2024']

YuceDB_alchemy_key = f"mssql+pyodbc://usryuceauto:Reader142536@YUCESQL2\SQL201701/Raporlar?driver=ODBC+Driver+17+for+SQL+Server"

mus_deneyimi_excel_path = r"Y:\MUSTERI DENEYIM YONETIMI\MUSTERI DENEYIM ORTAK\11-Mİ (SİLİNMEYECEK-ÖNEMLİ)\Yüce Auto Tahsis Araç Klasörü\Yüce Auto Geçici Araç Tahsis Takip Listesi 2024.xlsx"

from datetime import datetime
import openpyxl
import pyodbc
import time
import os
from send_email import *
from config import *
import pandas as pd
from sqlalchemy import text, create_engine


YuceDB_alchemy_key = f"mssql+pyodbc://usryuceauto:Reader142536@YUCESQL2\SQL201701/Raporlar?driver=ODBC+Driver+17+for+SQL+Server"
sheet_list = ['Geçici Araç Durum Özeti', 'Geçici Araç Tahsis Takip 2024']
table_list = ['GeciciAracDurumOzeti2024', 'GeciciAracTahsisi2024']

sheet_list2 = ['DASHBOARD1', 'DASHBOARD2']
table_list2 = ['DASHBOARD1_2024', 'DASHBOARD2_2024']


def excel_to_sql_GeciciArac(Arac_Tahsis_Excel_Path):
    for i in range(len(sheet_list)):
        excel = pd.read_excel(Arac_Tahsis_Excel_Path, sheet_name=sheet_list[i])

        # Düzeltilmiş sütun adlarını oluştur
        cleaned_columns = [col.replace("\n", "_") for col in excel.columns]
        excel.columns = cleaned_columns

        # Remove rows where both "Müşteri Adı" and "Plaka" are null for the specific sheets
        if sheet_list[i] in ['Geçici Araç Tahsis Takip 2024']:
            excel = excel.dropna(subset=['Müşteri Adı', 'Plaka'], how='all')

        # Connects to the Database given
        db_engine = create_engine(YuceDB_alchemy_key)

        # Boş olmayan sütunları filtrele
        non_empty_columns = [col for col in excel.columns if not excel[col].isnull().all()]
        excel_filtered = excel.loc[:, non_empty_columns].copy()
        # "S.No" sütununu belirli tablolardan çıkarmak
        if sheet_list[i] in ["Geçici Araç Durum Özeti", "Geçici Araç Tahsis Takip 2024"]:
            excel_filtered = excel_filtered.iloc[:, 1:]

         # Create a copy to avoid SettingWithCopyWarning

        # "Kritik" sütununu kaldır, eğer varsa
        if "Kritik" in excel_filtered.columns:
            excel_filtered = excel_filtered.drop(columns=["Kritik"])

        # Mevcut tarih ve saati içeren bir zaman damgası sütunu ekle
        excel_filtered['Timestamp'] = datetime.now()

        excel_filtered = excel_filtered.dropna(how='all')

        # Veritabanına DataFrame'i yaz
        excel_filtered.to_sql(table_list[i], db_engine, if_exists='replace', index=False)

def excel_to_sql_DashboardData(Arac_Tahsis_Excel_Path):
    for i in range(len(sheet_list2)):
        excel = pd.read_excel(Arac_Tahsis_Excel_Path, sheet_name=sheet_list2[i])

        # Düzeltilmiş sütun adlarını oluştur
        cleaned_columns = [col.replace("\n", "_") for col in excel.columns]
        excel.columns = cleaned_columns

        # Connects to the Database given
        db_engine = create_engine(YuceDB_alchemy_key)

        # Boş olmayan sütunları filtrele
        non_empty_columns = [col for col in excel.columns if not excel[col].isnull().all()]

        excel_filtered = excel.loc[:, non_empty_columns].copy()  # Create a copy to avoid SettingWithCopyWarning

        # Mevcut tarih ve saati içeren bir zaman damgası sütunu ekle
        excel_filtered['Timestamp'] = datetime.now()

        # Veritabanına DataFrame'i yaz
        excel_filtered.to_sql(table_list2[i], db_engine, if_exists='replace', index=False)

def excel_to_sql_Doga(Arac_Tahsis_Excel_Path):
    excel_file = openpyxl.load_workbook(Arac_Tahsis_Excel_Path, data_only=True)
    sheet = excel_file.get_sheet_by_name("DASHBOARD3_2024")

    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=YUCESQL2\SQL201701;DATABASE=Raporlar;UID=usryuceauto;PWD=Reader142536")
    cursor = conn.cursor()
    i = 0

    delete_query = "DELETE FROM DASHBOARD3"
    cursor.execute((delete_query))

    for row in sheet.iter_rows(values_only=True):
        if i != 0:

            traffic_date = f"'{row[2].strftime('%Y-%m-%d')}'" if isinstance(row[2], datetime) else 'NULL'
            ds_alis_tarihi = f"'{row[6].strftime('%Y-%m-%d')}'" if isinstance(row[6], datetime) else 'NULL'
            ds_satilma_tarihi = f"'{row[7].strftime('%Y-%m-%d')}'" if isinstance(row[7], datetime) else 'NULL'
            guncel_tarih = f"'{row[8].strftime('%Y-%m-%d')}'" if isinstance(row[8], datetime) else 'NULL'

            query = """
            INSERT INTO DASHBOARD3 (
                CHASSIS, PLATE, TRAFFIC_DATE, MODEL, COLOUR, VEHICLE_MILEAGE,
                DS_ALIS_TARIHI, DS_SATILMA_TARIHI, GUNCEL_TARIH, VEHICLE_BACK_PAYMENT,
                TRAFFIC_SIGORTA_PRICE_2024, KASKO_PRICE_2024, TRAFFIC_SIGORTA_PRICE_2025,
                KASKO_PRICE_2025, MAINTENANCE_PAYMENT_2024, MAINTENANCE_PAYMENT_2025,
                EXISTING_KM, SECOND_HAND_PRICE, CAR_COST, FUNDING_COST, TOTAL_COST, USAGE_DAY,
                TOTAL_EARN_FROM_USAGE
            )
            VALUES ('{}', '{}', {}, '{}', '{}', {},
                    {}, {}, {}, {}, 
                    {}, {}, {}, 
                    {}, {}, {}, 
                    {}, {}, {}, {}, {}, {}, 
                    {});
            """.format(
                row[0], row[1], traffic_date, row[3], row[4], row[5],
                ds_alis_tarihi, ds_satilma_tarihi, guncel_tarih, row[9],
                row[10], row[11], row[12],
                row[13], row[14], row[15],
                row[16], row[17], row[18], row[19], row[20], row[21],
                row[22])
            query = query.replace("None", "Null")
            #print(query)
            cursor.execute(query)
        i += 1
    conn.commit()
    cursor.close()
    conn.close()


def run_Musteri_Deneyimi_AracTahsis_excel_auto():
    excel_to_sql_DashboardData(mus_deneyimi_excel_path)
    excel_to_sql_GeciciArac(mus_deneyimi_excel_path)

    #Newly added by Doğa
    excel_to_sql_Doga(mus_deneyimi_excel_path)

    db_engine = create_engine(YuceDB_alchemy_key)

    query1 = "DELETE FROM [Raporlar].[dbo].[GeciciAracDurumOzeti2024] WHERE [Tahis Araç Model] IS NULL AND [İkame Araç Plaka] IS NULL AND [Kullanım Durumu] IS NULL AND [İl] IS NULL AND [Bulunduğu Yetkili Servis] IS NULL"
    #query2 = "DELETE FROM [Raporlar].[dbo].[LenaBodrumGeciciArac] WHERE [Tahis Araç Model] IS NULL AND [İkame Araç Plaka] IS NULL AND [Kullanım Durumu] IS NULL AND [İl] IS NULL AND [Bulunduğu Yetkili Servis] IS NULL"

    with db_engine.connect() as connection:
        connection.execute(text(query1))
        #connection.execute(text(query2))
        connection.commit()
