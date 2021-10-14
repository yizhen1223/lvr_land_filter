# lvr_land_filter
使用Pandas套件進行內政部不動產買賣資料

## 下載資料
- 下載【內政部不動產時價登錄網 】中，位於【臺北市/新北市/桃園市/臺中市/高雄市】的【不動產買賣】資料
- 使用5個檔案：【 a_lvr_land_a 】【 b_lvr_land_a 】【 e_lvr_land_a 】【 f_lvr_land_a 】 【 h_lvr_land_a 】五份csv資料集

## 利用Pandas操作dataframe物件
### 使用 filter_plvr_land.py 完成 filter_a.csv 與 filter_b.csv 檔案任務
1) 5份csv分別建立成【df_a】【df_b】【df_e】【df_f】【df_h】dataframe物件
2) 將五個縣市物件合併成【df_all】
3) 計算【總樓層數】需轉換國文數字為阿拉伯數值：使用def num_covert
4) 計算【總車位數】需透過【交易筆棟數】找出車位數量
5) 觀察到有幾筆紀錄存在車位數目但車位價格卻為0，若成為【車位平均價元】的分母將影響結果，不予計入。

### 從【df_all】篩選/計算出以下結果，並分別輸出csv檔案
#### filter_a.csv 
- 【主要用途】為【住家用】
- 【建物型態】為【住宅大樓】
- 【總樓層數】需【大於等於十三層】
#### filter_b.csv
- 計算【總件數】
- 計算【總車位數】(透過交易筆棟數)
- 計算【平均總價元】
- 計算【平均車位總價元】(使用車位總價元的平均數)
