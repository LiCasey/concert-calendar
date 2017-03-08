# -*- coding: utf-8 -*-
import Tkinter
import time
from ttk import *
import tkFont




def get_available_years(t):
    year_now = time.strftime('%Y', time.localtime(t))
    return [int(year_now)-1,int(year_now),int(year_now)+1]


def get_concert_data(year,month):
    pass


def init_calendar(year,month):
    import calendar
    concert_data = get_concert_data(year,month)
    c = calendar.Calendar(firstweekday=6)
    i = c.itermonthdays(year,month)

    return i


def refresh_calendar():
    year_now = int(time.strftime('%Y', time.localtime(time.time())))
    year = c1.current()+year_now-1
    month = c2.current()+1

    new_calendar = init_calendar(year,month)
    childs = calendar.children

    for d in childs.keys():
        childs[d].destroy()

    for c in range(7):
        Tkinter.Label(calendar, text=weekday[c], borderwidth=1).grid(row=0, column=c)
    for r in range(6):
        for c in range(7):
            day = new_calendar.next()
            if day == 0:
                continue
            Tkinter.Button(calendar, text=day, borderwidth=1,width=5,height=2).grid(row=r+1, column=c)

    pass

if __name__=="__main__":
    weekday=['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
    t = time.time()
    year = int(time.strftime('%Y', time.localtime(t)))
    month = int(time.strftime('%m', time.localtime(t)))
    calendar_iteration = init_calendar(year,month)
    years = get_available_years(t)

    root = Tkinter.Tk(className="音乐会日历 v1.0")

    options_labelPanel = Tkinter.LabelFrame(root,text="显示选项")
    options_labelPanel.pack()

    textdisplay='目前支持的音乐厅列表：国家大剧院'
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

    bRefresh = Tkinter.Button(options_labelPanel,text="刷新",border=1,command=refresh_calendar)
    bRefresh.pack(side=Tkinter.LEFT)

    # # calendar title: month
    #
    # ft = tkFont.Font(size=20)
    # titlelabel = Tkinter.Label(root,text=str(year)+'-'+str(month),font=ft)
    # titlelabel.pack()

    # calendar
    calendar = Tkinter.LabelFrame(root)
    calendar.pack(side=Tkinter.BOTTOM)

    for c in range(7):
        Tkinter.Label(calendar, text=weekday[c], borderwidth=1).grid(row=0, column=c)
    for r in range(5):
        for c in range(7):
            day = calendar_iteration.next()
            if day == 0:
                continue
            Tkinter.Button(calendar, text=day, borderwidth=1,width=5,height=2).grid(row=r+1, column=c)

    root.mainloop()