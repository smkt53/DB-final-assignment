import tkinter as tk
from tkinter import ttk
import datetime
import re
import dbControl as db
import inputInfo as ii

reserved_date = ""
reserved_people = ""
reserved_starttime = ""
table_state = [0, 0, 0, 0, 0, 0, 0, 0]

oval_x1 = 450
oval_x2 = 550

oval2_x1 = 625
oval2_x2 = 725

way = "web"



def menu_default():    
    # コンボボックスから日付を受け取る
    # 変数に代入して予約したい日時を保存する
    def select_day_combo(event):
        global reserved_date
        reserved_date = combobox_day.get()
        print(reserved_date)


    # コンボボックスから人数を受け取る
    # 変数に代入して予約したい人数を保存する
    def select_people_combo(event):
        global reserved_people
        reserved_people = combobox_people.get()
        print(reserved_people)

    # コンボボックスから開始時間を受け取る
    # 変数に代入して予約したい開始時間を保存する
    def select_starttime_combo(event):
        global reserved_starttime
        reserved_starttime = comobbox_starttime.get()
        print(reserved_starttime)

    # 空席確認ボタンが押されたときに呼び出される関数
    # 予約可能かどうかをチェックする
    # 座席を表示し、予約が可能なら赤、不可能ならグレーの円（テーブルをイメージ）で表示する
    # 予約が可能なら選択ボタンを表示する
    # 利用時間は2時間固定
    # 検索方法：予約テーブルから日付、開始時間、利用時間を条件に検索し、空いているテーブルを表示する
    #       データベースから取得した日付と同じ日付のデータを取得する、
    #       ユーザから得た開始時間を基に、データベースから使用していないかを確認する
    #           例：ユーザが15時に予約したい場合、データベースから14時, 15時, 16時開始のデータを取得する
    #             ：13時開始は15時に終了するため、使用していないと判断する
    def search_button_click():
        
        if reserved_date == "" or reserved_people == "" or reserved_starttime == "":
            print("予約情報を選択してください")
            caution_label.config(text = "予約情報を選択してください")
            return
        print("以下の情報で空席確認を行います")
        print(reserved_date)
        print(reserved_people)
        print(reserved_starttime)
        
        print()

        db.is_reservation_possible(int(re.sub(r"\D", "", reserved_date)), int(reserved_starttime.split(":")[0]))

        for i in range(0, 4):
            if db.table[i] == 1:
                canvas.create_oval(oval_x1, 100 + i * 100, oval_x2, 150 + i * 100, fill="red")
                buttons[i].config(text = "可能", background="red", state="normal")
            else:
                canvas.create_oval(oval_x1, 100 + i * 100, oval_x2, 150 + i * 100, fill="grey")
                buttons[i].config(text = "不可", background="grey", state="disabled")
                
        
        for i in range(4, 8):
            if db.table[i] == 1:
                canvas.create_oval(oval2_x1, 100 + (i - 4) * 100, oval2_x2, 150 + (i - 4) * 100, fill="red")
                buttons[i].config(text = "可能", background="red", state="normal")
            else:
                canvas.create_oval(oval2_x1, 100 + (i - 4) * 100, oval2_x2, 150 + (i - 4) * 100, fill="grey")
                buttons[i].config(text = "不可", background="grey", state="disabled")


    # テーブルボタンが押されたときに呼び出される関数
    # 押されたボタンが何番目かを取得し、その番号のテーブルが可能だったら色をオレンジに変更し、文字列を選択に変更する
    # もし選択だった場合は逆に赤に変更し、不可に変更する
    def click_table_button(index):
        if buttons[index].cget("text") == "可能":
            buttons[index].config(text = "選択", background="orange")
        elif buttons[index].cget("text") == "選択":
            buttons[index].config(text = "可能", background="red")

    def click_reserved_button():
        if reserved_people == "" or reserved_date == "" or reserved_starttime == "":
            print("予約情報を選択してください")
            caution_label.config(text = "予約情報を選択してください")
            return
        # 選択されたテーブル数が正しいか確認する
        # 1~4人なら1テーブル、5~8人なら2テーブル、9~12人なら3テーブル
        table_count = 0
        for i in range(0, 8):
            if buttons[i].cget("text") == "選択":
                table_count += 1
        if int(reserved_people) <= 4 and table_count != 1:
            print("テーブルは1つだけ選択してください")
            caution_label.config(text = "テーブルは1つだけ\n選択してください")
            return
        elif 5 <= int(reserved_people) <= 8 and table_count != 2:
            print("テーブルは2つだけ選択してください")
            caution_label.config(text = "テーブルは2つだけ\n選択してください")
            return
        elif 9 <= int(reserved_people) <= 12 and table_count != 3:
            print("テーブルは3つだけ選択してください")
            caution_label.config(text = "テーブルは3つだけ\n選択してください")
            return
        else:
            print("テーブル数は正しいです")
            caution_label.config(text = "予約者情報を入力してください")

        print("予約者情報入力")
        # 予約者情報入力画面に遷移する
        # 選択したテーブル、日付、開始時間、人数を引数に渡す
        global table_state
        for i in range(0, 8):
            if buttons[i].cget("text") == "選択":
                table_state[i] = 1

        frame.destroy()
        
        # 現在の画面を破棄し、入力画面を表示する
        ii.input_flow(table_state, reserved_date, reserved_starttime, reserved_people, way)

    label = tk.Label(frame, text = "予約画面", font = ("Helvetica", 20))

    label.pack()

    today = datetime.date.today()

    combobox_day = ttk.Combobox(frame, state="readonly", width=13, height= 30, values=[today + datetime.timedelta(days=i) for i in range(30)], font = ("Helvetica", 20))

    combobox_day.set("日付を選択")

    combobox_day.bind('<<ComboboxSelected>>', select_day_combo)

    combobox_day.place (x = 100, y = 100)

    combobox_people = ttk.Combobox(frame, state="readonly", width=13, height= 30, values=[i for i in range(1, 11)], font = ("Helvetica", 20))

    combobox_people.set("人数を選択")

    combobox_people.bind('<<ComboboxSelected>>', select_people_combo)

    combobox_people.place (x = 100, y = 200)

    comobbox_starttime = ttk.Combobox(frame, state="readonly", width=13, height= 30, values=["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"], font = ("Helvetica", 20))

    comobbox_starttime.set("開始時間を選択")

    comobbox_starttime.place (x = 100, y = 300)

    comobbox_starttime.bind('<<ComboboxSelected>>', select_starttime_combo)

    searchButton = tk.Button(frame, text = "空席確認", font = ("Helvetica", 20), command = search_button_click)

    searchButton.place(x = 135, y = 375)

    reserved_button = tk.Button(frame, text = "予約", font = ("Helvetica", 20), command = click_reserved_button)

    reserved_button.place(x = 165, y = 460)

    caution_label = tk.Label(frame, text = "", font = ("Helvetica", 20), foreground="red")

    caution_label.place(x = 400, y = 475)

    canvas.create_oval(oval_x1, 100, oval_x2, 150, fill="white")

    canvas.create_oval(oval_x1, 200, oval_x2, 250, fill="white")

    canvas.create_oval(oval_x1, 300, oval_x2, 350, fill="white")

    canvas.create_oval(oval_x1, 400, oval_x2, 450, fill="white")

    canvas.create_oval(oval2_x1, 100, oval2_x2, 150, fill="white")

    canvas.create_oval(oval2_x1, 200, oval2_x2, 250, fill="white")

    canvas.create_oval(oval2_x1, 300, oval2_x2, 350, fill="white")

    canvas.create_oval(oval2_x1, 400, oval2_x2, 450, fill="white")

    buttons = ["テーブル1", "テーブル2", "テーブル3", "テーブル4", "テーブル5", "テーブル6", "テーブル7", "テーブル8"]

    for i in range(0, 4):
        buttons[i] = tk.Button(frame, text = "不可", font = ("Helvetica", 15), background="white", foreground="grey", relief="flat", state="disabled", command = lambda i=i: click_table_button(i))
        buttons[i].place(x = 472, y = 105 + i * 100)

    for i in range(4, 8):
        buttons[i] = tk.Button(frame, text = "不可", font = ("Helvetica", 15), background="white", foreground="grey", relief="flat", state="disabled", command = lambda i=i: click_table_button(i))
        buttons[i].place(x = 647, y = 105 + (i - 4) * 100)



root = tk.Tk()

root.title("Menu")

root.geometry("800x600+500+100")

root.resizable(width = False, height = False)

frame = tk.Frame(root)

frame.pack( fill = tk.BOTH, expand = True)

canvas = tk.Canvas(frame, width = 800, height = 600)

canvas.place(x = 0, y = 0)

if __name__ != "__main__":
    way = "staff"

menu_default()

root.mainloop()

