# conn to sqlite
import requests
import json
from datetime import datetime
from connect_to_sqlite import MusicalDatabase
from connect_to_mongo import connect_to_mongo, upload_to_mongo
def get_data():
    url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
    # schema_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJOpenApi&category=1'
    res = requests.get(url)
    data = json.loads(res.text)
    return data

# 處理 Location
class UpdateProcess:
    def __init__(self, dict_UID: dict, dict_locNames: list) -> None:
        self.dict_UID = dict_UID
        self.dict_locNames = dict_locNames

    def update_location(self, show, db):
        locationName = show.get('locationName')
        if locationName not in self.dict_locNames:
            location = show.get('location')
            latitude = show.get('latitude')
            longitude = show.get('longitude')
            row = (location, locationName, latitude, longitude)
            # insert the location & update list
            if self.dict_locNames:
                # index is the next number
                index = list(self.dict_locNames.values())[-1] + 1
                self.dict_locNames.update({locationName : index})
            else:
                # from 1 begin
                index = 1
                self.dict_locNames.update({locationName : index})

            db.insert_location_data(row)
            print('Update location!')



    def update_activity(self, item, db):
        UID = item.get('UID')
        if UID not in self.dict_UID:
            self.is_new_UID = True
            self.UID = UID

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

            # list: masterUnit,subUnit,supportUnit,otherUnit
            masterUnit = self._list_to_str(item.get('masterUnit'))
            subUnit = self._list_to_str(item.get('subUnit'))
            supportUnit = self._list_to_str(item.get('supportUnit'))
            otherUnit = self._list_to_str(item.get('otherUnit'))

            # datetime: editModifyDate, startDate, endDate
            editModifyDate = self._str_to_datetime(item.get('editModifyDate'))
            startDate = self._str_to_datetime(item.get('startDate'))
            endDate = self._str_to_datetime(item.get('endDate'))

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

            db.insert_activity_data(row)
            print('Update activity!')

            if self.dict_UID:
                # index is the next number
                index = list(self.dict_UID.values())[-1] + 1
                self.dict_UID.update({UID : index})
            else:
                # from 1 begin
                index = 1
                self.dict_UID.update({UID : index})
        else:
            self.is_new_UID = False

    # 處理Showinfo
    def update_showinfo(self, show, db):
        locationName = show.get('locationName')
        activity_id = self.dict_UID.get(self.UID)
        location_id = self.dict_locNames.get(locationName)
        onSales = show.get('onSales')
        price = show.get('price')
        time = self._str_to_datetime(show.get('time'))
        endTime = self._str_to_datetime(show.get('endTime'))

        row = (activity_id,
                location_id,
                time,
                onSales,
                price,
                endTime)
        db.insert_show_data(row)
        print('Update showinfo!')
    def update_process(self, item, db):
        self.update_activity(item, db)
        if self.is_new_UID:
            shows = item.get('showInfo')
            for show in shows:
                self.update_location(show, db)
                self.update_showinfo(show, db)
        print('Success')

    # 處理Activity
    def _list_to_str(self, l: list):
        text = ','.join(l)
        return text


    def _str_to_datetime(self, text: str):
        if len(text)==10:
            text = datetime.strptime(text, '%Y/%m/%d')
        elif len(text)==0:
            text = None
        else:
            text = datetime.strptime(text, '%Y/%m/%d %H:%M:%S')
        return text


if __name__ == '__main__':
    """
    用於每日更新
    如果為空，重新建立資料表
    更新順序 爬蟲 -> 比對UID -> 更新location -> 更新showinfo
    """

    mongo_url = "mongodb://localhost:27017/"
    conn  = connect_to_mongo(mongo_url)

    try:
        data = get_data()
        db_path = '../Web/test.db'
        db = MusicalDatabase(db_path)
        db.connect()
        dict_UID, dict_locNames = db.get_dict_UID_locNames()
        
        process = UpdateProcess(dict_UID, dict_locNames)
        for item in data:
            process.update_process(item, db)

        db.close()

        is_finished = True
        report = ''
    except Exception as e:
        report = e
        is_finished = False

    if conn:
        upload_to_mongo(conn, is_finished, report)
        
    # schema = requests.get(schema_url)
    # schema = json.loads(schema.text)
    # schema = schema['components']['schemas']
    # col_activity = list(schema['Activity']['properties'].keys())
