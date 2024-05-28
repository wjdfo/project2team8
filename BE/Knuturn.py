import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from openai import OpenAI as op
import os

class Knuturn :
    def __init__(self) :
        self.gpt_model = 'gpt-3.5-turbo'
        with open('./api_key/GPT_API_KEY.txt', 'r') as f :
            self.GPT_API_KEY = f.readline()

        self.client = op(api_key = self.GPT_API_KEY)
        os.environ['OPENAI_API_KEY'] = self.GPT_API_KEY

        # self.db_path = "./VectorDB"
        self.db_path = "./testDB1"

        qna_table = "qna_test51535135151351"
        summary_table = "sum"
        question_table = "question_test541515151515"
        # self.collection_name = "knuturn"
        # self.EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'
        self.EMBEDDING_MODEL = 'snunlp/KR-SBERT-V40K-klueNLI-augSTS'

        client = chromadb.PersistentClient(path = self.db_path)
        qna_collection = client.get_or_create_collection(name = qna_table, metadata={'hnsw:space': 'cosine'})
        summary_collection = client.get_or_create_collection(name = summary_table, metadata={'hnsw:space': 'cosine'})
        question_collection = client.get_or_create_collection(name = question_table, metadata={'hnsw:space': 'cosine'})
        self.embed_model = LangchainEmbedding(
                                HuggingFaceEmbeddings(model_name = self.EMBEDDING_MODEL)
                            )
        self.qna_vector_store = ChromaVectorStore(chroma_collection = qna_collection)
        self.summary_vector_store = ChromaVectorStore(chroma_collection = summary_collection)
        self.question_vector_store = ChromaVectorStore(chroma_collection = question_collection)
        self.qna_index = VectorStoreIndex.from_vector_store(vector_store=self.qna_vector_store, embed_model=self.embed_model)
        self.summary_index = VectorStoreIndex.from_vector_store(vector_store=self.summary_vector_store, embed_model=self.embed_model)
        self.question_index = VectorStoreIndex.from_vector_store(vector_store=self.question_vector_store, embed_model=self.embed_model)