from edgar import Company, XBRL, XBRLElement

company = Company("Apple Inc.", "0000320193")
results = company.get_data_files_from_10K("EX-101.INS", isxml=True)
xbrl = XBRL(results[0])
XBRLElement(xbrl.relevant_children_parsed[15]).to_dict()
# returns a dictionary of name, value, and schemaRef