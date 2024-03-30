# OpenDartReader
OpenDartReader는 Open DART를 내용을 일반화하고 좀 더 쉽게 Open DART를 사용하기 위한 파이썬 라이브러리 입니다.
https://nbviewer.org/github/FinanceData/OpenDartReader/blob/master/docs/OpenDartReader_users_guide.ipynb

# 설치
> pip install opendartreader

# 업그레이드
> pip install --upgrade opendartreader

# 공시 정보 list()
> 지정한 회사의 보고서를 검색. 기간과 보고서의 종류를 지정 가능.

> dart.list(corp, start=None, end=None, kind='', kind_detail='', final=True)

* 날짜 지정하는 방법
> start와 end에 지정하는 날짜의 형식 '2020-07-01', '2020-7-1', '20200701', '1 july 2020', 'JULY 1 2020' 모두 가능합니다. datetime 객체도 가능.

> start 와 end를 함께 지정하면 start~end 기간을 지정.
start만 지정하면 start 부터 현재까지,
end만 지정하면 end 하루를 지정하게 됩니다.

> 회사 지정하지 않으면 모든 종목에 대한 공시 검색(이 때, 검색 기간은 start와 end 사이의 3개월 이내 범위만 가능)

# 기업개황 company(corp_code), company_by_name(corp_name)
> pandas data frame 형식으로 기업개황 정보 return

# 공시서류 원문 document(report_code)
> str 형식의 xml text 출력

# 고유 번호 corp_codes
> find_corp_code()를 이용해 특정 회사의 고유 번호 얻기 가능
>   > dart.find_corp_code(corp_code)
>   > dart.find_corp_code(corp_name)

# 사업보고서 report()
> 사업보고서의 주요 내용을 조회.

> dart.report(corp, key_word, bsns_year, reprt_code='11011')
>   > key_word는 ODR_type.json에 있음
>   > bsns_year 에 사업 년도를 지정 (문자열 혹은 정수값)
>   > reprt_code 에는 보고서 코드(문자열)을 지정
>   >   >'11013'=1분기보고서, '11012'=반기보고서, '11014'=3분기보고서, '11011'=사업보고서

# 상장기업 재무정보 finstate()
>   dat.finstate(corp, bsns_year, reprt_code)

# 지분공시 major_shareholders()
>   dart.major_shareholders(corp) - 대량보유 상황보고
>   dart.major_shareholders_exec(corp) - 임원ㆍ주요주주 소유보고

# 주요사항보고서 event()
>   dart.event(corp, event, start=None, end=None)

# 증권신고서 regstate()
>   dart.regstate(corp, key_word, start=None, end=None)

# 확장기능
* 지정한 날짜의 공시목록 전체 (시간 정보 포함)
* * dart.list_date_ex('2022-01-03')

> rcp_no = '20220308000798' ← 삼성전자 2021년 사업보고서
> * dart.sub_docs(rcp_no) 개별 문서 제목과 URL 출력