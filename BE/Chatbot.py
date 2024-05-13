from Knuturn import Knuturn

class Chatbot(Knuturn) :
    def __init__(self) :
        self.gpt_model_name = 'gpt-3.5-turbo'
        self.context = ""