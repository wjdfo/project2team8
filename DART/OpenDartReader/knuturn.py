import pandas as pd
import json
import knuturn_method as km

a = km.knuturn('./dart_api_key.txt') # 생성자 parameter : api key text file path
d = a.getReportCode('./kospi_top_30.txt') # param : 회사이름 담긴 text file path

with open('./20230101_20240329_report.json', 'w', encoding = 'utf-8')  as f :
    json.dump(d, f, ensure_ascii=False, indent = '\t')