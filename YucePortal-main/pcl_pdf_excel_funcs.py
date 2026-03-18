import pandas as pd

def read_column_to_list(file_path):
    df = pd.read_excel(file_path)
    column_name = 'Unnamed: 0'
    column_values = df[column_name].tolist()

    return column_values