import pymongo
from datetime import datetime
import pymongo
import pandas as pd
# 連線 MongoDB
def connect_to_mongo(url, db, collection):
    try:
        # 建立 MongoClient 物件，預設連接到本機的 MongoDB 伺服器
        client = pymongo.MongoClient(url)
        conn = client[db][collection]

        print("MongoDB is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("MongoDB falis in connect: %s" % e)
        return None

def upload_to_mongo(conn, is_finished, report):
    try:
        date = datetime.now()
        
        # 要插入的資料
        log = {"DateTime": date, "is_finished": is_finished, 'log': report}

        # 插入資料
        result = conn.insert_one(log)
        print("monog upload success!")

    except Exception as e:
        print("monog fails in upload: %s" % e)

def mongo_to_dataframe(conn, pipeline: list):
    # 執行聚合操作
    results = list(conn.aggregate(pipeline))
    df = pd.DataFrame(results)

    return df

if __name__ == '__main__':
    mongo_url = "mongodb://localhost:27017/"
    conn  = connect_to_mongo(mongo_url)
    # query all logs
    df = mongo_to_dataframe(conn, [{}])
    print(df)