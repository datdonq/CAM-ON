import pyodbc
# Cấu hình kết nối
server = 'DESKTOP-BVGOMR7'  # Tên server của bạn
database = 'CamOnDB'  # Thay bằng tên database bạn muốn kết nối

# Tạo kết nối sử dụng Windows Authentication
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(connection_string)
def execute_query(query):
    server = 'DESKTOP-BVGOMR7'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    
def retrival_query(query: str):
    server = 'DESKTOP-BVGOMR7'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return [row for row in result] if result else []

def fetch_query(query: str):
    server = 'DESKTOP-BVGOMR7'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    result = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in result] if result else []