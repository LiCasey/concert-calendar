def getHtml(url):
    import urllib2
    page = urllib2.urlopen(url)
    html = page.read()
    return html

def getNcpaBymonth(month):
    print 'method: getNcpaBymonth'
    url = "http://www.chncpa.org/was5/web/search?channelid=263964&ycid=73&month="+month
    html = getHtml(url)

    return html

if __name__=='__main__':
    html = getNcpaBymonth('2017-03')
    print html
