#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import re

# 讀取csv並刪除索引值為0的英文欄位名稱列
path_in = 'download_lvr_land/'
df_a = pd.read_csv(path_in+'a_lvr_land_a.csv', encoding='utf-8').drop([0], axis=0)
df_b = pd.read_csv(path_in+'b_lvr_land_a.csv', encoding='utf-8').drop([0], axis=0)
df_e = pd.read_csv(path_in+'e_lvr_land_a.csv', encoding='utf-8').drop([0], axis=0)
df_f = pd.read_csv(path_in+'f_lvr_land_a.csv', encoding='utf-8').drop([0], axis=0)
df_h = pd.read_csv(path_in+'h_lvr_land_a.csv', encoding='utf-8').drop([0], axis=0)

# 取欄位列表
columns = df_a.columns

# 四個縣市的資料合併
df_all = pd.concat([df_a, df_b, df_e, df_f, df_h], ignore_index=True)



# 定義條件式，篩選出來放在暫存df(filter_temp)
# (1)主要用途為"住家用"
# (2)建物型態為住宅大樓，但原資料的內容為'住宅大樓(11層含以上有電梯)'
condition_1 = df_all['主要用途'].isin(['住家用'])
condition_2 = df_all['建物型態'].isin(['住宅大樓(11層含以上有電梯)'])
filter_temp = df_all[(condition_1 & condition_2)]


# 檢視樓層欄位，型態為字串
# 內容為國文數字(ex.二十二層)，以及參有少許數值字串(ex."038")
# filter_temp['總樓層數'].unique()
# filter_temp['總樓層數'].value_counts()

# 為國字轉阿拉伯數字的函式建立dict
# 樓層至多到百單位
num_map = { '零': 0,
            '一': 1,
            '二': 2,
            '三': 3,
            '四': 4,
            '五': 5,
            '六': 6,
            '七': 7,
            '八': 8,
            '九': 9  }

unit_map = { '十': 10,
             '百': 100 }

# num_covert()進行中文數字轉數值
# 先取得完整的國文數值(cn_str)，接著反向遍歷該字串reversed(cn_str)
# 從最小單位往後推數值，以及乘上單位數值
# ex.reversed(三十四):(四>十>三)，先取到"四"可對應到num_map的4，
# 其單位一開始為個位數，這時樓層數(foolr_num)為0+4*1
# 接著取到"十"可對應unit_map的10，更換單位unit=10，樓層數不變。
# 再來取"三"可對應到num_map的3，乘上單位unit=10，樓層數=4+3*10=34
def num_covert(cn_str):
    try :
        if cn_str.isnumeric() :
            return int(cn_str)
        else :
            if '層' in cn_str :
                cn_str = re.sub('層', '', cn_str)
                num = 0
                unit = 1
                foolr_num = 0
                for index, cn_num in enumerate(reversed(cn_str)):
                    if cn_num in num_map :
                        num = num_map[cn_num]
                        foolr_num = foolr_num + num*unit
                    elif cn_num in unit_map :
                        unit = unit_map[cn_num]
                    else :
                        return foolr_num
            return foolr_num
    except ValueError :
        pass


# 建立臨時存放數字樓層的欄位['total_floor_num']，算出每筆紀錄的樓層數字
filter_temp['total_floor_num'] = filter_temp['總樓層數'].apply(lambda x: num_covert(x))


# 從filter_temp篩選出高於13層(含)的物件
condition_3 = filter_temp['total_floor_num']>=13
filter_a = filter_temp[(condition_3)]

# 最後刪除['total_floor_num']欄位另存成filter_a.csv
filter_a = filter_a.drop(['total_floor_num'], axis=1)
filter_a.to_csv('filter_a.csv' ,index=False, encoding='utf-8')




######################################
# filter_b 使用 pd.DataFrame from Dict
# 建立dict，其value為空，用來存放統計數值
filter_b_dict = {'總件數':[], '總車位數':[], '平均總價元':[],'平均車位總價元':[]}


# 1.計算總件數: 利用每筆紀錄的['編號']做計算數量的基準
# 其數值存入filter_b_dict['總件數']
total = df_all['編號'].count()
filter_b_dict['總件數'].append(total)

# 計算平均總價元：
# 先檢查資料型態，['總價元']、['車位總價元']發現為object
# 更改資料型態為float(用int會超過系統最大值)
df_all['總價元'] = df_all['總價元'].astype('float')
df_all['車位總價元'] = df_all['車位總價元'].astype('float')

# 2.計算平均總價元：利用['總價元']欄位做平均
# 其數值存入filter_b_dict['平均總價元']
means = df_all['總價元'].mean()
filter_b_dict['平均總價元'].append(means)

# 驗算
# 平均總價元 = 總價元/總件數 = df_all['總價元'].mean()
# print(df_all['總價元'].sum() / total)
# print(means)



# 3.平均車位總價元
# 其數值存入filter_b_dict['平均車位總價元']
means = df_all['車位總價元'].mean()
filter_b_dict['平均車位總價元'].append(means)


# 總車位數顯示於欄位['交易筆棟數']的內容中(ex.土地1建物1車位1)
# df_all['交易筆棟數'].unique()
# df_all['交易筆棟數'].value_counts()


# 利用函式find_parking_num取車位後的數值
def find_parking_num(trade_str):
    if '車位' in trade_str :
        parking_str = trade_str[trade_str.index('車位')+2:]
        return int(parking_str)

# 建立暫存欄位['parking_num'] 儲存車位數量
df_all['parking_num'] = df_all['交易筆棟數'].apply(lambda x: find_parking_num(x))

# 4.總車位數
# 加總['parking_num'] 可得總車位數
# 其數值存入filter_b_dict['總車位數']
filter_b_dict['總車位數'].append(df_all['parking_num'].sum())


# 觀察到幾筆紀錄有車位數目但車位價格卻為0的紀錄
# df_all['parking_num'].unique()
# df_all['parking_num'].value_counts()
# len(df_all[(df_all['parking_num']>0)&(df_all['車位總價元']=='0')])


# 驗算平均車位總價元 = 總車位價元/總車位數 = df_all['車位總價元'].mean()
# 若以總車位價元/總車位數，會因為有些紀錄是有車位卻沒車位價的數量而受影響(分母變大)
# 因此維持使用df_all['車位總價元'].mean()
# print(df_all['車位總價元'].sum() / df_all['parking_num'].sum())
# print(means)


# filter_b資料來源為filter_b_dict
# 另存成filter_b.csv
filter_b = pd.DataFrame.from_dict(filter_b_dict)
filter_b.to_csv('filter_b.csv', index=False, encoding='utf-8')




