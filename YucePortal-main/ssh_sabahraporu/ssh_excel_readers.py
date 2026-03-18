import pandas as pd
import xlwt
import math
import xlrd
import os


# Returns the holiday dates from the excel given.
def ReturnHolidayDates(filename, sheetname):
    df = pd.read_excel(filename, sheet_name=sheetname)
    holiday_dates = []
    for index, value in df.iloc[:, 0].items():
        try:
            if type(value) == str:
                holiday_dates.append(value)
            else:
                holiday_dates.append(value.strftime('%d-%m-%Y').replace("-", "."))
        except:pass
    """
    try:
        for i in range(df.shape[0]):
            date = df.iat[i, 0].strftime('%d-%m-%Y').replace("-", ".")
            holiday_dates.append(date)
    except:pass
    """
    holiday_dates_lastyear = []
    try:
        for i in range(160):
            date = df.iat[i, 1].strftime('%d-%m-%Y').replace("-", ".")
            holiday_dates_lastyear.append(date)
    except:pass

    return holiday_dates, holiday_dates_lastyear

# Reads the İşçilik+ve+Parça+Gelirleri Excel
def Read_SSH_Iscilik_ParcaGelirleri_Excel(excel_path, sheetname):
    df = pd.read_excel(excel_path, sheet_name=sheetname)

    empty_columns = [col for col in df.columns if df[col].isnull().all()]
    df.drop(empty_columns, axis=1, inplace=True)

    def extract_cell_from_table(row, column):
        value = df.at[row, "Unnamed: {}".format(column)]
        print(value)
        return value

    def nan_to_zero(value):
        if math.isnan(value):
            return 0
        else:
            return value

    i=0
    while extract_cell_from_table(i, 0) != "Toplam:":
            i=i+1
            Toplam_line = i

    İsemri_Adedi = extract_cell_from_table(Toplam_line, 4)

    ServisGiris = extract_cell_from_table(Toplam_line, 4)

    return İsemri_Adedi, ServisGiris

