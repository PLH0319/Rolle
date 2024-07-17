# conn to sqlite
import requests
import pandas as pd
import json
from datetime import datetime
url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
schema_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJOpenApi&category=1'

res = requests.get(url)
data = pd.read_json(res.text)
data = json.loads(res.text)


schema = requests.get(schema_url)
schema = json.loads(schema.text)
schema = schema['components']['schemas']

col_showinfo = list(schema['ShowInfo']['properties'].keys())

col_activity = list(schema['Activity']['properties'].keys())
col_activity.remove('showInfo')



for item in data[col_activity].iloc[0]:
    if isinstance(item, list):
        print(item)


col_to_text = ['masterUnit','subUnit','supportUnit','otherUnit']

# showinfo 轉成 id 
# 其餘 list 無額外資訊,以字串儲存


# 處理 Location
def insert_all_locations(data):
    locationNames = []
    count = 0
    location_count = 0
    for items in data:
        print(f"Update in index:{count}")
        shows = items.get('showInfo')
        for show in shows:
            location = show.get('location')
            locationName = show.get('locationName')
            latitude = show.get('latitude')
            longitude = show.get('longitude')
            row = (location, locationName, latitude, longitude)
            if locationName not in locationNames:
                insert_location_data(row)
                locationNames.append(locationName)
                location_count +=1
                print('Add a location, now location:', location_count)
        count += 1
insert_all_locations(data)

# cursor.execute("DROP TABLE IF EXISTS musicial_showinfo")

def fetch_location(conn):
    _query = """
    Select *
    from musicial_location
    """
    df = pd.read_sql_query(_query, conn)
    return df

df_locations = fetch_location(conn)

# 處理Activity
def list_to_text(l: list):
    text = ','.join(l)
    return text

def text_to_datetime(text: str):
    if len(text)==10:
        text = datetime.strptime(text, '%Y/%m/%d')
    elif len(text)==0:
        text = None
    else:
        text = datetime.strptime(text, '%Y/%m/%d %H:%M:%S')
    return text

def insert_all_activity(data):
    activities = []
    count = 0
    for item in data:
        print(f"Update in index:{count}")
        UID = item.get('UID')
        version = item.get('version')
        title = item.get('title')
        category = item.get('category')
        showUnit = item.get('showUnit')
        discountInfo = item.get('discountInfo')
        descriptionFilterHtml = item.get('descriptionFilterHtml')
        imageUrl = item.get('imageUrl')
        webSales = item.get('webSales')
        sourceWebPromote = item.get('sourceWebPromote')
        comment = item.get('comment')
        sourceWebName = item.get('sourceWebName')
        endDate = item.get('endDate')
        hitRate = item.get('hitRate')

        # 'masterUnit','subUnit','supportUnit','otherUnit'
        masterUnit = list_to_text(item.get('masterUnit'))
        subUnit = list_to_text(item.get('subUnit'))
        supportUnit = list_to_text(item.get('supportUnit'))
        otherUnit = list_to_text(item.get('otherUnit'))

        # editModifyDate, startDate, endDate
        editModifyDate = text_to_datetime(item.get('editModifyDate'))
        startDate = text_to_datetime(item.get('startDate'))
        endDate = text_to_datetime(item.get('endDate'))


        row = (UID,
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

        if UID not in activities:
            insert_activity_data(row)
            activities.append(UID)
    count +=1
act_data = data
insert_all_activity(act_data)

def fetch_activity(conn):
    _query = """
    Select *
    from musicial_activity
    """
    df = pd.read_sql_query(_query, conn)
    return df

df_activity = fetch_activity(conn)
# 處理Showinfo
def insert_all_shows(data, df_locations):
    for idx, items in enumerate(data):
        print(f"Update in index:{idx}")
        shows = items.get('showInfo') 
        for item in shows:
            activity_id = idx + 1
            location_id = int(df_locations.loc[df_locations['locationName']==item.get('locationName'),'id'])
            time = text_to_datetime(item.get('time'))
            onSales = item.get('onSales')
            price = item.get('price')
            endTime = item.get('endTime')

            row = (activity_id,
                    location_id,
                    time,
                    onSales,
                    price,
                    endTime)

            insert_show_data(row)

insert_all_shows(data, df_locations)

def fetch_showinfo(conn):
    _query = """
    Select *
    from musicial_showinfo
    """
    df = pd.read_sql_query(_query, conn)
    return df

df_showinfo = fetch_showinfo(conn)