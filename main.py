# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scraping(target_url: str):
    """
    概要: 指定されたurlからhtmlデータをスクレイピングする
    """
    r = requests.get(target_url)
    _html_data = BeautifulSoup(r.text, 'html.parser')
    return _html_data


def find_merchandise(_html_data):
    """
    スクレイピングで抽出したhtmlデータから、品名、価格を抽出する

    出力結果:
    [
     {'商品名': 'LCD works 【Exc+5】リコー GR1s QD シルバーポイント&シュート 35mm フィルムカメラ 日本製', '価格': '64,480 円'},
     {'商品名': '"LCD Works N MINT" Ricoh GR1s ポイントアンドシュート 35mm コンパクトフィルムカメラ"', '価格': '80,588 円'},
     {'商品名': 'Ricoh R1S 修理用 コンパクトフィルムカメラ', '価格': '23,272 円'}
    ]
    """
    productslist = []
    results = _html_data.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            '商品名': item.find('div', {'class': 's-item__title'}).text,
            '価格': item.find('span', {'class': 's-item__price'}).text,
        }
        productslist.append(product)
    return productslist


def find_search_results(_html_data):
    """
    検索結果の件数取得
    """
    _results = _html_data.find_all('h1', {'class': 'srp-controls__count-heading'})
    _menus = _results[0].find_all('span', {'class': 'BOLD'})
    return '検索結果: ' + _menus[0].text + '=' + _menus[1].text + '件'


# def find_menu_results(_html_data, target_menu_name: str):
def find_menu_results(_html_data):
    """
    左メニューの件数取得
    """
    results = _html_data.find_all('div', {'class': 'x-refine__select__svg'})
    menus = list(map(lambda x: [x.find('span', {'class': 'cbx x-refine__multi-select-cbx'}).text, x.find('span', {'class': 'x-refine__multi-select-histogram'}).text ], results))
    # menus = map(lambda x: {'メニュー名': x.find('span', {'class': 'cbx x-refine__multi-select-cbx'}).text, '件数': x.find('span', {'class': 'x-refine__multi-select-histogram'}).text }, results)
    print(list(menus))
    print(len(list(menus)))
    menus_dict = dict(menus)
    print(menus_dict)
    print(menus_dict.get('今すぐ落札'))
    # print(dict(menus))
    # l2 = {'今すぐ落札': '(22)', 'hoge': '1'}
    # print(len(l2))
    # print(l2.get('今すぐ落札'))
    # TODO: 今すぐ落札だけ抽出する
    return


def output_csv(file_name: str, _parsed_data: list):
    """
    概要:
    抽出したデータをCSVに書き出す

    parsed_dataの例:
    [
     {'商品名': 'LCD works 【Exc+5】リコー GR1s QD シルバーポイント&シュート 35mm フィルムカメラ 日本製', '価格': '64,480 円'},
     {'商品名': '"LCD Works N MINT" Ricoh GR1s ポイントアンドシュート 35mm コンパクトフィルムカメラ"', '価格': '80,588 円'},
     {'商品名': 'Ricoh R1S 修理用 コンパクトフィルムカメラ', '価格': '23,272 円'}
    ]
    """
    productsdf = pd.DataFrame(_parsed_data)
    productsdf.to_csv(file_name, encoding="utf-8_sig", index=False)
    print('CSV出力完了')
    return


def over_write_csv_head(file_name: str, text: str):
    with open(file_name) as reader:
        s = reader.read()
    s = text + '\n' + s
    with open(file_name, 'w', encoding='utf_8_sig') as writer:
        writer.write(s)


# ↓ 抽出したい画面のURL
url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=Ricoh+GR1s&_sacat=0&LH_TitleDesc=0&_odkw=Ricoh+GR1s&_osacat=0'
html_data = scraping(target_url=url)
# merchandise = find_merchandise(_html_data=html_data)
# search_results = find_search_results(_html_data=html_data)
find_menu_results(_html_data=html_data)
# output_csv(file_name='output.csv', _parsed_data=merchandise)
# over_write_csv_head(file_name='output.csv', text=search_results)

