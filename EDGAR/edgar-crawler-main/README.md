https://github.com/nlpaueb/edgar-crawler

https://github.com/nlpaueb/edgar-crawler

https://github.com/nlpaueb/edgar-crawler



## 설치 방법
- `pip install -r requirements.txt`

## 사용법
- `edgar_crawler.py` 실행 후 ( -> datasets 폴더 내 RAW_FILINGS 생성됨 확인 ) `extract_items.py` 실행 -> datasets 폴더 내 **EXTRACTED_FILINGS 폴더에 json 파일 생성됨**

- `edgar_crawler.py`와 `extract_items.py`의 인자는 `config.json` 수정해서 설정
- 수정해야할 중대인자는  `edgar_crawler.py`에서 : `start_year`, `end_year`, `filing_types`, `cik_tickers` , ( + `user_agent`는 적당히 자기 이메일 쓰면 됨 SEC에 로그 남기는 용인듯 ) `extract_items.py`에서 : `items_to_extract` 인 것으로 보임
- `items_to_extract` 옵션에 들어갈 수 있는 녀석들은  "1", "1A", "1B", "2", "3", "4", "5", "6", "7", "7A", "8", "9", "9A", "9B", "10", "11", "12", "13", "14", "15" 로, `can-be-extracted items.txt`에도 써 놓았음
- **extract_items.py는 현재 10-K 파일들(annual reports)만 지원함**

- 아래는 원문 옵션들 설명
  - Arguments for `edgar_crawler.py`, the module to download financial reports:
      - `start_year XXXX`: the year range to start from (default is 2021).
      - `end_year YYYY`: the year range to end to (default is 2021).
      - `quarters`: the quarters that you want to download filings from (List).<br> Default value is: `[1, 2, 3, 4]`.
      - `filing_types`: list of filing types to download.<br> Default value is: `['10-K', '10-K405', '10-KT']`.
      - `cik_tickers`: list or path of file containing CIKs or Tickers. e.g. `[789019, "1018724", "AAPL", "TWTR"]` <br>
        In case of file, provide each CIK or Ticker in a different line.  <br>
      If this argument is not provided, then the toolkit will download annual reports for all the U.S. publicly traded companies.
      - `user_agent`: the User-agent (name/email) that will be declared to SEC EDGAR.
      - `raw_filings_folder`: the name of the folder where downloaded filings will be stored.<br> Default value is `'RAW_FILINGS'`.
      - `indices_folder`: the name of the folder where EDGAR TSV files will be stored. These are used to locate the annual reports. Default value is `'INDICES'`.
      - `filings_metadata_file`: CSV filename to save metadata from the reports.
      - `skip_present_indices`: Whether to skip already downloaded EDGAR indices or download them nonetheless.<br> Default value is `True`.

  - Arguments for `extract_items.py`, the module to clean and extract textual data from already-downloaded 10-K reports:
    - `raw_filings_folder`: the name of the folder where the downloaded documents are stored.<br> Default value s `'RAW_FILINGS'`.
    - `extracted_filings_folder`: the name of the folder where extracted documents will be stored.<br> Default value is `'EXTRACTED_FILINGS'`.<br> For each downloaded report, a corresponding JSON file will be created containing the item sections as key-pair values.
    - `filings_metadata_file`: CSV filename to load reports metadata (Provide the same csv file as in `edgar_crawler.py`).
    - `items_to_extract`: a list with the certain item sections to extract. <br>
      e.g. `['7','8']` to extract 'Management’s Discussion and Analysis' and 'Financial Statements' section items.<br>
      The default list contains all item sections.
    - `remove_tables`: Whether to remove tables containing mostly numerical (financial) data. This work is mostly to facilitate NLP research where, often, numerical tables are not useful.
    - `skip_extracted_filings`: Whether to skip already extracted filings or extract them nonetheless.<br> Default value is `True`.

