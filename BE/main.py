'''
Backend
'''

import Dart

a = Dart.Dart()
corp_list = a.getCorpList()
print("회사 리스트")
print(corp_list[88270])

corp_report_code = a.getReportCode(corp_list[88270])
print("공시보고서 코드")
print(corp_report_code)

corp_report_url = a.getReportURL(corp_report_code)
print("공시보고서 링크")
print(corp_report_url)

corp_report_data = a.getEveryReportData(corp_report_url)
print("사업보고서 크롤링 데이터")
print(corp_report_data)
