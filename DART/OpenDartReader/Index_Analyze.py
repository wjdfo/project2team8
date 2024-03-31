import OpenDartReader
import pandas as pd
import json

with open('./dart_api_key.txt', 'r') as f :
    api_key = f.readline()
dart = OpenDartReader(api_key)

# corp_list = dart.corp_codes <- DART에 등록된 회사들 반환
companies = []

# 코스피 시총 상위 30개 회사
f = open('./kospi_top_30.txt', 'r', encoding = 'utf-8')
lines = f.readlines()

for line in lines :
    companies.append(line.strip())

d = {}
corp_code_mapping = {}

for comp in companies :
    print(comp, end = " ")
    
    try : # dart.list 함수 호출했을 때, data 없는 경우에도 exception raise하지 않고 {"status":"013","message":"조회된 데이타가 없습니다."} 출력하는 오류 있습니다.
        report_list = dart.list(comp, start = '2023-01-01', end = '2024-03-28', kind = 'A')
        corp_code = report_list['corp_code'][0]
        corp_code_mapping[corp_code] = comp
        d[corp_code] = []
        for report_code in report_list['rcept_no'] :
            d[corp_code].append(report_code)
        print()
    except :
        continue

dictionary = dict()
n = 0

a = {}

for corp_code in d.keys() :
    a[corp_code] = {}

    for report_num in d[corp_code] :
        a[corp_code][report_num] = {}
        for idx, row in dart.sub_docs(report_num).iterrows() :
            a[corp_code][report_num][row['title']] = row['url']
            

for corp_code in a.keys() :
    for report_number in a[corp_code].keys() :
        n += 1
        for title in a[corp_code][report_number].keys() :
            if title not in dictionary.keys() :
                dictionary[title] = [1, []]
                dictionary[title][1].append(corp_code_mapping[corp_code])
                
            else :
                dictionary[title][0] += 1
                dictionary[title][1].append(corp_code_mapping[corp_code])

print(f"total # of report : {n}")
for key in dictionary.keys() :
    print(f"제목 : {key}, 목차 포함 수 : {dictionary[key][0]}")
    print(set(dictionary[key][1]))
    print()

data = {}
data["제목"] = []

for corp_name in corp_code_mapping.values() :
    data[corp_name] = ['-' for _ in range(len(dictionary.keys()))]

#csv 파일로 저장
row = 0
for key in dictionary.keys() :
    data["제목"].append(key)
    for corp in set(dictionary[key][1]) :
        data[corp][row] = '★' * 5

    row += 1

df = pd.DataFrame(data)
df.set_index("제목", inplace = True)
df.head()

df.to_csv('./목차분석.csv')