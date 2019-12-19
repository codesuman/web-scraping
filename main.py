from scrapers.grofers.data_scraper import GrofersDataScraper
from scrapers.grofers.ui_scraper import GrofersUIScraper

groUIScrapper = GrofersUIScraper()
categoryDict = groUIScrapper.scrape()

groDataScrapper = GrofersDataScraper(categoryDict)
groDataScrapper.scrape()
