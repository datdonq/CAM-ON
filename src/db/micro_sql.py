import pyodbc
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
def retrival_query(query):
    server = 'HEROX\SQLEXPRESS'
    database = 'CamOnDB'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

insert_query = """
INSERT INTO AspNetUsers (
    Id, 
    UserName, 
    NormalizedUserName, 
    Email, 
    NormalizedEmail, 
    EmailConfirmed, 
    PasswordHash, 
    SecurityStamp, 
    ConcurrencyStamp, 
    PhoneNumber, 
    PhoneNumberConfirmed, 
    TwoFactorEnabled, 
    LockoutEnd, 
    LockoutEnabled, 
    AccessFailedCount
) VALUES (
    NEWID(),  -- Tạo ID ngẫu nhiên
    'dongdong', 
    'DONGDONG', 
    'dongdong@example.com', 
    'DONGDONG@EXAMPLE.COM', 
    0,  -- EmailConfirmed
    '123123',  -- PasswordHash
    NEWID(),  -- SecurityStamp ngẫu nhiên
    NEWID(),  -- ConcurrencyStamp ngẫu nhiên
    NULL,  -- PhoneNumber
    0,  -- PhoneNumberConfirmed
    0,  -- TwoFactorEnabled
    NULL,  -- LockoutEnd
    0,  -- LockoutEnabled
    0   -- AccessFailedCount
);
"""

# execute_query(insert_query)