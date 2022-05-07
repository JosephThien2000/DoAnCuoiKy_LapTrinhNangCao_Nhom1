from Core.webCrawler_Texts import *
from Core.webCrawler_Images import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import os
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from calendar import month_name
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import requests # cho phép bạn gửi HTTP thông qua Python
import re
import os # thư viện này cho phép thao tác với các thư mục và tệp
from XuLyFile import *
import pandas as pd


# url = "https://www.nasa.gov/topics/"
# url = "https://www.nasa.gov/topics/moon-to-mars/images/"

# path = 'D:/University/Lập trình nâng cao/file_code/Đồ án cuối kỳ/'
# path = "C:/Users/Admin/Desktop/"
path_data = os.path.join(path, "data")
condition = True
turn_on = True
lst_topics = []


class MainApp(Frame):
    
    # Constuctor
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):

        global lst_topics

        # main frame
        self.pack(fill=BOTH, expand=True)
        self.frm_main = Frame(self, relief=RAISED, borderwidth=1)
        self.frm_main.pack(fill=BOTH, expand=True)

        # frame 1
        self.frm_1 = Frame(self.frm_main, borderwidth=1)
        self.frm_1.pack(fill=X)

        # label and entry frame
        self.frm_label_entry = Frame(self.frm_1, borderwidth=1)
        self.frm_label_entry.grid(row=0, column=0, sticky=NSEW)
        self.lbl_url = Label(self.frm_label_entry, text='URL:')
        self.lbl_url.pack(side=LEFT, padx=10, pady=10)
        self.stringURL = StringVar()
        self.ent_url = Entry(self.frm_label_entry, width=100, bd=3, textvariable=self.stringURL)
        self.ent_url.pack(side=LEFT, padx=10, pady=10)

        # buttons frame
        self.btn_frame = Frame(self.frm_1, borderwidth=1)
        self.btn_frame.grid(row=1, column=0, sticky=NSEW)
        self.btn_frame.columnconfigure([0,1], weight=1)
        self.btn_text = Button(self.btn_frame, text='Text', bd=3, command=self.text_Button, padx=15)
        self.btn_text.grid(row=0, column=0)
        self.btn_image = Button(self.btn_frame, text='Image', bd=3, padx=10, command=self.image_Button)
        self.btn_image.grid(row=0, column=1)

        # frame 2
        self.frm_2 = Frame(self.frm_main, borderwidth=1)
        self.frm_2.pack(fill=X, padx=10, pady=10)
        self.frm_2.columnconfigure([0,1], weight=1)
  
        # listbox
        self.listbox = Listbox(self.frm_2, width=70, bd=3, height=22) # , selectmode=MULTIPLE
        self.listbox.grid(row=0, column=0, sticky=NSEW)

        # Scroll bar
        self.scrollbar1 = ttk.Scrollbar(
            master = self.frm_2
            , orient=VERTICAL
            , command=self.listbox.yview
        )
        self.scrollbar1.grid(sticky="NSE", row=0, column=0)
        self.listbox['yscrollcommand'] = self.scrollbar1.set

        self.scrollbar2 = ttk.Scrollbar(
            master = self.frm_2
            , orient=HORIZONTAL
            , command=self.listbox.xview
        )
        self.scrollbar2.grid(sticky="SWE", row=1, column=0)
        self.listbox['xscrollcommand'] = self.scrollbar2.set

        # # combobox and buttons frames
        self.cbx_btn_frame = Frame(self.frm_2, borderwidth=1)
        self.cbx_btn_frame.grid(row=0, column=1, sticky=NSEW)
        # self.combo = ttk.Combobox(self.cbx_btn_frame, values=lst_topics, state='readonly')
        # self.combo.set("Pick a topic")
        # self.combo.pack(padx=10, pady=20, fill=BOTH)

        # def filter(event):
        #     self.combo.delete(0, END)
        #     for topic in lst_topics:
        #         self.listbox.insert(END, topic)

        # self.combo.bind('<<ComboboxSelected>>', filter)

        # self.btn_show = Button(self.cbx_btn_frame, text='Show', bd=3, command=self.open_window)
        # self.btn_show.pack(padx=10, pady=20, fill=BOTH)

        self.btn_download = Button(self.cbx_btn_frame, text='Download', bd=3, command=self.download_Button)
        self.btn_download.pack(padx=10, pady=50, fill=BOTH)

        self.btn_select_all = Button(self.cbx_btn_frame, text='Select all', bd=3, command=self.select_All)
        self.btn_select_all.pack(padx=10, pady=50, fill=BOTH)
        self.listbox.event_generate("<<ListboxSelect>>")

        self.btn_close = Button(self.cbx_btn_frame, text='Close', bd=3, command=self.quit)
        self.btn_close.pack(padx=10, pady=50, fill=BOTH)

    def show_Listbox_t(self):
        # arrItems = DocFile()
        self.listbox.delete(0, END)
        for topic in topics: 
            self.listbox.insert(END, topic)
            topic_name = topic.split('/')[-1]
            lst_topics.append(topic_name)
        # for topic in lst_topics:
        #     print(topic)
    
    def show_Listbox_i(self):
        self.listbox.delete(0, END)
        for image in images:
            self.listbox.insert(END, image)

    def text_Button(self):
        global turn_on
        turn_on = True
        try:
            url = self.stringURL.get()
            get_wb_t(url)
            crawl_texts()
            self.show_Listbox_t()
        except:
            text = self.stringURL.get()
            url = os.path.join("https://www.nasa.gov/", text)
            get_wb_t(url)
            crawl_texts()
            self.show_Listbox_t()

    def image_Button(self):
        global turn_on
        turn_on = False
        try:
            url = self.stringURL.get()
            get_wb_i(url)
            crawl_images()
            self.show_Listbox_i()
        except:
            text = self.stringURL.get()
            url = os.path.join("https://www.nasa.gov/topics/moon-to-mars/", text)
            get_wb_i(url)
            crawl_images()
            self.show_Listbox_i()

    def select_All(self):
        global condition

        if condition:
            self.listbox.select_set(0, END)
            condition = False
        else:
            self.listbox.select_clear(0, END)
            condition = True
    
    def download_Button(self):

        global turn_on

        if turn_on==False:
            for i in self.listbox.curselection():
                # print(self.listbox.get(i))
                download_image(self.listbox.get(i))
        else:
            for i in self.listbox.curselection():
                # print(self.listbox.get(i))
                download_texts(self.listbox.get(i))
    
    # def show_Button(self):
    #     try:
    #         for i in self.listbox.curselection():
    #             # print(self.listbox.get(i))
    #             urllib.request.urlretrieve(self.listbox.get(i), self.listbox.get(i).split('/')[-1])
    #             img = Image.open(self.listbox.get(i))
    #             img.show()
    #     except: pass

    
    # def open_window(self):
    #     self.new_window = Show_Window(self)

    #     self.listbox_new_window = Listbox(self.new_window, bd=3, height=32, width=115, selectmode=MULTIPLE)
    #     self.listbox_new_window.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    #     self.listbox_new_window.bind('<<ListboxSelect>>', self.show_Button())

    #     self.btn_left = Button(self.new_window, bd=3, padx=10, pady=10, text="\N{LEFTWARDS ARROW}")
    #     self.btn_left.grid(row=0, column=0, sticky="ew")

    #     self.btn_right = Button(self.new_window, bd=3, padx=10, pady=10, text="\N{RIGHTWARDS ARROW}")
    #     self.btn_right.grid(row=0, column=2, sticky="ew")

    #     self.ent_number = Entry(self.new_window, bd=3, width=5)
    #     self.ent_number.grid(row=1, column=1, sticky="s")

    #     self.scrollbar_up = Scrollbar(self.new_window, orient="vertical", command=self.listbox_new_window.yview)
    #     self.scrollbar_up.grid(row=0, column=1, sticky="nse")

    #     self.scrollbar_down = Scrollbar(self.new_window, orient="horizontal", command=self.listbox_new_window.xview)
    #     self.scrollbar_down.grid(row=1, column=1, sticky="ewn")

    #     self.listbox_new_window.config(yscrollcommand=self.scrollbar_up.set)
    #     self.listbox_new_window.config(xscrollcommand=self.scrollbar_down.set)

    #     self.btn_left.config(command=lambda: self.move_left(self.listbox_new_window))
    #     self.btn_right.config(command=lambda: self.move_right(self.listbox_new_window))


# class Show_Window(Toplevel):

#     def __init__(self, parent):
#         Toplevel.__init__(self, parent)
#         self.title("Show Data")
#         self.geometry("800x600")
#         self.resizable(False, False)
#         self.parent = parent
#         self.rowconfigure([0,1], weight=1)
#         self.columnconfigure([0,1,2], weight=1)

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title("Hack NASA in a nutshell")
        self.geometry("700x500+0+0")
        self.resizable(False, False)

def main():
    root = Root()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
   main()
