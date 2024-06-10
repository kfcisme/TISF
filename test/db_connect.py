import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

class report_MySQLConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.conn.is_connected():
                print("report資料庫連接成功。")
            return self.conn
        except mysql.connector.Error as e:
            print(f"連接資料庫失敗：{e}")
            return None

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("數據庫連接已關閉。")

    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            return records
        except Exception as e:
            print(f"執行查詢失敗：{e}")
            return []

    def execute_insert(self, query, params):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"插入數據失敗：{e}")