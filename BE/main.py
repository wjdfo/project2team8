'''
Backend
'''

from QnA import QnA
import Dart
from DataPipeline import DataPipeline
from Chatbot import Chatbot
# import edgar_crawler
# import edgar_extractor

def dart_test(corp_list) :
    a = Dart.Dart()

    # print("회사 리스트")
    # corp_list = a.getCorpList()
    # print(len(corp_list))

    print("공시보고서 코드")
    corp_report_code = a.getReportCode(corp_list, "2023", "2023")
    if  not corp_report_code :
        return None
    print(corp_report_code)

    print("공시보고서 링크")
    corp_report_url, whole_report_data = a.getReportURL(corp_report_code)
    if not corp_report_url:
        return None
    print(corp_report_url)

    print("사업보고서 크롤링 데이터")
    corp_report_data = a.getEveryReportData(corp_report_url)
    print(corp_report_data)

    return corp_report_data

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

    d = DataPipeline()
    c = Chatbot()
    q = QnA()

    question_dict = {
        "삼성전자 어때?" :
        {
            "corp_name" : "삼성전자"
        }
    }

    start = time.time()
    print("chatbot test")
    corp_list = c.getCorpList(True)
    print(corp_list)
    print("\n\n")
    corp_report_data = dart_test(corp_list)
    print("data pipeline test")
    print(corp_report_data)
    print("\n\n")

    print("data pipeline")
    d.report_summary(corp_report_data, True)
    print("\n\nsummary table insert complete\n\n")
    answer = q.insertQnA(question_dict)
    print(f"result : {answer}\n\n")
    end =  time.time()
    print(f"{end-start :.5f}초 소요")