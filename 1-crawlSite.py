from crawler import linkcrawler

crawled_count = linkcrawler.crawlSite()

print("No. of links crawled: " + str(crawled_count))

retrieved = linkcrawler.getcontent()

print("No. of pages retrieved: " + str(retrieved))
