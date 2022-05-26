#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import cn2an
pd.set_option("display.max_columns", None)

df = pd.read_csv('./0_taipei.csv')

# 選擇需要的變數
df=df[["a", "b", "bs", "twn", "cp", "e", "f", "g", "lat", "lon", "m", "s", "tp", "v"]]

# 欄位重新命名
df.rename(columns={
"a": "address" ,   # 地址 
"b": "style",  # 建物型態
"bs": "percent", # 主建物占比(%)
"twn": "district",  # 縣市+行政區
"cp": "parking_price", # 車位總價
"e": "date", # 交易日期
"f": "floor", # 樓層
"g": "age", # 屋齡
"lat": "latitude", # 緯度
"lon": "longitude", # 經度
"m": "management", # 管理組織
"s": "size", # 移轉總面積
"tp": "total_price", # 交易總價
"v": "v" # 總格局
}, inplace = True)

# 地址
df['address'] = df['address'].str.split("#").str.get(1)

#'主建物占比(%)'
df['percent'] = df['percent'].fillna('100%')
df['percent'] = df['percent'].str[:-2].astype(float)

# 縣市+行政區
ref = {
'A10':'台北市中山區',
'A03':'台北市中正區',
'A17':'台北市信義區',
'A14':'台北市內湖區',
'A16':'台北市北投區',
'A13':'台北市南港區',
'A15':'台北市士林區',
'A09':'台北市大同區',
'A02':'台北市大安區',
'A11':'台北市文山區',
'A01':'台北市松山區',
'A05':'台北市萬華區',
'F15':'新北市三峽區',
'F30':'新北市三芝區',
'F05':'新北市三重區',
'F18':'新北市中和區',
'F03':'新北市五股區',
'F32':'新北市八里區',
'F19':'新北市土城區',
'F10':'新北市坪林區',
'F22':'新北市平溪區',
'F14':'新北市板橋區',
'F02':'新北市林口區',
'F33':'新北市永和區',
'F28':'新北市汐止區',
'F06':'新北市泰山區',
'F11':'新北市烏來區',
'F08':'新北市石碇區',
'F31':'新北市石門區',
'F24':'新北市貢寮區',
'F25':'新北市金山區',
'F27':'新北市淡水區',
'F09':'新北市深坑區',
'F07':'新北市新店區',
'F01':'新北市新莊區',
'F21':'新北市瑞芳區',
'F26':'新北市萬里區',
'F17':'新北市樹林區',
'F23':'新北市雙溪區',
'F04':'新北市蘆洲區',
'F16':'新北市鶯歌區'
}

for id in ref:
    df['district'] = df['district'].replace(id, ref[id])

# '車位總價'
df['parking_price'] = df['parking_price'].fillna('0')
df['parking_price'] = df['parking_price'].str.replace(',','').astype(float)
df['parking_price'] = df['parking_price'].fillna(0)

# '屋齡'
df['age'] = df['age'].fillna(0)

# 移轉總面積'
df['size'] = df['size'].str.replace(',','').astype(float)
bad = df.index[df['size'] == 0]
df = df.drop(bad)

# '交易總價'
df['total_price'] = df['total_price'].str.replace(',','').astype(float)
bad = df.index[df['total_price'] == 0]
df = df.drop(bad)

# '管理組織'
manage = {'有':1, '無':0}
for condition in manage:
    df['management'] = df['management'].replace(condition, manage[condition])

# 房廳衛
df['room']=df['v'].str.split('(\u623F|\u5EF3|\u885B)').str.get(0)
df['living']=df['v'].str.split('(\u623F|\u5EF3|\u885B)').str.get(2)
df['bath']=df['v'].str.split('(\u623F|\u5EF3|\u885B)').str.get(4)
df= df.drop(['v'], axis=1)

bad = df['bath'].index[df['bath'].astype(str)=="nan"]
df = df.drop(bad)

# 樓層
floor = df['floor'].str.split("/").str.get(0).str.split('([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94|\u516d|\u4e03|\u516b|\u4e5d|\u5341]+)(\u5c64)').str.get(1)

na_index = floor.index[floor.astype(str) == "nan"]
floor = floor.drop(na_index)
df = df.drop(na_index)

nums = []
for num in floor :
    nums.append(cn2an.cn2an(num))

floor_nums = np.array(nums)
df['floor'] = floor_nums


# 建物型態
styles = ['住宅大樓(11層含以上有電梯)' ,
        '公寓(5樓含以下無電梯)' ,
        '華廈(10層含以下有電梯)' ,
        '透天厝' ,
        '套房(1房(1廳)1衛)' ]

df = pd.concat([df[df['style'] == style ] for style in styles], ignore_index=True)

# 離群值 異常值
bad = df.index[df['date'] % 100 == 0 ]
df = df.drop(bad)
df = df[df['date'] > 10200]

df['avg'] = df['total_price'] / df['size']
Q1 = df['avg'].quantile(0.25)
Q3 = df['avg'].quantile(0.75)
IQR = Q3 - Q1

df = df.query('(@Q1 - 1.5 * @IQR) <= avg <= (@Q3 + 1.5 * @IQR)')
df.reset_index(drop = True, inplace = True)

#微調
df['style'] = df['style'].str.split("(").str.get(0)
df['date'] = df['date'] + 191100

df.to_csv('./1_taipei_purged.csv', index=False)
