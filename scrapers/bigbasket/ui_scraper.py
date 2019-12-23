from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup  # HTML data structure


class BigBasketUIScraper:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    req_url = "https://bigbasket.com/"
    selector_string='li.hvr-drop'

    def __init__(self):
        self.getDataSoup()

    # Creates Page soup, which in-turn is used for traversing HTML
    def getDataSoup(self):
        req = Request(url=self.req_url, headers=self.headers)

        # opens the connection and downloads html page from url
        uClient = urlopen(req)
        html = uClient.read()

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        self.page_soup = soup(html, "html.parser")
        uClient.close()

    def scrape(self):
        # traversing html for interested elements
        temp = self.page_soup.select(self.selector_string)
        print(temp)

        # return self.getCategories(categoryElements)

    def getCategories(self, categoryElements):
        categoryDict = {}

        for categoryElement in categoryElements:
            categoryPath = categoryElement.get('href')
            categoryId = categoryPath.split('/')[-1]
            categoryDict[categoryId] = categoryPath

        return categoryDict