# New formula that works without mistakes
def Read_SSH_Iscilik_ParcaGelirleri_Excel2(excel_path, sheetname):
    clean_empty_columns_of_excel(excel_path, sheetname)
    def nan_to_zero(value):
        if math.isnan(value):
            return 0
        else:
            return value
    df = pd.read_excel(r"excel_input.xls", header=None)
    headers = df.iloc[2].dropna().tolist()
    Toplam_line = df.loc[df.iloc[:, 0] == 'Toplam:'].index[0]
    if 'Diğer' in headers:
        pass
    else:
        headers = df.iloc[3].dropna().tolist()
        if 'Diğer' in headers:
            pass
        else:
            headers = df.iloc[1].dropna().tolist()

    try:
        Skoda_Anahtar_index = headers.index('Skoda Anahtar')
    except:
        Skoda_Anahtar_index = 0
    try:
        Skoda_Yedek_Parca_index = headers.index("Skoda Yedek Parça ")
    except:
        Skoda_Yedek_Parca_index = 0
    try:
        Skoda_Etiket_index = headers.index('Skoda Etiket')
    except:
        Skoda_Etiket_index = 0
    try:
        Yedek_Parca_index = headers.index("Yedek Parça")
    except:
        Yedek_Parca_index = 0
    try:
        YS_MotorYaglari_index = headers.index("YS Motor Yağları")
    except:
        YS_MotorYaglari_index = 0

    lower_headers = df.iloc[4].tolist()
    if 'İş Emri' in lower_headers:
        pass
    else:
        lower_headers = df.iloc[3].tolist()
        if 'İş Emri' in lower_headers:
            pass
        else:
            lower_headers = df.iloc[2].tolist()
            if 'İş Emri' in lower_headers:
                pass
            else:
                lower_headers = df.iloc[1].tolist()
                if 'İş Emri' in lower_headers:
                    pass
                else:
                    lower_headers = df.iloc[5].tolist()

    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "İş Emri":
            count += 1
            if Skoda_Anahtar_index != 0:
                if count == Skoda_Anahtar_index + 1:
                    # print("Skoda Anahtar", i)
                    Skoda_Anahtar_isemri = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "Garanti":
            count += 1
            if Skoda_Anahtar_index != 0:
                if count == Skoda_Anahtar_index + 1:
                    # print("Skoda Anahtar", i)
                    Skoda_Anahtar_Garanti = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "İş Emri":
            count += 1
            if Skoda_Yedek_Parca_index != 0:
                if count == Skoda_Yedek_Parca_index + 1:
                    # print("Skoda Yedek Parça", i)
                    Skoda_YedekParca_isemri = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "Garanti":
            count += 1
            if Skoda_Yedek_Parca_index != 0:
                if count == Skoda_Yedek_Parca_index + 1:
                    # print("Skoda Yedek Parça", i)
                    Skoda_YedekParca_Garanti = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "İş Emri":
            count += 1
            if Skoda_Etiket_index != 0:
                if count == Skoda_Etiket_index + 1:
                    # print("Yedek Parça", i)
                    Skoda_Etiket_isemri = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "Garanti":
            count += 1
            if Skoda_Etiket_index != 0:
                if count == Skoda_Etiket_index + 1:
                    # print("Yedek Parça", i)
                    Skoda_Etiket_Garanti = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "İş Emri":
            count += 1
            if Yedek_Parca_index != 0:
                if count == Yedek_Parca_index + 1:
                    # print("Yedek Parça", i)
                    YedekParca_isemri = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "Garanti":
            count += 1
            if Yedek_Parca_index != 0:
                if count == Yedek_Parca_index + 1:
                    # print("Yedek Parça", i)
                    YedekParca_Garanti = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "İş Emri":
            count += 1
            if YS_MotorYaglari_index != 0:
                if count == YS_MotorYaglari_index + 1:
                    # print("YS Motor Yağları", i)
                    YSMotor_Yaglari_isemri = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break
    count = 0
    for i, elem in enumerate(lower_headers):
        if elem == "Garanti":
            count += 1
            if YS_MotorYaglari_index != 0:
                if count == YS_MotorYaglari_index + 1:
                    # print("YS Motor Yağları", i)
                    YSMotor_Yaglari_Garanti = round(nan_to_zero(df.iloc[Toplam_line, i]))
                    break

    try:
        Skoda_Anahtar_isemri
    except:
        Skoda_Anahtar_isemri = 0
    try:
        Skoda_YedekParca_isemri
    except:
        Skoda_YedekParca_isemri = 0
    try:
        YedekParca_isemri
    except:
        YedekParca_isemri = 0
    try:
        YSMotor_Yaglari_isemri
    except:
        YSMotor_Yaglari_isemri = 0
    try:
        Skoda_Etiket_isemri
    except:
        Skoda_Etiket_isemri = 0
    try:
        Skoda_Anahtar_Garanti
    except:
        Skoda_Anahtar_Garanti = 0
    try:
        Skoda_YedekParca_Garanti
    except:
        Skoda_YedekParca_Garanti = 0
    try:
        YedekParca_Garanti
    except:
        YedekParca_Garanti = 0
    try:
        YSMotor_Yaglari_Garanti
    except:
        YSMotor_Yaglari_Garanti = 0
    try:
        Skoda_Etiket_Garanti
    except:
        Skoda_Etiket_Garanti = 0
    #print(Skoda_Anahtar_isemri, Skoda_YedekParca_isemri, YedekParca_isemri, YSMotor_Yaglari_isemri, Skoda_Etiket_isemri)
    total_isemri = Skoda_Anahtar_isemri + Skoda_YedekParca_isemri + YedekParca_isemri + YSMotor_Yaglari_isemri + Skoda_Etiket_isemri
    total_garanti = Skoda_Anahtar_Garanti + Skoda_YedekParca_Garanti + YedekParca_Garanti + YSMotor_Yaglari_Garanti + Skoda_Etiket_Garanti

    os.remove('excel_input.xls')
   
    return  total_isemri, total_garanti

