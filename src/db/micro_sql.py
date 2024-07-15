import pyodbc
from datetime import datetime
# Cấu hình kết nối
server = 'HEROX\SQLEXPRESS'  # Tên server của bạn
database = 'CamOnDB'  # Thay bằng tên database bạn muốn kết nối

# Tạo kết nối sử dụng Windows Authentication
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(connection_string)
def execute_query(query):
    server = 'HEROX\SQLEXPRESS'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    
def retrival_query(query: str):
    server = 'HEROX\SQLEXPRESS'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return [row for row in result] if result else []

def retrival_query_user(query: str, params: tuple):
    server = 'HEROX\SQLEXPRESS'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return [row for row in result] if result else []

def fetch_query(query: str):
    server = 'HEROX\SQLEXPRESS'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    result = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in result] if result else []

def fetch_query_user(query: str) :
    server = 'HEROX\SQLEXPRESS'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    result = cursor.fetchall()
    conn.close()

    # Chuyển đổi các kiểu dữ liệu datetime và datetimeoffset sang chuỗi
    formatted_result = []
    for row in result:
        row_dict = {}
        for col, val in zip(columns, row):
            if isinstance(val, datetime):
                row_dict[col] = val.isoformat()
            elif isinstance(val, bytes) and len(val) == 10:  # Chuyển đổi datetimeoffset thành chuỗi
                row_dict[col] = datetime.strptime(val.decode('utf-8'), '%Y-%m-%d %H:%M:%S').isoformat()
            else:
                row_dict[col] = val
        formatted_result.append(row_dict)

    return formatted_result if result else []