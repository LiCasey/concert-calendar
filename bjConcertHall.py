# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
import math

def getCount(year,month):
    data = "{strWhere:' 1=1  and (YEAR(SHOWDATE)="+str(year)+" or YEAR(SHOWDATE2)="+str(year)+\
           ")  and (MONTH(SHOWDATE)="+str(month)+" or MONTH(SHOWDATE2)="+str(month)+") '}"
    req = urllib2.Request('http://www.bjconcerthall.cn/AjaxService.asmx/GetPerformListHtmlCount')
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    u = urllib2.urlopen(req,data)
    return eval(u.readline())['d']


def getDataByMonthAndPage(year,month,page,count):
    data = "{strWhere:' 1=1  and (YEAR(SHOWDATE)=" + str(year) + " or YEAR(SHOWDATE2)=" \
           + str(year) + ")  and (MONTH(SHOWDATE)=" + str(month) + " or MONTH(SHOWDATE2)=" \
           + str(month) + ") ',orderby:'',PageNum:'"+str(page+1)+"',AllCount:'" + str(count) + "'}"
    req = urllib2.Request('http://www.bjconcerthall.cn/AjaxService.asmx/GetPerformListHtml')
    req.add_header('Host', 'www.bjconcerthall.cn')
    req.add_header('Origin', 'http://www.bjconcerthall.cn')
    req.add_header('Referer', 'http://www.bjconcerthall.cn/PerformList.aspx')
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    u = urllib2.urlopen(req, data)
    string = u.readline()
    htmldata = (eval(string)['d'])
    decoded = htmldata.decode("unicode_escape").encode("unicode_escape")

    # 解析html代码
    soup = BeautifulSoup(decoded)
    box = soup.find_all('div','yc_lb_box1')

    l = []
    for b in box:

        ul = b.find('ul')
        lil = ul.find_all('li')

        timestr = (lil[1].text).split()
        itemnum = timestr.__len__()/2
        for i in range(itemnum):
            dict = {}
            dict['VNAME'] = '北京音乐厅'
            dict['PRODUCTNAME'] = (lil[0].a.text).decode("string_escape")

            dict['SHOWDATE'] = (datetime.strptime(timestr[itemnum*i+1],"%Y/%m/%d")).strftime("%Y-%m-%d")
            l.append(dict)

    return l


def getBJConcertHallByMonth(month):
    temp = month.split('-')
    year = int(temp[0])
    month2 = int(temp[1])
    count = int(getCount(year,month2))

    maxPage = math.ceil(count/10.0)
    datalist = []
    for page_index in range(int(maxPage)):
        pagedata = getDataByMonthAndPage(year,month2,page_index,count)
        datalist.extend(pagedata)

    return datalist



if __name__=="__main__":
    print getBJConcertHallByMonth('2017-03')