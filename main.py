from scrapers.grofers.data_scraper import GrofersDataScraper
from scrapers.grofers.ui_scraper import GrofersUIScraper
from scrapers.bigbasket.categories_scraper import BigBasketCategoriesScraper
from scrapers.bigbasket.data_scraper import BigBasketDataScraper

def scrapeGrofersData():
    groUIScrapper = GrofersUIScraper()
    categoryDict = groUIScrapper.scrape()

    groDataScrapper = GrofersDataScraper(categoryDict)
    groDataScrapper.scrape()

def scrapeBigBasketData():
    bbCategoriesScraper = BigBasketCategoriesScraper()
    bbCategories = bbCategoriesScraper.getCategories()

    for category_id, categoryObj in bbCategories.items():
        print(f"{category_id} : {categoryObj['slug']} - {categoryObj['name']}")
        bbDataScrapper = BigBasketDataScraper(category_id, categoryObj['slug'], categoryObj['name'])
        bbDataScrapper.scrape()


scrapeBigBasketData()