# Returns Hedef values
def Read_Hedefler_from_Excel(excel_path, sheetname, month):
    df = pd.read_excel(excel_path, sheet_name=sheetname)

    def extract_cell_from_table(row, column):
        value = df.at[row, "{}".format(column)]
        return value
    Parca_Satis_Hedef = round(extract_cell_from_table(month - 1, 'PARÇA SATIŞI HEDEF'))
    İs_Emri_Hedef = round(extract_cell_from_table(month - 1, 'İŞEMRİ HEDEF'))
    Aksesuar_Satis_Hedef = round(extract_cell_from_table(month - 1, 'AKSESUAR SATIŞI HEDEF'))

    return Parca_Satis_Hedef, İs_Emri_Hedef, Aksesuar_Satis_Hedef

# Reads the PRC-YSA-GBU-007+SSH+Parça+Satış Excel
def Read_SSH_ParcaSatis_Excel(excel_path, sheetname):
    df = pd.read_excel(excel_path, sheet_name=sheetname)

    df1 = df.loc[df.iloc[:, -16] == "Skoda Yedek Parça "]
    SkodaYedekParca_Toplam = round(df1.iloc[:, 17].sum())

    df2 = df.loc[df.iloc[:, -16] == "Yedek Parça"]
    YedekParca_Toplam = round(df2.iloc[:, 17].sum())

    df3 = df.loc[df.iloc[:, -16] == "YS Motor Yağları"]
    YSMotorYaglari_Toplam = round(df3.iloc[:, 17].sum())

    df4 = df.loc[df.iloc[:, -16] == "Skoda Anahtar"]
    SkodaAnahtar_Toplam = round(df4.iloc[:, 17].sum())

    Toplam = SkodaYedekParca_Toplam + YedekParca_Toplam + YSMotorYaglari_Toplam + SkodaAnahtar_Toplam

    return Toplam

    def extract_cell_from_table(row, column):
        value = df.at[row, "Unnamed: {}".format(column)]
        return value

    def nan_to_zero(value):
        if math.isnan(value):
            return 0
        else:
            return value

#
def clean_empty_columns_of_excel(excel_input, excel_sheetname):
    workbook = xlrd.open_workbook(excel_input)

    # Select the worksheet by name
    worksheet = workbook.sheet_by_name(excel_sheetname)

    # Get the list of merged cells
    merged_cells = worksheet.merged_cells

    # Find the number of columns in the worksheet
    num_cols = worksheet.ncols

    # Create a new workbook to write the updated data
    new_workbook = xlwt.Workbook()

    # Create a new worksheet in the new workbook
    new_worksheet = new_workbook.add_sheet(excel_sheetname)

    # Loop through each column in the original worksheet
    for col in range(num_cols):

        # Check if the column contains any values
        col_data = worksheet.col_values(col)

        # Check if the column is part of a merged cell
        in_merged_cell = False
        for merged_cell in merged_cells:
            _, _, merged_col_start, merged_col_end = merged_cell
            if col == merged_col_start:
                in_merged_cell = True
                break

        # Copy the column to the new worksheet if it's not empty and not part of a merged cell
        if any(col_data) and not in_merged_cell:
            for row in range(len(col_data)):
                new_worksheet.write(row, col, col_data[row])

    # Save the updated workbook to a new file
    new_workbook.save('excel_input.xls')

# Renames the file, "old_path" must be the full path
def RenameFile_in_a_path(old_path, new_filename):
    directory_path, old_filename = os.path.split(old_path)

    # Create the new path by joining the directory path with the new filename
    new_path = os.path.join(directory_path, new_filename)

    # Rename the file
    os.rename(old_path, new_path)

