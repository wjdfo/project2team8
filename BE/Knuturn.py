class Knuturn :
    def __init__(self) :
        self.gpt_model = 'gpt-3.5-turbo'
        with open('./api_key/GPT_API_KEY.txt', 'r') as f :
            self.GPT_API_KEY = f.readline()

        self.db_path = "./VectorDB"
        self.collection_name = "knuturn"