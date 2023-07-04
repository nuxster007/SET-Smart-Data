import pandas as pd
import glob, os
import time
from datetime import datetime, timedelta
import openpyxl
import xlrd

DATA_PATH = "C:\\temp\\SET_Data\\"
#FILE_NAME = "AOT_balance_sheet.xlsx"
FILE_NAME = "AOT_cash_flow.xlsx"

df = pd.read_excel(DATA_PATH + FILE_NAME, engine="openpyxl", skiprows=12)

# Rename columns for better understanding / reading
df.rename(columns={ df.columns[0]: "รายการ" }, inplace = True)
for col in range(1, len(df.columns[1:]) + 1):
    y = df.columns[col].split("/ ")[1].split(" ")[0]
    q = df.columns[col].split(" /")[0].replace("งบปี", "Q4").replace("ไตรมาสที่ ", "Q")
    df.rename(columns={ df.columns[col]: f"{q} / {y}" }, inplace = True)

# Adjust some items before process
# df.loc[df["รายการ"] == " สินทรัพย์", "รายการ"] = "สินทรัพย์"
# df.loc[df["รายการ"] == " สินทรัพย์หมุนเวียน", "รายการ"] = "  สินทรัพย์หมุนเวียน"
# df.loc[df["รายการ"] == " สินทรัพย์ไม่หมุนเวียน", "รายการ"] = "  สินทรัพย์ไม่หมุนเวียน"
# df.loc[df["รายการ"] == " หนี้สิน", "รายการ"] = "หนี้สิน"
# df.loc[df["รายการ"] == " หนี้สินหมุนเวียน", "รายการ"] = "หนี้สินหมุนเวียน"
# df.loc[df["รายการ"] == " หนี้สินไม่หมุนเวียน", "รายการ"] = "หนี้สินไม่หมุนเวียน"
# df.loc[df["รายการ"] == " ส่วนของผู้ถือหุ้น", "รายการ"] = "ส่วนของผู้ถือหุ้น"

parent = ""
items_chain = ""
last_item = ""
last_level = 0
items_to_remove = []
start_to_remove = False

for idx, row in df.iterrows():
    sp = len(row["รายการ"]) - len(row["รายการ"].lstrip())

    if idx == 0:
        level = 0
    elif sp == 1:
        level = 1
    else:
        level = int(sp / 2)
    
    if level > last_level:
        items_chain += "|" + last_item
    elif level < last_level:
        items_chain = "|".join(items_chain.split("|")[:-1])

    parent = items_chain.split("|")[-1]

    df.at[idx, "Parent"] = parent
    df.at[idx, "Level"] = level
    df.at[idx, "Order"] = idx

    last_item = row["รายการ"].lstrip()
    last_level = level
    df.iat[idx, 0] = "-->"*level + row["รายการ"].lstrip()

    if row["รายการ"] == "งบการเงินฉบับเต็ม:":
        start_to_remove = True

    if start_to_remove:
        items_to_remove.append(row["รายการ"])

print(items_to_remove)

df = df.drop(df[df["รายการ"].isin(items_to_remove)].index)

print(df[["รายการ", "Parent", "Level", "Order"]].head(10))

df.to_csv("test.csv", sep="|", encoding="utf-8-sig")



