from edgar import Company, XBRL, XBRLElement

company = Company("Apple Inc.", "0000320193")

# 특정 날짜 범위 내의 10-K 보고서 가져오기
# documents = company.get_10Ks(filing_type="10-K", prior_to="20210101", count=5)
# documents = company.get_10K()
documents = company.get_data_files_from_10K("EX-101.INS", isxml=True)

# XBRL 데이터 가져오기
# for doc in documents:
#     xbrl = XBRL(doc)
#     xbrl_data = xbrl.xbrl
#     print(xbrl_data)

xbrl = XBRL(documents[0])
XBRLElement(xbrl.relevant_children_parsed[15]).to_dict()