SQL vs. No-SQL 的差異
數據模型：

SQL： 使用結構化數據模型，通常是表格形式，有固定的模式（schema），包括列名、數據類型等。使用關聯型數據庫管理系統（RDBMS）來處理數據。
No-SQL： 使用靈活的數據模型，例如文檔、鍵值對、列族或圖形等。這些數據庫可以處理非結構化、半結構化和結構化數據。
架構和一致性：

SQL： 傳統SQL數據庫通常支持ACID（原子性、一致性、隔離性、持久性）事務特性，以確保數據的完整性和一致性。
No-SQL： 大多數No-SQL數據庫放棄了ACID事務特性，注重於高可用性和分佈式架構，提供了更靈活的一致性模型（如BASE，即Basically Available、Soft state、Eventually consistent）。
擴展性和性能：

SQL： 傳統的關聯型數據庫在擴展性上通常受限，難以應對大規模數據的高性能需求。
No-SQL： 許多No-SQL數據庫設計為分佈式系統，可以更容易地擴展以處理大量數據和高流量。
運用場景
SQL的運用場景：

傳統的業務應用程序： 需要事務支持和複雜的查詢操作，如電子商務平台、ERP系統等。
需要複雜的查詢： 需要進行複雜的數據分析和多表關聯查詢的場景。
數據一致性要求高： 需要確保數據的ACID特性和絕對的一致性的應用。
No-SQL的運用場景：

大數據和即時Web應用： 需要處理大量非結構化或半結構化數據的應用，如社交網絡、日誌數據分析等。
高性能和可擴展性要求： 需要在多台服務器上平行處理和存儲數據的應用。
靈活的數據模型： 需要支持頻繁變更和擴展數據模型的應用，如內容管理、設備監控等。
總結
SQL和No-SQL數據庫各有其獨特的優勢和適用場景。選擇適合的數據庫類型取決於應用的需求，包括數據的結構化程度、一致性和性能要求等。在現代應用開發中，有時也會使用混合模式，根據需求選擇適合的SQL和No-SQL數據庫來達到最佳的效果。


# 為何要執行正規化？
提昇儲存資料與資料庫操作效率
減少資料異常
使資料庫維護更容易

## 正規化的資料庫特性
經過正規化後的資料庫，應具備以下特性：

欄位唯一性：每個欄位只儲存一項資料
主關鍵欄位：每筆資料都擁有一個主鍵，來區別這些資料
功能關聯性：欄位之間的關聯應該要明確
欄位獨立性：欄位之間不應存在遞移相依

## 第一正規化
問題：

一個欄位儲存多筆資料(elements need spilt)
出現意義上重複的欄位(column useless)
缺乏主鍵(Primary Key)

第一NF要完成的工作：

一個欄位只能有單一值
消除意義上重複的欄位
決定主鍵

## 第二正規化
問題：

出現過多重複資料(rows_complicated)

第二NF要完成的工作：

消除部分相依:
部分相依的意思為跟主鍵只有一部份有關係，另一部份沒有關係的欄位，我們要把這些欄位獨立於另一張表。

## 第三正規化
第三NF要完成的工作：

消除資料表中的遞移相依
消除遞移相依：非主鍵屬性的欄位都只能和候選鍵相關，非主鍵屬性的欄位彼此間應該要是獨立無關的

遞移關係，在這個範例裡就是指：總金額是依賴商品及數量的資訊，而商品id和數量又和主鍵直接相關，那總金額和主鍵之間的關係就是遞移關係。


Event
-------------------
UID: Event
version: Event
title: Event
category: Event
showUnit: Event
discountInfo: Event
descriptionFilterHtml: Event
imageUrl: Event
masterUnit: Event
subUnit: Event
supportUnit: Event
otherUnit: Event
webSales: Event
sourceWebPromote: Event
comment:Event
editModifyDate:Event
sourceWebName:Event
startDate:Event
endDate:Event
hitRate:Event
showInfo: {pk: UID}

Show
-----------------------------
pk: (UID,time,location_id)
UID
"time": "2024/11/23 14:30:00",
"onSales": "Y",
"price": "",
"endTime": "2024/11/23 16:00:00"
location_id


Location
--------------------------
location_id: 0
"location": "臺中市西屯區惠來路二段101號",
"locationName": "臺中國家歌劇院小劇場",
"latitude": "24.1626492",
"longitude": "120.6403028",


showUnit: 不拆開,表演人,表演團隊無額外資勛。

 "Activity": 
                "type": "object",
                "properties": 
                    "version": {
                        "type": "string",
                        "description": "發行版本"
                    },
                    "UID": {
                        "type": "string",
                        "description": "唯一辨識碼"
                    },
                    "title": {
                        "type": "string",
                        "description": "活動名稱"
                    },
                    "category": {
                        "type": "string",
                        "description": "活動類別 1:音樂 2:戲劇 3:舞蹈 4:親子 5:獨立音樂 6:展覽 7:講座 8:電影 11:綜藝 13:競賽 14:徵選 15:其他 17:演唱會 19:研習課程 200:閱讀"
                    },
                    "showInfo": {
                        "type": "array",
                        "description": "活動場次資訊",
                        "items": {
                            "$ref": "#/components/schemas/ShowInfo"
                        }
                    },
                    "showUnit": {
                        "type": "string",
                        "description": "演出單位"
                    },
                    "discountInfo": {
                        "type": "string",
                        "description": "折扣資訊"
                    },
                    "descriptionFilterHtml": {
                        "type": "string",
                        "description": "簡介說明"
                    },
                    "imageUrl": {
                        "type": "string",
                        "description": "圖片連結"
                    },
                    "masterUnit": {
                        "type": "array",
                        "description": "主辦單位",
                        "items": {
                            "type": "string"
                        }
                    },
                    "subUnit": {
                        "type": "array",
                        "description": "協辦單位",
                        "items": {
                            "type": "string"
                        }
                    },
                    "supportUnit": {
                        "type": "array",
                        "description": "贊助單位",
                        "items": {
                            "type": "string"
                        }
                    },
                    "otherUnit": {
                        "type": "array",
                        "description": "其他單位",
                        "items": {
                            "type": "string"
                        }
                    },
                    "webSales": {
                        "type": "string",
                        "description": "售票網址"
                    },
                    "sourceWebPromote": {
                        "type": "string",
                        "description": "推廣網址"
                    },
                    "comment": {
                        "type": "string",
                        "description": "備註"
                    },
                    "editModifyDate": {
                        "type": "string",
                        "description": "編輯時間"
                    },
                    "sourceWebName": {
                        "type": "string",
                        "description": "來源網站名稱"
                    },
                    "startDate": {
                        "type": "string",
                        "description": "活動起始日期"
                    },
                    "endDate": {
                        "type": "string",
                        "description": "活動結束日期"
                    },
                    "hitRate": {
                        "type": "integer",
                        "description": "點閱數",
                        "format": "Int32"
                    }