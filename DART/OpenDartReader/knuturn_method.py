import OpenDartReader
import pandas as pd
import json

class knuturn :
    def __init__(self, file: str) :
        with open('./dart_api_key.txt', 'r') as f :
            api_key = f.readline()
        self.dart = OpenDartReader(api_key)

    def getReportCode(self, corp_file: str) : #공시보고서 코드를 회사마다 dictionary에 담아서 return
        companies = []
        d = {}

        f = open('./kospi_top_30.txt', 'r', encoding = 'utf-8')
        lines = f.readlines()

        for line in lines :
            companies.append(line.strip())

        for comp in companies :
            print(comp, end = " ")
            try : # dart.list 함수 호출했을 때, data 없는 경우에도 exception raise하지 않고 {"status":"013","message":"조회된 데이타가 없습니다."} 출력하는 오류 있습니다.
                report_list = self.dart.list(comp, start = '2023-01-01', end = '2024-03-28', kind = 'A')
                corp_code = report_list['corp_code'][0]
                d[corp_code] = []
                for report_code in report_list['rcept_no'] :
                    d[corp_code].append(report_code)
                print()
            except :
                continue
        
        return d