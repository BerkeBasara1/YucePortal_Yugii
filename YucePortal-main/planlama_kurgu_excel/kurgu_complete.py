from planlama_kurgu_excel.kurgu_ora import *
from planlama_kurgu_excel.kurgu_excel_func import kurgu_excel_func


def kurgu_complete(excel_path, yolda_status_excluded, start_date, end_date, session_email):
    result1 = return_modelKirilimli1_fromOraDB(start_date, end_date)
    result2 = return_modelKirilimli2_fromOraDB(start_date, end_date)
    result3 = return_modelKirilimli3_fromOraDB()
    result4 = return_modelKirilimli4_fromOraDB(yolda_status_excluded)
    result5 = return_modelKirilimli5_fromOraDB(yolda_status_excluded)

    excel_path_to_be_saved = r'Y:\YUCE AUTO GENEL\RPA_Doga\Planlama_Kurgu\Kurgu Dosyası.xlsx'
    kurgu_excel_func(excel_path, result1, result2, result3, result4, result5, excel_path_to_be_saved)




    



    




#kurgu_complete(r'C:\Users\yuceappadmin\Documents\GitHub\RPA-Projects\planlama_kurgu_excel\Örnek Kurgu Dosyası.xlsx')