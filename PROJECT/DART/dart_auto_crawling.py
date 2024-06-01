import dart_fss as dart
from bs4 import BeautifulSoup
import pandas as pd

apiKey = 'DART_API_KEY'
dart.set_api_key(api_key=apiKey)

corps = dart.get_corp_list()

# 상장종목과 비상장종목 데이터를 pandas DataFrame으로 변경
df = pd.read_csv('/상장종목.csv') # 알맞는 주소 설정
ndf = pd.read_csv('/비상장종목.csv') # 알맞는 주소 설정

# DataFrame에서 기업명을 리스트로 추출
corp_name_list = df['corp_name'].tolist()
non_corp_name_list = ndf['corp_name'].tolist()

# 검색할 시작 날짜를 설정
time = '20100101'

# 상장 기업 목록을 순회하며 각 기업의 최신 보고서 조회
for corp in corp_name_list:
    corperation = corps.find_by_corp_name(corp, exactly=True)[0]
    print(corperation)

    # 해당 기업의 공시 정보를 검색
    try:
        filings = corperation.search_filings(bgn_de=time, pblntf_detail_ty='a001')
        recentReport = filings[0]

    # 해당 기업의 데이터가 존재하지 않을 때의 예외처리
    except Exception as e:
        print(f"{corp}에 대한 조회된 데이터가 없습니다.")
        continue

    # 보고서의 내용을 파싱
    for i in range(len(recentReport)):
        soup = BeautifulSoup(recentReport[i].html, features="lxml")
        # 불필요한 태그를 제거
        scriptTag = soup.find_all(['script', 'style', 'header', 'footer', 'form'])

        for script in scriptTag:
            script.extract()
        
        # HTML에서 텍스트 내용만 추출
        content = soup.get_text(' ', strip=True)
      
        print(recentReport[i].title + ": \n")
        print(content)

# 비상장 기업 목록에 대해서도 동일한 작업을 수행
for corp in non_corp_name_list:
    corperation = corps.find_by_corp_name(corp, exactly=True)[0]
    print(corperation)
    try:
        filings = corperation.search_filings(bgn_de=time, pblntf_detail_ty='a001')
        recentReport = filings[0]

    except Exception as e:
        print(f"{corp}에 대한 조회된 데이터가 없습니다.")
        continue

    for i in range(len(recentReport)):
        soup = BeautifulSoup(recentReport[i].html, features="lxml")
        scriptTag = soup.find_all(['script', 'style', 'header', 'footer', 'form'])

        for script in scriptTag:
            script.extract()
        
        content = soup.get_text(' ', strip=True)
      
        print(recentReport[i].title + ": \n")
        print(content)

# 기업 코드를 통한 검색
corp_code_list = df['corp_code'].tolist()
non_corp_code_list = ndf['corp_code'].tolist()

time = '20100101'
for corp in corp_code_list:
    corperation = corps.find_by_corp_code(str(corp))
    print(corperation)
    try:
        filings = corperation.search_filings(bgn_de=time, pblntf_detail_ty='a001')
        recentReport = filings[0]

    except Exception as e:
        continue

    for i in range(len(recentReport)):
        soup = BeautifulSoup(recentReport[i].html, features="lxml")
        scriptTag = soup.find_all(['script', 'style', 'header', 'footer', 'form'])

        for script in scriptTag:
            script.extract()
        
        content = soup.get_text(' ', strip=True)
      
        print(recentReport[i].title + ": \n")
        print(content)
