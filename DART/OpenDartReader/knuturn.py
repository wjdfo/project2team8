import pandas as pd
import json
import knuturn_method

#필요한 함수 주석 해제해서 쓰세요

a = knuturn_method.knuturn('./dart_api_key.txt') # param : api key text file path

companies = []

f = open('./kospi_top_30.txt', 'r', encoding = 'utf-8')
lines = f.readlines()

for line in lines :
    companies.append(line.strip())


# 회사 고유코드 얻어오는 method <- report_list.json 파일 없을 때 사용
# report_list = a.getReportCode(companies) # param : 회사 리스트

# with open('./20230101_20240329_report_list.json', 'w', encoding = 'utf-8')  as f : # report list json 파일로 저장
#     json.dump(report_list, f, ensure_ascii=False, indent = '\t')



#이미 report_list.json 파일 있는 경우 사용
with open('./20230101_20240329_report_list.json', 'r', encoding = 'utf-8')  as f :
    report_list = json.load(f)



# 회사 고유코드로 사업보고서 url 가져오는 method <- report_url.json 파일 없을 때 사용
# report_url = a.getReportURL(report_list) # param : report num dict

# with open('./20230101_20240329_report_url.json', 'w', encoding = 'utf-8')  as f : # report url json 파일로 저장
#     json.dump(report_url, f, ensure_ascii=False, indent = '\t')



#이미 report_url.json 파일 있는 경우 사용
with open('./20230101_20240329_report_url.json', 'r', encoding = 'utf-8') as f :
    report_url = json.load(f)

report_data = a.getReportData2(report_url)

with open('./20230101_20240329_report_data.json', 'w', encoding = 'utf-8') as f :
    json.dump(report_data, f, ensure_ascii = False, indent = '\t')


# xml to json
# pip install xmltodict

# import xmltodict

# jsonString = json.dumps(xmltodict.parse(xml_text), indent='\t', ensure_ascii=False)

# print("\nJSON output(output.json):")
# print(jsonString)

# with open("xml_to_json.json", 'w', encoding='utf-8') as f:
#     f.write(jsonString)