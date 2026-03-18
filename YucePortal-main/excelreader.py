import pandas as pd


# EXCEL SATIŞ ADETLERİ TABLOSU SCRAPING
def ExcelRead(filename, sheetname, DigerSatislarValueAyFromTurkuaz):
    df = pd.read_excel(filename, sheet_name=sheetname)

    def extract_cell_from_table(row, column):
        value = df.at[row, "Unnamed: {}".format(column)]
        return value

    table_headers = []
    for i in range(1000):
        try:
            table_header = extract_cell_from_table(27, i)
            if type(table_header) == str:
                table_headers.append(table_header)
        except:
            pass
        
    FPTM_cols = []
    for i in range(1000):
        try:
            FPTM = extract_cell_from_table(28, i)
            if type(FPTM) == str:
                FPTM_cols.append(i)
        except:
            pass
    if len(FPTM_cols) == 0:
        for i in range(1000):
            try:
                FPTM = extract_cell_from_table(29, i)
                if type(FPTM) == str:
                    FPTM_cols.append(i)
            except:
                pass
    if len(FPTM_cols) == 0:
        for i in range(1000):
            try:
                FPTM = extract_cell_from_table(30, i)
                if type(FPTM) == str:
                    FPTM_cols.append(i)
            except:
                pass
    if len(FPTM_cols) == 0:
        for i in range(1000):
            try:
                FPTM = extract_cell_from_table(31, i)
                if type(FPTM) == str:
                    FPTM_cols.append(i)
            except:
                pass
    if len(FPTM_cols) == 0:
        for i in range(1000):
            try:
                FPTM = extract_cell_from_table(27, i)
                if type(FPTM) == str:
                    FPTM_cols.append(i)
            except:
                pass
    if len(FPTM_cols) == 0:
        for i in range(1000):
            try:
                FPTM = extract_cell_from_table(26, i)
                if type(FPTM) == str:
                    FPTM_cols.append(i)
            except:
                pass
    if len(FPTM_cols) == 0:
        for i in range(1000):
            try:
                FPTM = extract_cell_from_table(25, i)
                if type(FPTM) == str:
                    FPTM_cols.append(i)
            except:
                pass
    
    FPTM_data = []
    FPTMs_countz = 0
    for number in FPTM_cols:
        FPTM_number = extract_cell_from_table(39, number)
        if type(FPTM_number) == int:
            FPTM_data.append(FPTM_number)
            FPTMs_countz += 1
        else:
            FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(40, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(41, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(42, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(43, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(44, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(45, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(46, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")
    if FPTMs_countz == 0:
        FPTM_data = []
        FPTMs_countz = 0
        for number in FPTM_cols:
            FPTM_number = extract_cell_from_table(47, number)
            if type(FPTM_number) == int:
                FPTM_data.append(FPTM_number)
                FPTMs_countz += 1
            else:
                FPTM_data.append("empty")


    try:
        Aylik_DS_Satis_val = FPTM_data[5]
        Aylik_DS_Satis_F = FPTM_data[3]
        Yillik_DS_Toptan_val = FPTM_data[8]
        Aylik_YS_Satis_F = FPTM_data[12]
        Aylik_YS_Satis_val = FPTM_data[14]
        Yillik_YS_Satis_val = FPTM_data[17]
    except:
        Aylik_DS_Satis_val = 999
        Aylik_DS_Satis_F = 999
        Yillik_DS_Toptan_val = 999
        Aylik_YS_Satis_F = 999
        Aylik_YS_Satis_val = 999
        Yillik_YS_Satis_val = 999


    def nullcorrector(input):
        if input != 'empty':
            if input >= 0:
                pass
            else:
                input = 0
            result = input
        else:
            result = 0
        return result
    Aylik_YS_Satis_val = nullcorrector(Aylik_YS_Satis_val)
    Aylik_DS_Satis_val = nullcorrector(Aylik_DS_Satis_val)
    Aylik_YS_Satis_F = nullcorrector(Aylik_YS_Satis_F)
    Yillik_YS_Satis_val = nullcorrector(Yillik_YS_Satis_val)
    Yillik_DS_Toptan_val = nullcorrector(Yillik_DS_Toptan_val)
    Aylik_DS_Satis_F  = nullcorrector(Aylik_DS_Satis_F)
    Aylik_DS_Satis_F = int(Aylik_DS_Satis_F)
    Perakende_Ay = int(Aylik_YS_Satis_val)
    Perakende_Ay = format_with_period(Perakende_Ay)
    Toptan_Ay = Aylik_DS_Satis_val #- int(DigerSatislarValueAyFromTurkuaz)
    Toptan_Ay = format_with_period(Toptan_Ay)
    try:
        Perakende_Yil = int(Yillik_YS_Satis_val)
        Perakende_Yil = format_with_period(Perakende_Yil)
    except:
        Perakende_Yil=0
    Toptan_Yil = Yillik_DS_Toptan_val
    Toptan_Yil = format_with_period(Toptan_Yil)
    YSval_YSF = int(Aylik_YS_Satis_val) - int(Aylik_YS_Satis_F)
    Toptan_Aylik_eksi= int(Aylik_DS_Satis_val) - int(Aylik_DS_Satis_F)

    return Perakende_Ay, Toptan_Ay, Perakende_Yil, Toptan_Yil, Aylik_YS_Satis_F, YSval_YSF, Aylik_DS_Satis_F, Toptan_Aylik_eksi

# YS/DS STOK DURUMU DATASINI SCRAPE ETME EXCEL
def ExcelRead2(filename, sheetname):
    df = pd.read_excel(filename, sheet_name=sheetname)
    def extract_cell_from_table(row, column):
        value = df.at[row, "Unnamed: {}".format(column)]
        return value

    # EXCEL STOK DURUMU TABLOSU SCRAPING
    #Baslik_list = []
    #Baslik_list.append(df.at[4, "Unnamed: 5"]) # F 6
    #Baslik_list.append(df.at[4, "Unnamed: 15"]) # P 6
    #Baslik_list.append(df.at[4, "Unnamed: 29"]) # AD 6
    #Baslik_list.append(df.at[4, "Unnamed: 41"])  # AP 6 bazen ap6ya gidi
    #Baslik_list.append(df.at[4, "Unnamed: 53"])  # BB 6
    #Baslik_list.append(df.at[4, "Unnamed: 66"])  # BO 6
    #Baslik_list.append(df.at[4, "Unnamed: 78"])  # CA 6
    #Baslik_list.append(df.at[4, "Unnamed: 91"])  # CN 6
    #Baslik_list.append(df.at[4, "Unnamed: 99"])  # CV 6

    table_headers = []
    for i in range(1000):
        try:
            table_header = extract_cell_from_table(4, i)
            if type(table_header) == str:
                table_headers.append(table_header)
        except:
            pass
    FPTM_cols = []
    for i in range(1000):
        try:
            FPTM = extract_cell_from_table(5, i)
            if type(FPTM) == str:
                FPTM_cols.append(i)
        except:
            pass
    FPTM_data = []
    for number in FPTM_cols:
        FPTM_number = extract_cell_from_table(19, number)
        if type(FPTM_number) == int:
            FPTM_data.append(FPTM_number)
        else:
            FPTM_data.append("empty")
    T_value1 = FPTM_data[2]
    M_value1 = FPTM_data[3]

    T_value2 = FPTM_data[6]
    M_value2 = FPTM_data[7]

    T_value3 = FPTM_data[10]
    M_value3 = FPTM_data[11]

    T_value4 = FPTM_data[14]
    M_value4 = FPTM_data[15]

    T_value5 = FPTM_data[18]
    M_value5 = FPTM_data[19]

    T_value6 = FPTM_data[22]
    M_value6 = FPTM_data[23]

    T_value7 = FPTM_data[26]
    M_value7 = FPTM_data[27]

    try:
        T_value8 = FPTM_data[30]
    except:
        T_value8 = 0
    try:
        M_value8 = FPTM_data[31]
    except:
        M_value8 = 0
    
    try:
        T_value9 = FPTM_data[34]
    except:
        T_value9 = 0
    try:
        M_value9 = FPTM_data[35]
    except:
        M_value9 = 0

    table_values = {table_headers[0] + '_T' : T_value1, table_headers[0] + '_M' : M_value1,
                    table_headers[1] + '_T' : T_value2, table_headers[1] + '_M' : M_value2,
                    table_headers[2] + '_T' : T_value3, table_headers[2] + '_M' : M_value3,
                    table_headers[3] + '_T' : T_value4, table_headers[3] + '_M' : M_value4,
                    table_headers[4] + '_T' : T_value5, table_headers[4] + '_M' : M_value5,
                    table_headers[5] + '_T' : T_value6, table_headers[5] + '_M' : M_value6,
                    table_headers[6] + '_T' : T_value7, table_headers[6] + '_M' : M_value7,
                    table_headers[7] + '_T' : T_value8, table_headers[7] + '_M' : M_value8,
                    table_headers[8] + '_T' : T_value9, table_headers[8] + '_M' : M_value9,
                    }
    return table_values

# Araç model bazlı data okuma EXCEL
def ExcelRead3(filename, sheetname):
    df = pd.read_excel(filename, sheet_name=sheetname)
    def nanTo0Converter(nan_object):
        if nan_object >= 0:
            pass
        else:
            nan_object = 0
    headers_of_the_tables = df.iloc[4].values
    correct_headers = []
    for value in headers_of_the_tables:
        if type(value) == str:
            correct_headers.append(value)
    if correct_headers[3] == 'YSStok':
        FABIA_M = df.at[6, "Unnamed: 36"] # AK8 in excel
        FABIA_T = df.at[6, "Unnamed: 33"]
        nanTo0Converter(FABIA_M)
        nanTo0Converter(FABIA_T)
        try:
            perc_Fabia = str(round((FABIA_M / FABIA_T) * 100))
        except:
            perc_Fabia = 0
        OCTAVIA_M1 = df.at[7, "Unnamed: 36"] # AK9 in excel
        OCTAVIA_T1 = df.at[7, "Unnamed: 33"]
        nanTo0Converter(OCTAVIA_M1)
        nanTo0Converter(OCTAVIA_T1)
        OCTAVIA_M2 = df.at[8, "Unnamed: 36"] # AK10 in excel
        OCTAVIA_T2 = df.at[8, "Unnamed: 33"]
        nanTo0Converter(OCTAVIA_M2)
        nanTo0Converter(OCTAVIA_T2)
        try:
            s = int(OCTAVIA_M2)
        except:
            OCTAVIA_M2 = 0
        try:
            s = int(OCTAVIA_T2)
        except:
            OCTAVIA_T2 = 0
        OCTAVIA_M = OCTAVIA_M1 + OCTAVIA_M2
        OCTAVIA_T = OCTAVIA_T1 + OCTAVIA_T2
        nanTo0Converter(OCTAVIA_M)
        nanTo0Converter(OCTAVIA_T)
        try:
            perc_Octavia = str(round((OCTAVIA_M / OCTAVIA_T) * 100))
        except:
            perc_Octavia = "0"
        KAROQ_M = df.at[9, "Unnamed: 36"] # AK11 in excel
        KAROQ_T = df.at[9, "Unnamed: 33"]
        nanTo0Converter(KAROQ_M)
        nanTo0Converter(KAROQ_T)
        try:
            perc_Karoq = str(round((KAROQ_M / KAROQ_T) * 100))
        except:
            perc_Karoq = 0
        KODIAQ_M = df.at[10, "Unnamed: 36"] # AK12 in excel
        KODIAQ_T = df.at[10, "Unnamed: 33"]
        nanTo0Converter(KODIAQ_M)
        nanTo0Converter(KODIAQ_T)
        try:
            perc_Kodiaq = str(round((KODIAQ_M / KODIAQ_T) * 100))
        except:
            perc_Kodiaq = 0
        SUPERB_M1 = df.at[11, "Unnamed: 36"] # AK13 in excel
        SUPERB_T1 = df.at[11, "Unnamed: 33"]
        nanTo0Converter(SUPERB_M1)
        nanTo0Converter(SUPERB_T1)
        SUPERB_M2 = df.at[13, "Unnamed: 36"]
        SUPERB_T2 = df.at[13, "Unnamed: 33"]
        nanTo0Converter(SUPERB_M2)
        nanTo0Converter(SUPERB_T2)
        try:
            s = int(SUPERB_M2)
        except:
            SUPERB_M2 = 0
        try:
            s = int(SUPERB_T2)
        except:
            SUPERB_T2 = 0
        try:
            s = int(SUPERB_T1)
        except:
            SUPERB_T1 = 0
        try:
            s = int(SUPERB_M1)
        except:
            SUPERB_M1 = 0

        SUPERB_M = SUPERB_M1 + SUPERB_M2
        SUPERB_T = SUPERB_T1 + SUPERB_T2

        try:
            perc_Superb = str(round((SUPERB_M / SUPERB_T) * 100))
        except:
            perc_Superb = 0

        SCALA_M = df.at[15, "Unnamed: 36"] # AK14 in excel
        SCALA_T = df.at[15, "Unnamed: 33"]
        nanTo0Converter(SCALA_M)
        nanTo0Converter(SCALA_T)
        try:
            s = int(SCALA_M)
        except:
            SCALA_M = 0
        try:
            s = int(SCALA_T)
        except:
            SCALA_T = 0
        try:
            perc_Scala = str(round((SCALA_M / SCALA_T) * 100))
        except:
            perc_Scala = "0"
        KAMIQ_M = df.at[16, "Unnamed: 36"] # AK13 in excel
        KAMIQ_T = df.at[16, "Unnamed: 33"]
        nanTo0Converter(KAMIQ_M)
        nanTo0Converter(KAMIQ_T)
        try:
            perc_Kamiq = str(round((KAMIQ_M / KAMIQ_T) * 100))
        except:
            perc_Kamiq = 0
        T_toplam = FABIA_T + OCTAVIA_T + KAROQ_T + KODIAQ_T + SUPERB_T + SCALA_T + KAMIQ_T
        M_toplam = FABIA_M + OCTAVIA_M + KAROQ_M + KODIAQ_M + SUPERB_M + SCALA_M + KAMIQ_M
        try:
            perc_Toplam = str(round((M_toplam / T_toplam) * 100))
        except:
            perc_Toplam = 0
    elif correct_headers[2] == 'YSStok':
        FABIA_M = df.at[6, "Unnamed: 24"]
        FABIA_T = df.at[6, "Unnamed: 22"]
        nanTo0Converter(FABIA_M)
        nanTo0Converter(FABIA_T)
        try:
            perc_Fabia = str(round((FABIA_M / FABIA_T) * 100))
        except:
            perc_Fabia = 0
        OCTAVIA_M1 = df.at[7, "Unnamed: 24"]
        OCTAVIA_T1 = df.at[7, "Unnamed: 22"]
        nanTo0Converter(OCTAVIA_M1)
        nanTo0Converter(OCTAVIA_T1)
        OCTAVIA_M2 = df.at[8, "Unnamed: 24"]
        OCTAVIA_T2 = df.at[8, "Unnamed: 22"]
        nanTo0Converter(OCTAVIA_M2)
        nanTo0Converter(OCTAVIA_T2)
        try:
            s = int(OCTAVIA_M2)
        except:
            OCTAVIA_M2 = 0
        try:
            s = int(OCTAVIA_T2)
        except:
            OCTAVIA_T2 = 0
        OCTAVIA_M = OCTAVIA_M1 + OCTAVIA_M2
        OCTAVIA_T = OCTAVIA_T1 + OCTAVIA_T2
        nanTo0Converter(OCTAVIA_M)
        nanTo0Converter(OCTAVIA_T)
        try:
            perc_Octavia = str(round((OCTAVIA_M / OCTAVIA_T) * 100))
        except:
            perc_Octavia = "0"
        KAROQ_M = df.at[9, "Unnamed: 24"]
        KAROQ_T = df.at[9, "Unnamed: 22"]
        nanTo0Converter(KAROQ_M)
        nanTo0Converter(KAROQ_T)
        perc_Karoq = str(round((KAROQ_M / KAROQ_T) * 100))
        KODIAQ_M = df.at[10, "Unnamed: 24"]
        KODIAQ_T = df.at[10, "Unnamed: 22"]
        nanTo0Converter(KODIAQ_M)
        nanTo0Converter(KODIAQ_T)
        perc_Kodiaq = str(round((KODIAQ_M / KODIAQ_T) * 100))
        SUPERB_M1 = df.at[11, "Unnamed: 24"]
        SUPERB_T1 = df.at[11, "Unnamed: 22"]
        nanTo0Converter(SUPERB_M1)
        nanTo0Converter(SUPERB_T1)
        SUPERB_M2 = df.at[13, "Unnamed: 24"]
        SUPERB_T2 = df.at[13, "Unnamed: 22"]
        nanTo0Converter(SUPERB_M2)
        nanTo0Converter(SUPERB_T2)
        SUPERB_M = SUPERB_M1 + SUPERB_M2
        SUPERB_T = SUPERB_T1 + SUPERB_T2
        try:
            perc_Superb = str(round((SUPERB_M / SUPERB_T) * 100))
        except:
            perc_Superb = 0
        SCALA_M = df.at[15, "Unnamed: 24"]
        SCALA_T = df.at[15, "Unnamed: 22"]
        nanTo0Converter(SCALA_M)
        nanTo0Converter(SCALA_T)
        try:
            s = int(SCALA_M)
        except:
            SCALA_M = 0
        try:
            s = int(SCALA_T)
        except:
            SCALA_T = 0
        try:
            perc_Scala = str(round((SCALA_M / SCALA_T) * 100))
        except:
            perc_Scala = 0
        KAMIQ_M = df.at[16, "Unnamed: 24"]
        KAMIQ_T = df.at[16, "Unnamed: 22"]
        nanTo0Converter(KAMIQ_M)
        nanTo0Converter(KAMIQ_T)
        try:
            perc_Kamiq = str(round((KAMIQ_M / KAMIQ_T) * 100))
        except:
            perc_Kamiq = 0
        T_toplam = FABIA_T + OCTAVIA_T + KAROQ_T + KODIAQ_T + SUPERB_T + SCALA_T + KAMIQ_T
        M_toplam = FABIA_M + OCTAVIA_M + KAROQ_M + KODIAQ_M + SUPERB_M + SCALA_M + KAMIQ_M
        try:
            perc_Toplam = str(round((M_toplam / T_toplam) * 100))
        except:
            perc_Toplam = 0
    return FABIA_T, OCTAVIA_T, KAROQ_T, KODIAQ_T, SUPERB_T, SCALA_T, KAMIQ_T, FABIA_M, OCTAVIA_M, KAROQ_M, KODIAQ_M, SUPERB_M, SCALA_M, KAMIQ_M,\
           T_toplam, M_toplam, perc_Fabia, perc_Octavia, perc_Karoq, perc_Kodiaq, perc_Superb, perc_Scala, perc_Kamiq, perc_Toplam

def format_with_period(n):
    n = str(n)
    n_len = len(n)
    if n_len <= 3:
        return n
    else:
        return format_with_period(n[:-3]) + "." + n[-3:]