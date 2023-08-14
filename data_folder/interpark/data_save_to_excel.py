import csv
import pandas as pd
from datetime import date

def load_data(file_path):
    datas = []
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for data in reader:
            datas.append(data)
    return datas

def save_to_excel(current_dir, file_path, keys):
    df = pd.DataFrame(load_data(file_path), columns=keys)
    df.to_excel(f'{current_dir}/interpark_excel/exhibit_{date.today()}.xlsx', index=False)