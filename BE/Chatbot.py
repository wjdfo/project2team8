from Knuturn import Knuturn
from Dart import Dart

class Chatbot(Knuturn) :
    def __init__(self) :
        #self.gpt_model_name = 'gpt-3.5-turbo'
        #self.context = ""
        self.dart = Dart()

    def getCorpList(self, option : bool) : # false : dart / true : edgar
        # case : dart
        if not option :
            return self.dart.getCorpList()
        
        # case : edgar
        else :
            return
        
    def getResponse(self, question : str, option : bool) :
    
        return
    
    def getCorpSummary(self, corp_name : str, option : bool) :

        return
    
    def getCorpReport(self, corp_name : str, option : bool) :

        return
    
    def Compare2Corps(self, corp_list : list, option : bool) :

        return