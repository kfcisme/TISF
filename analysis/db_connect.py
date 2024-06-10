import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

class analysis_MySQLConnection:
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
            print("數據分析資料庫連接成功。")
        except Exception as e:
            print(f"連接資料庫失敗：{e}")
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            print("數據庫連接已關閉。")

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records

    def execute_insert(self, query, params):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()