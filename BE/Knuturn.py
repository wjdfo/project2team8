class Knuturn :
    def __init__(self) :
        self.gpt_model = 'gpt-3.5-turbo'
        with open('./api_key/GPT_API_KEY.txt', 'r') as f :
            self.GPT_API_KEY = f.readline()

        self.db_path = "./VectorDB"
        self.qna_table = "qna"
        self.summary_table = "sum"
        self.collection_name = "knuturn"
        self.EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'