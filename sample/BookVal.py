
import urllib.robotparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import *
from tkinter import scrolledtext

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


def scraping(keywd):
    option = Options()
    # Chromeの通知バーを表示しない
    option.add_argument("--disable-infobars")
    # 最大化で起動
    option.add_argument("--start-maximized")
    # 拡張機能を無効化
    option.add_argument("--disable-extensions")
    # ポップアップ通知を、1：許可、2：ブロック
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    # ECサイトURLを指定
    urllist = ["https://shopping.yahoo.co.jp/",
        "https://www.bookoffonline.co.jp/",
        "https://www.suruga-ya.jp/"]

    url = "https://www.bookoffonline.co.jp/"
    # 利用制限のチェック
    robot_check(url)

    #driver = webdriver.Chrome(options=option, executable_path = cdriverpath)
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #ショッピングサイトを開く
    driver.get(url)
    # 検索キーワードを指定
    elem_keyword = driver.find_element(By.NAME,"keyword")
    # 検索キーワードを入力
    elem_keyword.send_keys(keywd)
    # 検索ボタンを押す
    driver.find_element(By.ID,"zsSearchFormButton").click()
    
    
    # 検索結果のページのURLを取得
    cur_url = driver.current_url
    # 検索結果のURLのHTMLを取得
    r_html = requests.get(cur_url)

    soup = BeautifulSoup(r_html.content, 'html.parser')
    # "LoopList__item"のテキスト部分を取り出す
    for i in soup.find_all(class_="mainprice"):
        txt.insert("end",i.text.replace(",",""))
        txt.insert("end","\n")
    for i in soup.find_all(class_="itemttl"):
        txt.insert("end",i.text)
        txt.insert("end","\n")


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

srcbtn = tk.Button(root,
    text="検索",
    command = lambda:scraping(kwtxt.get()),
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