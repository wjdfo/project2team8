'''
Backend
'''

import Dart

def test() :
    a = Dart.Dart()

    print("회사 리스트")
    corp_list = a.getCorpList()
    print(len(corp_list))

    print("공시보고서 코드")
    corp_report_code = a.getReportCode(corp_list)
    if  len(corp_report_code) == 0 :
        return None
    print(corp_report_code)

    print("공시보고서 링크")
    corp_report_url = a.getReportURL(corp_report_code)
    if len(corp_report_url) == 0 :
        return None
    print(corp_report_url)

    print("사업보고서 크롤링 데이터")
    corp_report_data = a.getEveryReportData(corp_report_url)
    print(corp_report_data)


import edgar_crawler
import edgar_extractor

def edgar_test():
    crawler = edgar_crawler.EDGAR_Crawler()
    crawler.doCrawl()

    extractor = edgar_extractor.EDGAR_Extractor()
    extractor.doExtractFromRAWs()




if __name__ == "__main__" :
    test()

    edgar_test()