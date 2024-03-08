#open API key는
#https://opendart.fss.or.kr/uss/umt/EgovMberInsertView.do
#에서 신청가능

########################
import dart_fss as dart

apiKey = '45e284591cad627ed6b7b278608bbe5b81f6893d'
dart.set_api_key(api_key=apiKey)

# dart에 상장된 기업 중 삼성전자 검색
corps = dart.get_corp_list()
samsung = corps.find_by_corp_name('삼성전자', exactly=True)[0]

# 20100101 부터 지금까지 연간 사업보고서 가져오기 // a001 == 사업보고서
filings = samsung.search_filings(bgn_de='20100101', pblntf_detail_ty='a001')

# 가장 최신 보고서 (2023사업보고서)
recentReport = filings[0]

# 사업보고서 출력
# recent_report의 type == 'dart_fss.filings.reports.Report'
# recent_report의 요소의 type == 'dart_fss.filings.pages.Page'

# print(help('dart_fss.filings.reports.Report'))
# print(help('dart_fss.filings.pages.Page'))
# 상기 help들로 메소드 찾아보세요.


# 삼성전자 2023 사업보고서 : https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20230307000542

# 사업보고서 목차
print(recentReport.pages)
print()
# 사업보고서 중 일부 내용
print(recentReport[3].html)