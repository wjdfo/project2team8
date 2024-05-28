import OpenDartReader
import dart_fss
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

class Dart :
    def __init__(self) :
        with open('./api_key/dart_api_key.txt', 'r') as api_key_file :
            dart_api_key = api_key_file.readline()
        self.dart = OpenDartReader(dart_api_key)
        dart_fss.set_api_key(api_key = dart_api_key)
        
    def getCorpList(self) :
        f = open("./ref/dart_corp_name_code_mapping.txt", 'w', encoding = 'utf-8')

        corp_list = dart_fss.api.filings.get_corp_code()
        df = pd.DataFrame(corp_list)
        stock_list = df[df['stock_code'].notnull()]

        for idx, corp in stock_list.iterrows() :
            f.write(f"{corp['corp_code']} {corp['corp_name']}\n")
        print("corp_name_code_mapping file created.")

        f.close()

        return stock_list['corp_name'].tolist()

    def getReportCode(self, comps: list, start_year, end_year) : #공시보고서 코드를 회사마다 dictionary에 담아서 return
        d = {}
        start_year += "0101"
        end_year += "1231"
        
        for comp in comps :
            print(comp, end = " ")
            try : # dart.list 함수 호출했을 때, data 없는 경우에도 exception raise하지 않고 {"status":"013","message":"조회된 데이타가 없습니다."} 출력하는 오류 있습니다.
                report_list = self.dart.list(comp, start = start_year, end = end_year, kind = 'A')
                d[comp] = []
                d[comp].append(min(report_list['rcept_no']))
                # for report_code in report_list['rcept_no'] :
                #     if int(report_code) < int(min) :
                #         min = report_code
                    
                #     # d[comp].append(report_code)
                # d[comp].append(min)
            except :
                continue
        
        return d
    
    def getReportURL(self, report_list: dict) : #report_list 받아서 공시보고서 url 생성
        if len(list(report_list.keys())) == 0 :
            print("There's no report list.")
            return None, None
        whole_report_url = []
        report_url = {}

        for corp_code in report_list.keys() :
            report_url[corp_code] = {}

            for report_num in report_list[corp_code] :
                report_url[corp_code][report_num] = {}
                report = self.dart.attach_files(report_num)
                for title, url in report.items() :
                    if url.startswith("http://dart.fss.or.kr/pdf/download/pdf") :
                        whole_report_url.append(url)
                for idx, row in self.dart.sub_docs(report_num).iterrows() :
                    report_url[corp_code][report_num][row['title']] = row['url']
            
        return report_url, whole_report_url
    
    '''
    모든 목차 가져오는 함수
    '''
    def getEveryReportData(self, report_url: dict) : #report_url_list 받아서 url에서 text 가져옴
        if len(list(report_url.keys ())) == 0 :
            print("There's no report url.")
            return None
        
        report_data = {}

        # 크롬 드라이버와 크롬 버전이 충돌하여, 직접 크롬 드라이버의 주소를 기입할 경우에 아래의 코드 사용
        # driver = webdriver.Chrome(Service(executable_path=CHROME_DRIVER_PATH))

        driver = webdriver.Chrome()

        # crawling test
        # fp = open('./crawling_output_try_2.txt', 'a', encoding = 'utf-8')

        for corp_code in report_url.keys() :
            report_data[corp_code] = {}

            for report_num in report_url[corp_code] :
                report_data[corp_code][report_num] = {}

                for title in report_url[corp_code][report_num] :
                    url = report_url[corp_code][report_num][title]
                    report_data[corp_code][report_num][title] = []
                    # fp.write(title + "\n")

                    driver.get(url)
                    time.sleep(2)

                    report_string = driver.find_element(By.TAG_NAME, 'body').text
                    lines = report_string.splitlines()

                    for line in lines :
                        if len(line) < 1 : # 빈 줄 삭제
                            continue
                        report_data[corp_code][report_num][title].append(line + "\n")
                    #     fp.write(line + "\n")
                    # fp.write("\n")
                    # print(report_string)

        driver.quit()
        # fp.close()

        return report_data
    
    def getSelectiveReportData(self, report_url: dict, indices: list) : # 목차 골라서 가져오는 함수

        # 크롬 드라이버와 크롬 버전이 충돌하여, 직접 크롬 드라이버의 주소를 기입할 경우에 아래의 코드 사용
        # driver = webdriver.Chrome(Service(executable_path=CHROME_DRIVER_PATH))

        driver = webdriver.Chrome()

        report_data = {}

        for corp_name in report_url.keys() :
            report_data[corp_name] = {}
            for report_num in report_url[corp_name] :
                report_data[corp_name][report_num] = {}

                print(report_num, end = " ")

                for title in report_url[corp_name][report_num] :
                    extract = False # 뽑아야 할 목차인지 확인하는 conditional variable
                    
                    for index in indices :
                        if index in title :
                            extract = True
                            break

                    if extract :
                        report_data[corp_name][report_num][title] = []
                        url = report_url[corp_name][report_num][title]

                        driver.get(url)
                        time.sleep(2)

                        report_string = driver.find_element(By.TAG_NAME, 'body').text

                        lines = report_string.splitlines()

                        for line in lines :
                            if len(line) < 1 :
                                continue
                            report_data[corp_name][report_num][title].append(line + '\n')
                print("done.")

        driver.quit()

        return report_data