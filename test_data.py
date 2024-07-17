import pandas as pd
import json
import os

data = pd.read_json('data.json')

data.columns

# UID is pk

data.showInfo


df_event = data[['UID',
'title',
'category',
'descriptionFilterHtml',
'discountInfo',
'imageUrl',
'startDate',
'endDate',
'hitRate',
'showInfo']]

