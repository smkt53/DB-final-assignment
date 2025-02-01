import tkinter as tk
from tkinter import ttk
import dbControl as db
import re
import datetime




def set_window():
    global root_staff
    global frame_staff
    global canvas

    # 予約を追加するためのmenuを表示する
    def add_reservation():
        print("予約を追加します")
        root_staff.destroy()
        import menu

        # 日付を選択し、その日の予約情報をすべて表示する
    def show_reservation():
        if(select_day.get() == ""):
            print("日付を選択してください")
            return
        print("予約情報を表示します")
        db.show_reservation(int(re.sub(r"\D", "", select_day.get())))
        print(db.rows_staff)

        # 予約情報を表示する
        label_title = tk.Label(text = "予約情報", font = ("Helvetica", 30))
        label_title.place(x = 50, y = 160)

        label_no = tk.Label(text = "番号", font = ("Helvetica", 20))
        label_no.place(x = 50, y = 210)

        label_date = tk.Label(text = "日付", font = ("Helvetica", 20))
        label_date.place(x = 130, y = 210)

        label_starttime = tk.Label(text = "開始時間", font = ("Helvetica", 20))
        label_starttime.place(x = 250, y = 210)

        label_name = tk.Label(text = "名前", font = ("Helvetica", 20))
        label_name.place(x = 375, y = 210)

        label_phone = tk.Label(text = "電話番号", font = ("Helvetica", 20))
        label_phone.place(x = 600, y = 210)

        label_discount = tk.Label(text = "割引", font = ("Helvetica", 20))
        label_discount.place(x = 850, y = 210)

    
        for row in db.rows_staff:
            # テーブル番号
            label1 = tk.Label(text = row[0], font = ("Helvetica", 20))
            label1.place(x = 70, y = 250 + 30 * db.rows_staff.index(row))

            # 日付
            label2 = tk.Label(text = row[1], font = ("Helvetica", 20)) 
            label2.place(x = 120, y = 250 + 30 * db.rows_staff.index(row))

            # 開始時間
            label3 = tk.Label(text= str(row[2]) + "時", font = ("Helvetica", 20))
            label3.place(x = 270, y = 250 + 30 * db.rows_staff.index(row))

            # 名前
            label4 = tk.Label(text = row[3], font = ("Helvetica", 20))
            label4.place(x = 380, y = 250 + 30 * db.rows_staff.index(row))

            # 電話番号
            label5 = tk.Label(text = row[4], font = ("Helvetica", 20))
            label5.place(x = 600, y = 250 + 30 * db.rows_staff.index(row))

            # 割引
            label6 = tk.Label(text = row[5], font = ("Helvetica", 20))
            label6.place(x = 850, y = 250 + 30 * db.rows_staff.index(row))

        if(len(db.rows_staff) == 0):
            print("予約情報がありません")
            label_no = tk.Label(text = str(datetime.date.today()) + "に予約情報がありません", font = ("Helvetica", 20))
            label_no.place(x = 300, y = 50)
        else:
            label_no.config(text = str(datetime.date.today()) + "の予約情報")
            label_no.place(x = 300, y = 50)








    button = tk.Button(text = "予約を追加", font = ("Helvetica", 20), command = add_reservation)
    button.place(x = 100, y = 50)

    button2 = tk.Button(text = "予約情報を表示", font = ("Helvetica", 20), command = show_reservation)
    button2.place(x = 100, y = 100)

    select_day = ttk.Combobox(root_staff, state = "readonly", width=10 , font = ("Helvetica", 30), values=[datetime.date.today() + datetime.timedelta(days=i) for i in range(30)])
    select_day.place(x = 350, y = 100)
    

    

    


root_staff = tk.Tk()

root_staff.title("Menu")

root_staff.geometry("800x600+500+100")

frame_staff = tk.Frame(root_staff)

frame_staff.pack( fill = tk.BOTH, expand = True)

canvas = tk.Canvas(frame_staff, width = 800, height = 600)

canvas.place(x = 0, y = 0)

set_window()

root_staff.mainloop()