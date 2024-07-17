
import sqlite3

def connect_to_database(db_name):
    """連接到 SQLite 資料庫"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def create_users_table(cursor):
    """建立 users 表格"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    ''')

def create_activity_table(cursor):
    """建立 Activity 表格"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musicial_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UID VARCHAR(255) UNIQUE,
            version VARCHAR(50) ,
            title VARCHAR(255),
            category INTEGER,
            showUnit VARCHAR(255),
            discountInfo VARCHAR(255),
            descriptionFilterHtml TEXT,
            imageUrl VARCHAR(255),
            masterUnit VARCHAR(255),
            subUnit VARCHAR(255),
            supportUnit VARCHAR(255),
            otherUnit VARCHAR(255),
            webSales VARCHAR(255),
            sourceWebPromote VARCHAR(255),
            comment TEXT,
            editModifyDate DATETIME,
            sourceWebName VARCHAR(255),
            startDate DATETIME,
            endDate DATETIME,
            hitRate INTEGER
        )
    ''')


def create_showinfo_table(cursor):
    """建立 ShowInfo 表格"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musicial_showinfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER REFERENCES musicial_activity(id),
            location_id INTEGER REFERENCES musicial_location(id),
            time DATETIME ,
            onSales VARCHAR(255),
            price VARCHAR(255),
            endTime DATETIME
        )
    ''')    

def create_location_table(cursor):
    """建立 Location 表格"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musicial_location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location VARCHAR(255),
            locationName VARCHAR(255) UNIQUE,
            latitude FLOAT,
            longitude FLOAT
        )
    ''')  

def insert_location_data(row):
    # 連接到 SQLite 資料庫
    conn, cursor = connect_to_database('../test.db')

    location, locationName, latitude, longitude = row
    query = """
    INSERT INTO musicial_location (location, locationName, latitude, longitude)
            VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (location, locationName, latitude, longitude))

    conn.commit()
    conn.close()


def insert_activity_data(row):
    # 連接到 SQLite 資料庫
    conn, cursor = connect_to_database('../test.db')

    UID, \
    version, \
    title, \
    category, \
    showUnit, \
    discountInfo, \
    descriptionFilterHtml, \
    imageUrl, \
    masterUnit, \
    subUnit, \
    supportUnit, \
    otherUnit, \
    webSales, \
    sourceWebPromote, \
    comment, \
    editModifyDate, \
    sourceWebName, \
    startDate, \
    endDate, \
    hitRate = row
    query = """
    INSERT INTO musicial_activity 
            (UID,
            version,
            title,
            category,
            showUnit,
            discountInfo,
            descriptionFilterHtml,
            imageUrl,
            masterUnit,
            subUnit,
            supportUnit,
            otherUnit,
            webSales,
            sourceWebPromote,
            comment,
            editModifyDate,
            sourceWebName,
            startDate,
            endDate,
            hitRate)

            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    cursor.execute(query, (UID,
            version,
            title,
            category,
            showUnit,
            discountInfo,
            descriptionFilterHtml,
            imageUrl,
            masterUnit,
            subUnit,
            supportUnit,
            otherUnit,
            webSales,
            sourceWebPromote,
            comment,
            editModifyDate,
            sourceWebName,
            startDate,
            endDate,
            hitRate))

    conn.commit()
    conn.close()


def insert_show_data(row):
    # 連接到 SQLite 資料庫
    conn, cursor = connect_to_database('../test.db')
    activity_id, location_id, time, onSales, price, endTime = row
    query = """
    INSERT INTO musicial_showinfo (activity_id, location_id, time,onSales, price, endTime)
            VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (activity_id, location_id, time, onSales, price, endTime))

    conn.commit()
    conn.close()

def main():
    # 連接到 SQLite 資料庫
    conn, cursor = connect_to_database('../test.db')

    # 建立 Activity 表格
    # create_activity_table(cursor)
    
    # 建立 Location 表格
    create_location_table(cursor)

    # 建立 ShowInfo 表格
    create_showinfo_table(cursor)


    conn.commit()
    conn.close()
