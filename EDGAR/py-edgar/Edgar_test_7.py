import requests
from bs4 import BeautifulSoup

def get_xbrl_from_10k(cik, accession_number):
    # SEC API 엔드포인트 URL
    endpoint = f"https://data.sec.gov/submissions/CIK{cik}.json"

    # 보고서 accession number로 필터링
    params = {
        "type": "10-K",
        "date": "20190101-20211231",  # 보고서 날짜 범위 (예: 2019년부터 2021년까지)
        "accept": "application/json"
    }

    try:
        # SEC API에서 보고서 데이터 가져오기
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            # JSON 형식의 응답을 파싱하여 보고서 데이터 추출
            reports = response.json()
            for report in reports:
                if report['accessionNumber'] == accession_number:
                    # 해당 보고서의 URL 가져오기
                    report_url = report['url']
                    # 보고서 내용 다운로드
                    report_content = requests.get(report_url).content
                    # BeautifulSoup을 사용하여 HTML 파싱
                    soup = BeautifulSoup(report_content, 'html.parser')
                    # XBRL 데이터를 포함하는 태그(예: <xbrl> 또는 <xbrlTable>) 찾기
                    xbrl_tag = soup.find("xbrl")
                    if xbrl_tag:
                        # XBRL 데이터 출력
                        xbrl_data = xbrl_tag.get_text()
                        return xbrl_data
                    else:
                        print("보고서에 XBRL 데이터가 포함되어 있지 않습니다.")
                        return None
            print("해당 accession number의 보고서를 찾을 수 없습니다.")
        else:
            print(f"오류: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

# CIK와 Accession Number 설정
cik = "0000320193"  # Apple Inc.의 CIK
accession_number = "0000320193-21-000056"  # 예시 accession number

# 10-K 보고서에서 XBRL 데이터 가져오기
xbrl_data = get_xbrl_from_10k(cik, accession_number)
if xbrl_data:
    # XBRL 데이터 출력 또는 처리
    print(xbrl_data)
