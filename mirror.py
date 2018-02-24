#!/usr/bin/python3
from tkinter import *
import locale
import threading
import time
import urllib
import urllib.parse
import urllib.request
import json
import requests
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = '' 
time_format = 12
date_format = "%b %d, %Y"
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18


@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


class UserDetails(Frame):
    def printUser(self, user):
        #print(user)
        self.name = Label(self, font=('Helvetica', medium_text_size), text=user.get('name'), fg="white", bg="black")
        self.name.pack(side=TOP, anchor=W)
        self.country = Label(self, font=('Helvetica', small_text_size), text=user.get('country'), fg="white", bg="black")
        self.country.pack(side=TOP, anchor=W)
    def getJSON(self):
        user = json.load(open('user_details.json'))
        return user

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.name = ''
        self.country = ''
        #TODO get from http prot
        self.printUser(self.getJSON())



class Temperature(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label

        self.temperature = ''
        self.temp = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.temp.pack(side=TOP, anchor=E)
        #TODO setup temperature setup calls
        self.tick()

    def tick(self):
        self.temp.config(text='27°C')
        #update the UI from yahoo
        self.temp.after(200, self.tick)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

class Notification(Frame):
    def printUser(self, user):
        #print(user)
        self.app = Label(self, font=('Helvetica', medium_text_size), text=user.get('app'), fg="white", bg="black")
        self.app.pack(side=TOP, anchor=W)
        self.msg = Label(self, font=('Helvetica', small_text_size), text=user.get('msg'), fg="white", bg="black")
        self.msg.pack(side=TOP, anchor=W)
        self.app2 = Label(self, font=('Helvetica', medium_text_size), text=user.get('app2'), fg="white", bg="black")
        self.app2.pack(side=TOP, anchor=W)
        self.msg2 = Label(self, font=('Helvetica', small_text_size), text=user.get('msg2'), fg="white", bg="black")
        self.msg2.pack(side=TOP, anchor=W)
        self.app3 = Label(self, font=('Helvetica', medium_text_size), text=user.get('app3'), fg="white", bg="black")
        self.app3.pack(side=TOP, anchor=W)
        self.msg3 = Label(self, font=('Helvetica', small_text_size), text=user.get('msg3'), fg="white", bg="black")
        self.msg3.pack(side=TOP, anchor=W)

        
    def getJSON(self):
        user = json.load(open('nots.json'))
        return user

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        #TODO get from http prot
        self.printUser(self.getJSON())
        


class  MirrorUI:
    def __init__(self):
        self.root = Tk()
        self.root.configure(background='black')
        frame = Frame(self.root, background='black')
        frame.pack(fill=BOTH, side=LEFT, expand=True)
        clock = Clock(frame)
        clock.pack(side=TOP, anchor=N, padx=50, pady=60)

        self.temperature = Temperature(frame)
        self.temperature.pack(side=TOP, anchor=NE, padx=100, pady=60)

        userDetails = UserDetails(frame)
        userDetails.pack(side=BOTTOM, anchor=S, padx=25, pady=25)

        noti = Notification(frame)
        noti.pack(side=LEFT, anchor=N, padx=25, pady=25)


    def fullscreen(self, state):
        self.root.attributes('-fullscreen', state)

    def show(self):
        self.root.mainloop()


if __name__ == '__main__':
    mirror = MirrorUI()
    mirror.fullscreen(True)
    mirror.show()
