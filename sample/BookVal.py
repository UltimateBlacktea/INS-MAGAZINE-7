
import urllib.robotparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

class website:
    def __init__(self,url,ikwbar,kwbar,ikwbtn,kwbtn,itemcn,iitemval,itemval,iitemname,itemname,itemurl,name):
        self.url = url
        self.ikwbar = ikwbar
        self.kwbar = kwbar
        self.ikwbtn = ikwbtn
        self.kwbtn = kwbtn
        self.itemcn = itemcn
        self.iitemval = iitemval
        self.itemval = itemval
        self.iitemname = iitemname
        self.itemname = itemname
        self.itemurl = itemurl
        self.name = name

bookoff = website("https://www.bookoffonline.co.jp/",
    By.NAME,
    "keyword",
    By.ID,
    "zsSearchFormButton",
    "list_group",
    By.CLASS_NAME,
    "mainprice",
    By.CLASS_NAME,
    "itemttl",
    "itemttl",
    "ブックオフオンライン")

surugaya = website("https://www.suruga-ya.jp/",
    By.NAME,
    "search_word",
    By.ID,
    "btn-search",
    "item",
    By.CLASS_NAME,
    "text-red",
    By.CLASS_NAME,
    "title",
    "title",
    "駿河屋")

mottainai = website("https://www.mottainaihonpo.com/shop/",
    By.NAME,
    "query",
    By.NAME,
    "submit",
    "searchresult",
    By.CLASS_NAME,
    "content",
    By.CLASS_NAME,
    "title",
    "title",
    "もったいない本舗")

amazon = website("https://www.amazon.co.jp/",
    By.NAME,
    "field-keywords",
    By.ID,
    "nav-search-submit-button",
    "a-section a-spacing-base",
    By.CLASS_NAME,
    "a-price-whole",
    By.CLASS_NAME,
    "a-size-base-plus a-color-base a-text-normal",
    "a-size-mini a-spacing-none a-color-base s-line-clamp-4",
    "Amazon")

def robot_check(url):

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "robots.txt")
    rp.read()

    # クローリングへの指示書があるか
    req_rate = rp.request_rate("*")
    if req_rate is None:
        print(url,":","クローリングへの指示書はありません")

        # URLの取得が許可されているかを確認
        req_URL = rp.can_fetch("*", url)
        if req_URL == True:
            print(url,":","URLの取得も許可されています。これよりスクレイピングを開始します。")
        else:
            print(url,":","URLの取得が許可されていません。スクレイピングを中止します")
    else:
        print(url,":","クローリングへの指示書があります。問題がないか、利用規約を確認ください。")

def output(soup,url,itemcn,val,name,itemurl):
    maxsrc = int(cb.get())

    if soup.find(class_ = itemcn) == None:
        txt.insert("end","商品が検索できませんでした\n")
    else:
        """
        for i,j,k in zip(soup.find_all(class_=val),soup.find_all(class_ = name),range(maxsrc)):
            txt.insert("end",j.text.replace("\n",""))
            txt.insert("end","\n")
            txt.insert("end",i.text.replace("\n",""))
            txt.insert("end","\n")
        """
        for i,j in zip(soup.find_all(class_ = itemcn),range(maxsrc)):
            txt.insert("end",i.find(class_ = name).text.replace("\n",""))
            txt.insert("end","\n")
            if i.find(class_ = val) == None:
                txt.insert("end","価格が取得できませんでした\n")
            else:
                txt.insert("end",i.find(class_ = val).text.replace("\n",""))
                txt.insert("end","\n")
            if i.find(class_ = itemurl).find("a").get("href") == None:
                txt.insert("end","URLが取得できませんでした\n")
            else:
                iurl = i.find(class_ = itemurl).find("a").get("href")
                if url == "https://www.amazon.co.jp/":iurl = iurl[iurl.find("/dp/")+1:]
                if url == "https://www.suruga-ya.jp/":
                    txt.insert("end",iurl)
                else:
                    txt.insert("end",url+iurl)
                txt.insert("end","\n")
            txt.insert("end","\n")



