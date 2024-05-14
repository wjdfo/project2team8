from Knuturn import Knuturn
from Dart import Dart

class Chatbot(Knuturn) :
    def __init__(self) :
        #self.gpt_model_name = 'gpt-3.5-turbo'
        #self.context = ""
        self.dart = Dart()

    def getCorpList(self, isDart : bool) : # true : dart / false : edgar
        # case : dart
        if isDart :
            return self.dart.getCorpList()
        
        # case : edgar
        else :
            return
        
    def getResponse(self, question : str, isDart : bool) :
        # 사용자의 질문을 받아서 qna table에 query

        # # Dart
        # if isDart :

        # # Edgar
        # else :

        return

    def getCorpSummary(self, corp_name : str, isDart : bool, report_num : str = None) :
        # summary table에 query

        # # Dart
        # if isDart :

        # # Edgar
        # else :

        return
    
    def getCorpReport(self, corp_name : str, isDart : bool, date : tuple = None) :
        # Dart
        if isDart :
            report_dict = self.dart.getReportCode([corp_name])
            report = self.dart.getReportURL(report_dict)

        # # Edgar
        # else :

        return report
    
    def Compare2Corps(self, corp_list : tuple, isDart : bool) :
        corp1, corp2 = corp_list[0], corp_list[1]
        # summary table에 두 회사 query

        # Dart
        # if isDart :

        # # Edgar
        # else :
            
        return