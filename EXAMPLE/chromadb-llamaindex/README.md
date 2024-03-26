# 설치
pip install -r requirements.txt

# 실행
dustmq.py 실행 

-> data 폴더 내에 있는 .txt 파일들 가져와서 chromadb에 저장 -> query 주면 알아서 참조하여 대답해 줌

# 주의
꼭 같은 폴더 내에서 실행시켜야함 ( 상대 경로 있어서 )

# 참조
chromadb와 그를 다룰 수 있는 프레임워크 llamaindex 이용했음.

https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/

https://www.trychroma.com/

https://docs.llamaindex.ai/en/stable/examples/llm/openai/

https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_context/