import urllib.request, urllib.parse
import os
import datetime
import json
import pandas as pd


def search():
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    encText = urllib.parse.quote("몰스킨")
    url = "https://openapi.naver.com/v1/search/shop?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    print(response.read().decode('utf-8'))


def get_request_url(API_URL):
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    request = urllib.request.Request(API_URL)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    if response.getcode() == 200:
        print("[%s] Url Request Success" % datetime.datetime.now())
        return response.read().decode('UTF-8')
    else:
        print("[%s] Url Request Error" % datetime.datetime.now())
        return None


def get_search_result(api_node, search_text, start_num, disp_num):
    base = 'https://openapi.naver.com/v1/search'
    node = '/' + api_node + ".json"
    param_query = "?query=" + urllib.parse.quote(search_text)
    param_start = "&start=" + str(start_num)
    param_display = "&display=" + str(disp_num)
    url = base + node + param_query + param_start + param_display
    getting_data = get_request_url(url)
    if(getting_data == None):
        return None
    else:
        return json.loads(getting_data)


def delete_tag(input_string):
    input_string = input_string.replace("<b>", "")
    input_string = input_string.replace("</b>", "")
    return input_string


def get_fields(post):
    title = []
    link = []
    lprice = []
    hprice = []

    for each in post:
        title.append(delete_tag(each['title']))
        link.append(each['link'])
        lprice.append(each['lprice'])
        hprice.append(each['hprice'])

    result_pd = pd.DataFrame({'title': title, 'lprice': lprice, 'hprice': hprice, 'link': link}, columns=['title', 'lprice', 'hprice', 'link'])

    return result_pd


def search_shop():
    result_mol = []
    for n in range(1, 100, 10):
        search_result = get_search_result('shop', '몰스킨', n, 10)
        result_mol.append(get_fields(search_result['items']))
    result_mol = pd.concat(result_mol)
    result_mol = result_mol.reset_index(drop=True)
    result_mol['lprice'] = result_mol['lprice'].astype(float)
    result_mol['hprice'] = result_mol['hprice'].astype(float)
    writer = pd.ExcelWriter('data/molskin_in_naver_shop.xlsx', engine="xlsxwriter")
    result_mol.to_excel(writer, sheet_name="Sheet1")
    worksheet = writer.book
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:A', 4)
    worksheet.set_column('B:B', 60)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 50)

    worksheet.conditional_format('C2:C101', {'type': '3_color_scale'})

    writer.save()


search_shop()