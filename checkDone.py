import os, glob
import pandas as pd

FILES_PATH = ["SET DATA\\SET", "SET DATA\\mai"]

DONE_FILE = "done.txt"

df_stock = pd.read_csv("set_stock_symbol.csv")

done_list = ""
all_files = []
for path in FILES_PATH:
    all_files += glob.glob(path + "\\*.xlsx")

for idx, row in df_stock.iterrows():
    stock = row["ชื่อย่อหลักทรัพย์"]
    count = 0
    for file_type in ["balance_sheet", "income_statement", "cash_flow"]:
        fname = f"{stock}_{file_type}.xlsx"
        for path in FILES_PATH:
            if path + "\\" + fname in all_files:
                if os.path.getsize(path + "\\" + fname) > 18*1024:
                    count += 1
    
    if count == 3:
        done_list += stock + "\n"

with open(DONE_FILE, "w") as f:
    f.write(done_list)