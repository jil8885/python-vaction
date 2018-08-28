from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from urllib.parse import urljoin
import re, time

url_base = 'http://www.chicagomag.com'
url_sub = '/Chicago-Magazine/November-2012/Best-Sandwiches-Chicago/'
url = url_base + url_sub

html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
menu_list = soup.find_all('div', 'sammy')
rank = []
main_menu = []
cafe_name = []
url_add = []
for tmp in menu_list:
    menu = tmp.find('b').string
    num = tmp.get_text().split('\n')[1].strip()
    store = tmp.get_text().split('\n')[3].strip()
    link = urljoin(url_base, tmp.find('a')['href'])
    rank.append(num)
    main_menu.append(menu)
    cafe_name.append(store)
    url_add.append(link)

data = {'Rank': rank, 'Menu': main_menu, 'Cafe': cafe_name, 'URL': url_add}
df = pd.DataFrame(data)
df.to_csv("data/04_best_sandwitch_list_chicago.csv", sep=',', encoding='UTF-8')

prices = []
address = []
for idx, row in df.iterrows():
    html = urlopen(row['URL'])
    soup_tmp = BeautifulSoup(html, 'lxml')

    gettings = soup_tmp.find('p', 'addy').get_text()
    price_tmp = re.split('.,', gettings)[0]
    tmp = re.search('\$\d+\.(\d+)?', price_tmp).group()
    prices.append(tmp)
    end = re.search('\$\d+\.(\d+)?',price_tmp).end()
    address.append(price_tmp[end + 1:])

    print(row['Rank'], '/', '50')

df['Price'] = prices
df['Address'] = address

df = df.loc[:, ['Rank', 'Cafe', 'Menu', 'Price', 'Address']]
df.set_index('Rank', inplace=True)
df.to_csv("data/04_best_sandwitch_list_chicago2.csv", sep=',', encoding='UTF-8')
