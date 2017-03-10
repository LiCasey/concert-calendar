# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from datetime import datetime

def decodePage(htmlstr):
    data = []
    soup = BeautifulSoup(htmlstr)
    divl = soup.find_all('div','blog-post')

    for div in divl:
        dict = {}
        str = div.div.p.text.strip().split()
        dict['SHOWDATE'] = str[0].encode('utf-8')
        dict['VNAME'] = str[2].encode('utf-8')
        dict['PRODUCTNAME'] = div.find('h3','mt0').text.strip().encode('utf-8')
        data.append(dict)
    return data


def getZhongShanByMonth(month):
    if all_ZhongShanData==[]:
        all_ZhongShanData.extend(get_all_zhongshan())
    l = month.split('-')

    data_by_month = []
    for dataitem in all_ZhongShanData:
        if dataitem['SHOWDATE'].startswith(month):
            data_by_month.append(dataitem)

    return data_by_month


def get_all_zhongshan():
    # get page number and content of first page
    page = urllib2.urlopen('http://www.fcchbj.com/all_class')
    html = page.read()

    soup = BeautifulSoup(html)
    spanl = soup.find_all('span', 'paginator_page')
    maxPage = spanl.__len__()

    data = decodePage(html)

    # get rest pages
    for page_index in range(1, maxPage):
        page = urllib2.urlopen(
            'http://www.fcchbj.com/all_class/' + str(page_index + 1) + '/Show.showtime2/asc/all/0/0/0/0//')
        html = page.read()

        data.extend(decodePage(html))

    return data


all_ZhongShanData = get_all_zhongshan()

if __name__ =="__main__":
    data = getZhongShanByMonth('2017-05')
    print data
    pass