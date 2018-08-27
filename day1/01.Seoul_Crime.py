import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns

crime_raw_data = pd.read_csv('data/Crime_data.csv', encoding = 'euc-kr')
# crime_raw_data.head()
# crime_raw_data.info()
# crime_raw_data['죄종'].unique()
crime_raw_data = crime_raw_data[crime_raw_data['죄종'].notnull()]
crime_station = crime_raw_data.pivot_table(crime_raw_data, index = ['구분'], columns = ["죄종", "발생검거"], aggfunc = [np.sum])
crime_station.columns = crime_station.columns.droplevel([0, 1])
tmp = crime_station.columns.get_level_values(0) + crime_station.columns.get_level_values(1)
crime_station.columns = tmp
police_station_pos = {"강남": "강남구", "강동": "강동구", "강서": "강서구", "관악": "관악구", "구로": "구로구", "남대문": "중구", "금천": "금천구", "동작": '동작구', "노원": "노원구", "도봉": "도봉구", "혜화": "종로구", "광진": "광진구", "마포": "마포구", "방배": "서초구", "강북": "강북구", "서부": "은평구", "서대문": "서대문구", "서초": "서초구", "성동": "성동구", '성북': '성북구', '송파': '송파구', '수서': '강남구', '양천': '양천구', '영등포': '영등포구', '용산': '용산구', '은평': '은평구', '종로': '종로구', '종암': '성북구', '중랑': '중랑구', '중부': '중구', '동대문': '동대문구'}
tmp = [police_station_pos.get(idx) for idx, row in crime_station.iterrows()]
crime_station['구'] = tmp
crime_station.to_csv('data/crime_station.csv', sep=',', encoding='UTF-8')
crime_gu = pd.pivot_table(crime_station, index='구', aggfunc=np.sum)
target = ["강간검거율", "강도검거율", "살인검거율", "절도검거율", "폭력검거율"]
num = ["강간검거", "강도검거", "살인검거", "절도검거", "폭력검거"]
den = ["강간발생", "강도발생", "살인발생", "절도발생", "폭력발생"]
crime_gu[target] = crime_gu[num].div(crime_gu[den].values) * 100
crime_gu[crime_gu[target] > 100] = 100
crime_gu.rename(columns={"강간발생": "강간", "강도발생": "강도", "살인발생": "살인", "절도발생": "절도", "폭력발생": "폭력"}, inplace=True)
crime_gu = crime_gu.drop(columns=num)
col = ["강간", "강도", "살인", "절도", "폭력"]
crime_gu_norm = crime_gu[col] / crime_gu[col].max()
col2 = ["강간검거율", "강도검거율", "살인검거율", "절도검거율", "폭력검거율"]
crime_gu_norm[col2] = crime_gu[col2]
POP_Seoul = pd.read_csv('data/Seoul_pop.csv', index_col=1, encoding='UTF-8')
crime_gu_norm[['인구수']] = POP_Seoul[['인구수']]
crime_gu_norm['범죄'] = np.mean(crime_gu_norm[col], axis=1)
crime_gu_norm['검거'] = np.mean(crime_gu_norm[col2], axis=1)
print(crime_gu_norm.head())
target_col = ["강간", "강도", "살인", "절도", "폭력", "범죄"]
crime_gu_sort = crime_gu_norm.sort_values(by='범죄', ascending=False)
plt.rcParams['axes.unicode_minus'] = False
f_path = '/Library/Fonts/AppleGothic.ttf'
font_name = font_manager.FontProperties(fname=f_path).get_name()
rc('font', family=font_name)
plt.figure(figsize=(10,10))
sns.heatmap(crime_gu_sort[target_col], annot=True, fmt='f', linewidths=5, cmap='RdPu')
plt.title("범죄 비율")
plt.show()
crime_gu_norm.to_csv('data/crime_seoul_final.csv', sep=',', encoding='UTF-8')