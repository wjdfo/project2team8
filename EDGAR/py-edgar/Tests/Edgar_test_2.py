from edgar import Company, TXTML

company = Company("Apple Inc.", "0000320193")
doc = company.get_10K()
text = TXTML.parse_full_10K(doc)
print(text)
file_path = '/Users/crossrunway/vsCODE/project2team8/EDGAR/py-edgar/test_output/full_10k.txt' 
# 파일 경로 및 이름
with open(file_path, 'w') as file:
    file.write(text)