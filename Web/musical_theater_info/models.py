from django.db import models

class ModelActivity(models.Model):
    # 定義模型欄位，與現有資料表格對應
    id = models.IntegerField(primary_key=True)
    UID = models.CharField(max_length=255)
    version = models.CharField(max_length=50) 
    title = models.CharField(max_length=255)
    category = models.IntegerField()
    showUnit = models.CharField(max_length=255)
    discountInfo = models.CharField(max_length=255)
    descriptionFilterHtml = models.CharField(max_length=255)
    imageUrl = models.CharField(max_length=255)
    masterUnit = models.CharField(max_length=255)
    subUnit = models.CharField(max_length=255)
    supportUnit = models.CharField(max_length=255)
    otherUnit = models.CharField(max_length=255)
    webSales = models.CharField(max_length=255)
    sourceWebPromote = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    editModifyDate = models.DateTimeField()
    sourceWebName = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    hitRate = models.IntegerField()

    class Meta:
        # 設定資料表格名稱，如果資料庫中表格名稱與 Django 慣例不同，可以在這裡指定
        db_table = 'musicial_activity'


class ModelShowInfo(models.Model):
    # 定義模型欄位，與現有資料表格對應
    id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField()
    location_id = models.IntegerField() 
    time = models.DateTimeField()
    onSales = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    endTime = models.DateTimeField(max_length=255)

    class Meta:
        # 設定資料表格名稱，如果資料庫中表格名稱與 Django 慣例不同，可以在這裡指定
        db_table = 'musicial_showinfo'
