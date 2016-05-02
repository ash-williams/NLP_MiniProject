from crawler import linkcrawler

crawled_count = linkcrawler.crawlSite()

print("No. of links crawled: " + str(crawled_count))