def scraping(site,keywd):
    option = Options()
    # Chromeの通知バーを表示しない
    option.add_argument("--disable-infobars")
    # 最大化で起動
    option.add_argument("--start-maximized")
    # 拡張機能を無効化
    option.add_argument("--disable-extensions")
    # ポップアップ通知を、1：許可、2：ブロック
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    url = site.url
    # 利用制限のチェック
    robot_check(url)

    #driver = webdriver.Chrome(options=option, executable_path = cdriverpath)
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #ショッピングサイトを開く
    driver.get(url)
    # 検索キーワードを指定
    elem_keyword = driver.find_element(site.ikwbar,site.kwbar)
    # 検索キーワードを入力
    elem_keyword.send_keys(keywd)
    # 検索ボタンを押す
    driver.find_element(site.ikwbtn,site.kwbtn).click()
    
    
    # 検索結果のページのURLを取得
    cur_url = driver.current_url
    # 検索結果のURLのHTMLを取得
    r_html = requests.get(cur_url)

    soup = BeautifulSoup(r_html.content, 'html.parser')
    
    txt.insert("end",site.name)
    txt.insert("end","\n")
    output(soup,site.url,site.itemcn,site.itemval,site.itemname,site.itemurl)
    txt.insert("end","\n")

def query_scraping(keywd):
    txt.delete('1.0', 'end')
    if kwtxt.get() == "":
        txt.insert("end","キーワードが入力されていません\n")
        return
    site_list = [bookoff,surugaya,mottainai,amazon]
    chkbool = [Val1.get(),Val2.get(),Val3.get(),Val4.get()]
    scrape_list = [site_list[i] for i in range(len(site_list)) if chkbool[i]]
    for site in scrape_list:
        scraping(site,keywd)

root = tk.Tk()
root.title("お値段サーチ")
root.resizable(True,True)
root.geometry("960x540")

label11 = tk.Label(root,
    text="検索ワードを入力",
    font=("Yu Gothic UI Semibold",16))
label11.pack(side = tk.TOP)

kwd = StringVar()
kwtxt = tk.Entry(root,
    textvariable = kwd,
    width = 1920,
    borderwidth = 5,
    font=("Yu Gothic UI Semibold",16))
kwtxt.pack(side = tk.TOP)

frame1 = ttk.Frame(root,padding=10)
frame1.pack()

Val1 = tk.BooleanVar()
Val2 = tk.BooleanVar()
Val3 = tk.BooleanVar()
Val4 = tk.BooleanVar()

Val1.set(True)
Val2.set(True)
Val3.set(True)
Val4.set(True)

CheckBox1 = tk.Checkbutton(frame1,text=u"ブックオフオンライン", variable=Val1)
CheckBox1.pack(side = tk.LEFT)
CheckBox2 = tk.Checkbutton(frame1,text=u"駿河屋", variable=Val2)
CheckBox2.pack(side = tk.LEFT)
CheckBox3 = tk.Checkbutton(frame1,text=u"もったいない本舗", variable=Val3)
CheckBox3.pack(side = tk.LEFT)
CheckBox4 = tk.Checkbutton(frame1,text=u"Amazon", variable=Val4)
CheckBox4.pack(side = tk.LEFT)

label3 = tk.Label(frame1,
    text="      検索数：",
    font=("Yu Gothic UI Semibold",12))
label3.pack(side = tk.LEFT)

# Combobox
srcnum = [1,3,5,10,15,20]
v = StringVar()
cb = ttk.Combobox(
    frame1, textvariable=v, 
    values=srcnum, width=10)
cb.set(srcnum[0])
cb.bind(
    '<<ComboboxSelected>>', 
    lambda e: print('v=%s' % v.get()))
cb.pack(side = tk.RIGHT)

srcbtn = tk.Button(root,
    text="検索",
    command = lambda:query_scraping(kwtxt.get()),
    borderwidth = 5,
    font = ("Yu Gothic UI Semibold",20))
srcbtn.pack(side = tk.TOP)

label2 = tk.Label(root,
    text="以下に結果が出力されます",
    font=("Yu Gothic UI Semibold",16))
label2.pack(side = tk.TOP)

txt = tk.scrolledtext.ScrolledText(
    root,
    height = 1080,
    width = 1920,
    borderwidth = 5,
    font = ("Yu Gothic UI Semibold",16))
txt.pack(side = tk.TOP)

root.mainloop()