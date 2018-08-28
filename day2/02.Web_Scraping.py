from bs4 import BeautifulSoup
from urllib.request import urlopen
import re, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = 'https://movie.naver.com/movie/running/current.nhn'
page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")

title = soup.find_all('dt', 'tit')
info = soup.find_all('span', 'num')
title_list = []
for x in range(10):
    tmp = [title[x].find('a').get_text(), title[x].find('span').get_text(), info[2 * x].get_text(), info[2 * x + 1].get_text()]
    title_list.append(tmp)

print("="*10, "현재 상영중인 영화 TOP 10", "="*10)
for each_movie in title_list:
    print("제목:", each_movie[0], each_movie[1], "평점:", each_movie[2], "/ 10", "예매율:", each_movie[3], "%")

print('\n')
print("="*10, "현재 IT 책 TOP 10", "="*10)

url = 'https://book.naver.com/category/index.nhn?cate_code=280020&tab=top100&list_type=list&sort_type=salecount'
page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")

title_list = soup.find_all('a', 'N=a:bta.title')
author_list = soup.find_all('a', 'txt_name N=a:bta.author')
star_list = soup.find_all('dd', 'txt_desc')
date_list = soup.find_all('dd', 'txt_block')
score = []
date = []
title = []
author = []

for x in star_list[:10]:
    result = re.search("\d.\d", x.get_text())
    score.append(result.group())

for x in date_list[:10]:
    result = re.search("\d+.\d+.\d+", x.get_text())
    date.append(result.group())

for x in title_list[:10]:
    title.append(x.get_text())

for x in author_list[:10]:
    author.append(x.get_text())


bestseller = pd.DataFrame({'책제목': title, '저자': author, '평점': score, '출판일': date})

print(bestseller.to_string(justify='left', index=True))


url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date='
date = pd.date_range('2018.07.01', periods=58, freq='D')

movie_date = []
movie_name = []
movie_point = []

print("="*10, "영화 크롤링 중", "="*10)
for x in date:
    print(x.strftime("%Y%m%d"))
    page = urlopen(url + x.strftime("%Y%m%d"))
    soup = BeautifulSoup(page, 'html.parser')
    for y in range(len(soup.find_all('td', 'point'))):
        movie_date.append(x)
    movie_name.extend([each.a.string for each in soup.find_all('div', 'tit5')])
    movie_point.extend([each.string for each in soup.find_all('td', 'point')])


print()

movie = pd.DataFrame({'date': movie_date, 'name': movie_name, 'point': movie_point})
movie['point'] = movie['point'].astype(float)
movie.to_csv('data/naver_movie_raw_data.csv', sep=',', encoding='utf-8', index_label=False)

print("="*10, "영화 정보 저장 완료", "="*10)
print()
print("="*10, "영화 정보 불러오는 중", "="*10)
movie = pd.read_csv("data/naver_movie_raw_data.csv", index_col=0)
movie_unique = pd.pivot_table(movie, index=['name'], aggfunc=np.sum)

movie_best = movie_unique.sort_values(by='point', ascending=False)
print(movie_best.head())

plt.figure(figsize=(12, 8))
plt.plot(movie.query('name == ["너의 결혼식"]')['date'], movie.query('name == ["너의 결혼식"]')['point'])
plt.legend(loc='best')
plt.axis([0, 10, 0, 10])
plt.grid()
plt.show()

time.sleep(10)
plt.close()

movie_pivot = movie.pivot('date', 'name', 'point')
movie_pivot.to_excel('data/04_movie_pivot.xlsx')

