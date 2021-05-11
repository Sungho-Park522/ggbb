import time
import datetime
import pyupbit
import pandas as pd

data = pd.read_csv('trade_info.txt', sep = "\t", engine='python', encoding = "cp949")
df = pd.DataFrame(data)
count = 1
while True:
    etc_price = pyupbit.get_current_price("KRW-ETC")
    dt_now = datetime.datetime.now()
    df = df.append({'date': str(count), ignore_index=True)
    count = count + 1
    df.to_csv('trade_info.txt',index=False, sep="\t")
