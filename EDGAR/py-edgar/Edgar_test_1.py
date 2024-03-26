from edgar import Company, TXTML

# 회사 이름 또는 CIK (Central Index Key)를 사용하여 Company 객체를 만듭니다.
company = Company("Apple Inc.", "0000320193")

# 특정 날짜 범위 내의 10-K 보고서 가져오기
# docs = company.get_10Ks(filing_type="10-K", prior_to="20210101", count=5)
docs = company.get_10K()

# 가져온 각 보고서의 내용 출력
for doc in docs:
    text = TXTML.parse_full_10K(doc)
    print(text)

file_path = '/Users/crossrunway/vsCODE/project2team8/EDGAR/py-edgar/test_output/example.txt' 
# 파일 경로 및 이름
with open(file_path, 'w') as file:
    for doc in docs:
        text = TXTML.parse_full_10K(doc)
        file.write(text)