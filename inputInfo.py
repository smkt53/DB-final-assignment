# 予約情報を入力するためだけのプログラム
# 名前と電話番号を入力する
# 予約ボタンを押すと10秒後に自動的にウィンドウが閉じる

import tkinter as tk
from tkinter import ttk
import dbControl as db
import re
import datetime

# 選択されたテーブル、日付、開始時間、人数を受け取り、名前と電話番号を入力する画面を表示する
def input_flow(table_state, date, startTime, people, way):

    print(table_state)
    print(date)
    print(startTime)
    print(people)
    print(way)


    caution_label = tk.Label(text = "", font = ("Helvetica", 30), foreground="red")

    # 予約希望日時と人数を表示

    # テーブルは配列で受け取る
    # 1が選択されたテーブルである
    tableNo = None
    for i in range(0, 8):
        if table_state[i] == 1:
            if(tableNo == None):
                tableNo = str(i + 1)
            else:
                tableNo += ", "+ str(i + 1)
            

    people_label = tk.Label(text = f"予約人数", font = ("Helvetica", 20))
    people_label.place(x = 100, y = 100)
    people_label2 = tk.Label(text = f": {people}人", font = ("Helvetica", 20))
    people_label2.place(x = 300, y = 100)
    date_label = tk.Label(text = f"希望日", font = ("Helvetica", 20))
    date_label.place(x = 100, y = 175)
    date_label2 = tk.Label(text = f": {date}", font = ("Helvetica", 20))
    date_label2.place(x = 300, y = 175)
    time_label = tk.Label(text = f"希望時間", font = ("Helvetica", 20))
    time_label.place(x = 100, y = 250)
    time_label2 = tk.Label(text = f": {startTime}", font = ("Helvetica", 20))
    time_label2.place(x = 300, y = 250)

    # 予約者情報入力画面

    # 名前入力欄
    name_label = tk.Label(text = "名前", font = ("Helvetica", 20))
    name_label.place(x = 100, y = 325)
    name_entry = tk.Entry(width = 10, font = ("Helvetica", 30))
    name_entry.place(x = 300, y = 325)

    # 電話番号入力欄
    phone_label = tk.Label(text = "電話番号", font = ("Helvetica", 20))
    phone_label.place(x = 100, y = 400)
    phone_entry = tk.Entry(width = 10, font = ("Helvetica)", 33))
    phone_entry.place(x = 300, y = 400)

    # 予約ボタン

    def insert_reservation(name, phone, way):

        # 早期予約かチェックする
        # 予約日が当日から1週間以内の場合、早期予約と判定しinsert_reservationの引数としてdiscountに早期割引を渡す

        discount = "なし"
        today = datetime.date.today()
        reserved_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if (reserved_date - today).days >= 7:
            discount = "早期予約割引"


        # table_stateから予約するテーブルを取得
        # 予約するテーブルの番号を取得
        for i in range(0, 8):
            if table_state[i] == 1:
                tableNo = i + 1
                db.insert_reservation(tableNo, int(re.sub(r"\D", "", date)), int(startTime.split(":")[0]), name, phone, way, discount)

        label = tk.Label(text = "予約が完了しました！\nweb予約特典がございますので\nお楽しみにお待ちください！", font = ("Helvetica", 20))

        label.place(x = 200, y = 410)

        label = tk.Label(text = "10秒後にウィンドウを閉じます", font = ("Helvetica", 10))

        label.place(x = 300, y = 525)

        reservation_button.destroy()

        # root.after(10000, delay_destroy, root)

        # 予約確認画面へ遷移
    def confirm_reservation():
        if name_entry.get() == "" or phone_entry.get() == "":
            caution_label.configure(text = "＊名前と電話番号を入力してください")
            caution_label.place(x = 65, y = 30)
            return
        
        name = name_entry.get()
        phone = phone_entry.get()
        name_entry.destroy()
        phone_entry.destroy()
        time_label.place(y = 150)
        time_label2.place(y = 150)
        date_label.place(y = 200)
        date_label2.place(y = 200)
        name_label.place(y = 250)
        phone_label.place(y = 300)
        name_label2 = tk.Label(text = f": {name}", font = ("Helvetica", 20))
        name_label2.place(x = 300, y = 250)
        phone_label2 = tk.Label(text = f": {phone}", font = ("Helvetica", 20))
        phone_label2.place(x = 300, y = 300)

        reservation_button.configure(text = "予約")
        reservation_button.configure(command = lambda : insert_reservation(name, phone, way))

        label_confirm = tk.Label(text = "以上の内容で予約しますか？", font = ("Helvetica", 20))
        label_confirm.place(x = 100, y = 350)

    

    reservation_button = tk.Button(text = "確認", command = confirm_reservation, font = ("Helvetica", 20))

    reservation_button.place(x = 350, y = 500, width = 100, height = 50)



def debugging():
    root = tk.Tk()
    root.geometry("800x600")
    input_flow([0, 1, 0, 0, 0, 0, 1, 0], "2025-02-02", "13:00", "8", "web")
    root.mainloop()

# debugging()