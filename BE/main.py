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
    corp_report_code['삼성전자'] = corp_report_code['삼성전자'][:1]
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
    end =  time.time()
    print(f"챗봇 테스트 getCorpList test {end-start :.5f}초 소요")

    start = time.time()
    corp_report_data = dart_test(corp_list[:1])
    print(corp_report_data)
    end =  time.time()
    print(f"dart api data 하나 가져오는데 {end-start :.5f}초 소요")

    print("data pipeline test")
    print("\n\n")

    start = time.time()
    d.report_summary(corp_report_data, True)
    print("\n\nsummary table insert complete\n\n")
    end =  time.time()
    print(f"data pipeline 한 기업 보고서 요약 & 적재하는데 {end-start :.5f}초 소요")

    start = time.time()
    q.insertQnA(question_dict)
    q.insertCheck("삼성전자", "임직원 정보")
    end =  time.time()
    print(f"VectorDB 접근해서 요약된 데이터 가져오오고 그 데이터 기반으로 질문 후 답변 가져오는데 {end-start :.5f}초 소요")