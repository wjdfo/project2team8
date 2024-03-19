from edgar import Company, XBRL, XBRLElement

company = Company("Oracle Corp", "0001341439")
results = company.get_data_files_from_10K("10-K", isxml=True)
print(results)
# xbrl = XBRL(results[0])
# XBRLElement(xbrl.relevant_children_parsed[15]).to_dict()
# returns a dictionary of name, value, and schemaRef(스키마참조)