from edgar_crawler import EDGAR_Crawler
from edgar_extractor import EDGAR_Extractor
from Dart import Dart
from DataPipeline import DataPipeline
from QnA import QnA

import json
import os

def dart_loader():
    '''
    function which do store DART data to json files
    
    -> JSON files
    '''
    dart_dataset_path = './dart-datasets'
    dart = Dart()

    print("회사 리스트 ...")
    corp_list = [ "삼성전자", "SK하이닉스", "LG에너지솔루션", "삼성바이오로직스", "현대자동차",
            "POSCO홀딩스", "삼성SDI", "LG화학", "NAVER", "KB금융", "에코프로비엠", "현대모비스",
            "신한지주", "포스코퓨처엠", "삼성생명", "하나금융지주", "에코프로", "메리츠금융지주",
            "LG전자", "LG",
            "HLB", "카카오뱅크", "한미반도체" ]



    print("공시보고서 코드 ...")
    corp_report_code = dart.getReportCode(corp_list,'2019','2023')
    if not corp_report_code :
        return None

    print("공시보고서 링크 ...")
    corp_report_url, _ = dart.getReportURL(corp_report_code)
    if not corp_report_url:
        return None
        
    print("사업보고서 크롤링 데이터 ...")
    corp_report_data = dart.getEveryReportData(corp_report_url)


    if not os.path.isdir(dart_dataset_path):
        os.mkdir(dart_dataset_path)

    for report_company in corp_list:
        json_filename = f'{report_company}_report.json'
        absolute_json_filename = os.path.join(
            dart_dataset_path , json_filename
         )


        with open(absolute_json_filename, "w", encoding='UTF-8') as filepath:
            d = {}
            d[report_company] = corp_report_data[report_company]
            json.dump(d, filepath, ensure_ascii=False, indent='\t')




def edgar_loader():
    '''
    function which do store EDGAR data to json files
    options based on `config.json`
    
    -> JSON files
    '''
    
    e_crawler = EDGAR_Crawler()
    e_crawler.doCrawl()
    e_extractor = EDGAR_Extractor()
    e_extractor.doExtractFromRAWs()

def store_summary_to_db(raw_report_store : DataPipeline, path : str, isDart : bool):
    '''
    get path of json files
    store them to chromadb summary_collection

    isDart == True : dart
    '''

    json_list = os.listdir(path)
    for i in json_list:
        json_path = os.path.join(path,i)
        with open(json_path, "r", encoding = 'utf-8') as f:
            report_data = json.load(f)
            raw_report_store.report_summary(report_data,isDart)



if __name__ == "__main__":
    ############ CRAWL & JSONified store ##############
    '''
    dart_loader()
    edgar_loader()
    '''

    ############ STORE in DB : summary #########################
    
    '''
    raw_report_store = DataPipeline()
    '''
    # EDGAR
    ''' 
    path = './edgar-datasets/EXTRACTED_FILINGS'
    store_summary_to_db(raw_report_store,path,False)
    '''

    # DART
    '''
    path = './dart-datasets'
    store_summary_to_db(raw_report_store,path,True)
    '''

    ################ STORE in DB : estimated QnA ############################

    estimated_qna_store = QnA()
    
    question_dict = {
        "삼성전자 요즘 어떤 제품으로 사업해?" : {
                "corp_name" : "삼성전자"
        }
    }



    estimated_qna_store.insertQnA(question_dict)