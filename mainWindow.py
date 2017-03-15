# -*- coding: utf-8 -*-
import Tkinter
import time
from ttk import *
import tkFont
from collections import Counter
from datetime import datetime




def get_available_years(t):
    year_now = time.strftime('%Y', time.localtime(t))
    return [int(year_now)-1,int(year_now),int(year_now)+1]


def get_concert_data(year,month):
    concert_data = []

    # 获取国家大剧院数据
    import getNcpa
    s = '%d-%02d'%(year,month)
    ncpa_html = getNcpa.getNcpaBymonth(s)
    ncpa_data = eval(ncpa_html)

    for n in ncpa_data:
        n['VNAME'] = '国家大剧院'+n['VNAME']

    concert_data.extend(ncpa_data)

    # 获取北京音乐厅数据
    import bjConcertHall
    bj_hall_data = bjConcertHall.getBJConcertHallByMonth(s)
    concert_data.extend(bj_hall_data)

    import zhongShanHall
    zs_hall_data = zhongShanHall.getZhongShanByMonth(s)
    concert_data.extend(zs_hall_data)

    import tsinghua
    tsinghua_data = tsinghua.getTsinghuaByMonth(s)
    concert_data.extend(tsinghua_data)

    return concert_data


def init_calendar(year,month):
    import calendar
    concert_data = get_concert_data(year,month)
    c = calendar.Calendar(firstweekday=6)
    i = c.itermonthdays(year,month)

    daylist = []
    for d in concert_data:
        dateString = d['SHOWDATE']
        day = datetime.strptime(dateString,"%Y-%m-%d").day
        daylist.append(day)

    counter = Counter(daylist)

    return i, counter, concert_data


def refresh_calendar():
    year_now = int(time.strftime('%Y', time.localtime(time.time())))
    year = c1.current()+year_now-1
    month = c2.current()+1

    new_calendar, new_c_count, new_c_data = init_calendar(year,month)
    childs = calendar.children

    for d in childs.keys():
        childs[d].destroy()

    for c in range(7):
        Tkinter.Label(calendar, text=weekday[c], borderwidth=1).grid(row=0, column=c)
    for r in range(6):
        for c in range(7):
            try:
                day = new_calendar.next()
            except:
                pass

            if day == 0:
                continue
            createDayLabelFrame(calendar, year, month, day, new_c_count[day], r + 1, c, new_c_data, borderwidth=1, height=5)


def change_info_text(year,month, day,concert_data):
    dayLabel['text'] = '%d-%02d-%02d 演出信息'%(year,month,day)
    concert_info = get_concert_info_by_day('%d-%02d-%02d'%(year,month,day),concert_data)
    infoText.delete('1.0', Tkinter.END)
    infoText.insert('1.0', concert_info)


def createDayLabelFrame(master,year,month,day,count,row,column,concert_data,**kwargs):
    dlf = Tkinter.LabelFrame(master,kwargs)
    dlf.grid(row=row, column=column,sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)

    lb_day = Tkinter.Label(dlf,width=5,text=str(day),font=tkFont.Font(size=20))
    lb_day.pack()

    if count!=0:
        btn_count = Tkinter.Button(dlf,text=str(count)+'场演出',command=lambda: change_info_text(year,month,day,concert_data))
        btn_count.pack()

    # else:
    #     lb_empty = Tkinter.Label(dlf,height=1)
    #     lb_empty.pack()


def get_concert_info_by_day(dayString,concert_data):
    infoString = ''
    for dict in concert_data:
        if dict['SHOWDATE']==dayString:
            infoString+=dict['VNAME']+'：'+dict['PRODUCTNAME']+'\n\n'
    return infoString



if __name__=="__main__":
    weekday=['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
    t = time.time()
    year = int(time.strftime('%Y', time.localtime(t)))
    month = int(time.strftime('%m', time.localtime(t)))
    now_day = int(time.strftime('%d', time.localtime(t)))
    calendar_iteration, concert_count, concert_data = init_calendar(year,month)
    years = get_available_years(t)

    root = Tkinter.Tk(className="音乐会日历 v0.1")

    leftFrame = Tkinter.Frame(root)
    leftFrame.grid(row=0,column=0)
    rightFrame = Tkinter.Frame(root,padx=15)
    rightFrame.grid(row=0,column=1)

    dayLabel = Tkinter.Label(rightFrame, width=30, text=time.strftime('%Y-%m-%d 演出信息', time.localtime(t)),
                             font=tkFont.Font(size=20))
    dayLabel.pack()

    infoText = Tkinter.Text(rightFrame, width=40, font=tkFont.Font(size=11))
    infoText.pack()

    concert_info = get_concert_info_by_day(time.strftime('%Y-%m-%d', time.localtime(t)),concert_data)
    infoText.delete('1.0', Tkinter.END)
    infoText.insert('1.0', concert_info)

    options_labelPanel = Tkinter.LabelFrame(leftFrame,text="显示选项")
    options_labelPanel.pack()

    textdisplay='目前支持的音乐厅列表：国家大剧院、北京音乐厅、中山公园音乐堂、清华大学艺术教育中心'
    text_label = Tkinter.Label(options_labelPanel, text=textdisplay+'\n', justify=Tkinter.LEFT,wraplength=350,width=50,
                               fg="blue")
    text_label.pack()

    l1 = Tkinter.Label(options_labelPanel,text='选择日期')
    l1.pack(side=Tkinter.LEFT)

    c1 = Combobox(options_labelPanel,width=6)
    # years=[2016,2017,2018]
    c1['values'] = years
    c1['state'] = 'readonly'
    c1.current(1)
    c1.pack(side=Tkinter.LEFT)

    l2 = Tkinter.Label(options_labelPanel, text='年')
    l2.pack(side=Tkinter.LEFT)

    c2 = Combobox(options_labelPanel, width=4)
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    c2['values'] = months
    c2['state'] = 'readonly'
    c2.current(month-1)
    c2.pack(side=Tkinter.LEFT)

    l3 = Tkinter.Label(options_labelPanel, text='月')
    l3.pack(side=Tkinter.LEFT)

    bRefresh = Tkinter.Button(options_labelPanel, text="刷新", border=1, command=refresh_calendar)
    bRefresh.pack(side=Tkinter.LEFT)

    # # calendar title: month
    #
    # ft = tkFont.Font(size=20)
    # titlelabel = Tkinter.Label(root,text=str(year)+'-'+str(month),font=ft)
    # titlelabel.pack()

    # calendar
    calendar = Tkinter.Frame(leftFrame,height=480,width=600)
    calendar.grid_propagate(0)
    calendar.pack(fill="both",expand='yes')

    for c in range(7):
        Tkinter.Label(calendar, text=weekday[c], borderwidth=1).grid(row=0, column=c)
    for r in range(6):
        for c in range(7):
            try:
                day = calendar_iteration.next()
            except:
                pass
            if day == 0:
                continue
            createDayLabelFrame(calendar, year, month,day, concert_count[day],r+1, c,concert_data, borderwidth=1,height=5)

    root.mainloop()