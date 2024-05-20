'''
Backend
'''

import Dart
from DataPipeline import DataPipeline
from Chatbot import Chatbot
# import edgar_crawler
# import edgar_extractor

def dart_test() :
    a = Dart.Dart()

    print("회사 리스트")
    corp_list = a.getCorpList()
    print(len(corp_list))

    print("공시보고서 코드")
    corp_report_code = a.getReportCode(corp_list)
    if  not corp_report_code :
        return None
    print(corp_report_code)

    print("공시보고서 링크")
    corp_report_url = a.getReportURL(corp_report_code)
    if not corp_report_url:
        return None
    print(corp_report_url)

    print("사업보고서 크롤링 데이터")
    corp_report_data = a.getEveryReportData(corp_report_url)
    print(corp_report_data)

# def edgar_test():
#     crawler = edgar_crawler.EDGAR_Crawler()
#     crawler.doCrawl()

#     extractor = edgar_extractor.EDGAR_Extractor()
#     extractor.doExtractFromRAWs()

import time
import json

if __name__ == "__main__" :
    # a = DataPipeline()

    # # dart_test()

    # # edgar_test()
    # with open("./text.json", "r", encoding = 'utf-8') as f:
    #     report_data = json.load(f)

    # print(a.report_summary(report_data, 1))
    start = time.time()
    a = Chatbot()
    print(a.getCorpReport(corp_name="삼성전자", isDart = True, date = (2023, 2024)))
    end =  time.time()
    print(f"{end-start :.5f}초 소요")