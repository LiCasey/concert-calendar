# -*- coding: utf-8 -*-
import urllib2

def getTsinghuaByMonth(month):
    url = 'http://www.hall.tsinghua.edu.cn/info/calendar/list/json'
    data = 'date='+month+'&channelId=153%2C154%2C155%2C156%2C159'
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    u = urllib2.urlopen(req, data)
    json = eval(u.read())

    if json['infos'] is None:
        return []
    data = json['infos']

    for item in data:
        item['VNAME'] = '清华大学'+item.pop('infoParamMap')['dz']['value']
        item['PRODUCTNAME'] = item.pop('title')
        item['SHOWDATE'] = item.pop('pubtime')[:10]
    return data

if __name__=='__main__':
    print getTsinghuaByMonth('2017-03')