import edgar_crawler
import extract_items

inst = edgar_crawler.Crawler()
inst.doCrawl()

dest = extract_items.Edgar_Extractor()
dest.doExtractFromRAWs()