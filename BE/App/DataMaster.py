from BEMethods.edgar_crawler import EDGAR_Crawler
from BEMethods.edgar_extractor import EDGAR_Extractor
from BEMethods.Dart import Dart
from BEMethods.DataPipeline import DataPipeline
from BEMethods.QnA import QnA
from BEMethods.Edgar import Edgar

import json
import os

def dart_loader():
    '''
    function which do store DART data to json files
    
    -> JSON files
    '''
    dart_dataset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BEMethods/dart-datasets')
    dart = Dart()

    print("회사 리스트 ...")

    corp_list = [ "삼성전자", "SK하이닉스", "LG에너지솔루션", "삼성바이오로직스", "현대자동차",
            "POSCO홀딩스", "삼성SDI", "LG화학", "NAVER", "KB금융", "에코프로비엠", "현대모비스",
            "신한지주", "포스코퓨처엠", "삼성생명", "하나금융지주", "에코프로", "메리츠금융지주",
            "LG전자", "LG",
            "HLB", "카카오뱅크", "한미반도체"
        ]

    print("공시보고서 코드 ...")
    corp_report_code = dart.getReportCode(corp_list,'2019','2023')
    if not corp_report_code :
        return None

    print("공시보고서 링크 ...")
    corp_report_url, whole_corp_report_url = dart.getReportURL(corp_report_code)
    if not corp_report_url:
        return None
        
    indices = []

    print("사업보고서 크롤링 데이터")
    dart_index_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BEMethods/ref/index.txt')
    with open(dart_index_path, "r", encoding = 'utf-8') as f :
        lines = f.readlines()
        for line in lines :
            indices.append(line.strip("\n"))

    corp_report_data = dart.getSelectiveReportData(corp_report_url, indices)

    if not os.path.isdir(dart_dataset_path):
        os.mkdir(dart_dataset_path)

    for report_company in corp_report_url.keys():
        json_filename = f'{report_company}_report.json'
        absolute_json_filename = os.path.join(
            dart_dataset_path , json_filename
        )


        with open(absolute_json_filename, "w", encoding='UTF-8') as filepath:
            d = {}
            d[report_company] = corp_report_data[report_company]
            json.dump(d, filepath, ensure_ascii=False, indent='\t')

    print("기업별 보고서 링크")
    i = 0
    for corp in corp_report_url.keys() :
        print(f"{corp}, {whole_corp_report_url[i]}")
        i += 1

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


def makeQuestionDict():
    '''
    read question_list.txt & integrate it with corpList

    return dict
    '''

    # question list 받아오기
    question_dict = {}

    question_set_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BEMethods/question_list.txt')
    with open(question_set_path, 'r',encoding = 'utf-8') as question_set_file:
        question_list = question_set_file.readlines()

    # \n 삭제
    for i in range(len(question_list)):
        question_list[i] = question_list[i][:-1]
    

    # Dart corp_list 처리
    dart_corp_list = [ "삼성전자", "SK하이닉스", "LG에너지솔루션", "삼성바이오로직스", "현대자동차",
            "POSCO홀딩스", "삼성SDI", "LG화학", "NAVER", "KB금융", "에코프로비엠", "현대모비스",
            "신한지주", "포스코퓨처엠", "삼성생명", "하나금융지주", "에코프로", "메리츠금융지주",
            "LG전자", "LG",
            "HLB", "카카오뱅크", "한미반도체"
        ]
        
    for corp_name in dart_corp_list:
        question_dict[corp_name] = question_list

    # Edgar corp_list 처리
    edgar = Edgar()
    edgar_corp_list = edgar.getCorpList()
    for corp_name in edgar_corp_list:
        question_dict[corp_name] = question_list
    
    return question_dict



if __name__ == "__main__":
    
    print('initiate DataMaster.py')

    ############################################################
    ################ CRAWL & JSONified store ###################
    ############################################################
    # DART
    dart_loader()

    # EDGAR
    edgar_loader()

    print('CRAWL done . . . ')

    ############################################################
    ############ STORE in DB : summary #########################
    ############################################################
    raw_report_store = DataPipeline()
    
    # DART
    
    dart_dataset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BEMethods/dart-datasets')

    store_summary_to_db(raw_report_store,dart_dataset_path, True)

    # EDGAR
    
    edgar_dataset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BEMethods/edgar-datasets/EXTRACTED_FILINGS')
    store_summary_to_db(raw_report_store,edgar_dataset_path,False)
    
    print('Summary done . . . ')
    
    ############################################################
    ################ STORE in DB : estimated QnA ###############
    ############################################################
    
    estimated_qna_store = QnA()

    question_dict = makeQuestionDict()
    estimated_qna_store.insertQnA_GPT(question_dict)

    print('Estimated QnA done . . . ')
    print('Bye ! ')