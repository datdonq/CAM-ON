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
def retrival_query(query):
    server = 'DESKTOP-BVGOMR7'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None