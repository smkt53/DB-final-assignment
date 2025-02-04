import psycopg2


# PostgreSQLデータベースへの接続情報
DB_HOST = "localhost"
DB_NAME = "restaurant_reservation_system"
DB_USER = "restaurant"
DB_PASSWORD = "restaurant"
DB_PORT = "5432"

table = [1, 1, 1, 1, 1, 1, 1, 1]

rows_staff = []

def is_reservation_possible(date, starttime):

    global table
    table = [1, 1, 1, 1, 1, 1, 1, 1]
    """
    指定された日時に予約が可能かをチェックする。

    Args:
        date (int): 日付 (yyyymmdd形式)。
        starttime (int): 開始時間 (hh形式)。

    Returns:
        bool: 予約が可能かどうか。
    """
    
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()

        for i in range(-1, 2):
            cursor.execute("select * from reservations where date = %s and starttime = %s", (date, starttime + i))
            rows = cursor.fetchall()
            # 予約情報を全て取得
            for row in rows:
                for i in range(0, 8):
                    if(row[0] == (i + 1)):
                        table[i] = 0


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"エラーが発生しました: {error}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def insert_reservation(no, date, starttime, name, phone, way, discount):
    """
    予約をデータベースに挿入する。

    Args:
        date (int): 日付。
        starttime (int): 開始時間。
        name (str): 名前。
        phone (str): 電話番号。
    """
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()

        cursor.execute("insert into reservations (no, date, starttime, name, phone, way, discount) values (%s, %s, %s, %s, %s, %s, %s)", (no, date, starttime, name, phone, way, discount))

        connection.commit()

        print("予約を追加しました")


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"エラーが発生しました: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# 特定の日の予約を全て表示する
def show_reservation(date):
    """
    指定された日の予約を表示する。

    Args:
        date (int): 日付。
    """
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()

        cursor.execute("select * from reservations where date = %s", (date,))
        rows = cursor.fetchall()
        global rows_staff
        rows_staff = rows


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"エラーが発生しました: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# is_reservation_possible(20250211, 12)
# insert_reservation(5, 20250202, 15, "山田太郎", "090-1234-5678", "web", "早期予約割引")

