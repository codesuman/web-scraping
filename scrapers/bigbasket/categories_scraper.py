from utils.http_req_res import getData
from utils.file_io import createFiles, writeLineData, getBBPath, getBBCategoriesFileName

class BigBasketCategoriesScraper:
    CATEGORIES_URL = "https://www.bigbasket.com/auth/get_menu/?city_id=1"
    CATEGORIES_FILE_HEADER = "CATEGORY ID,CATEGORY NAME,CATEGORY SLUG\n"

    def __init__(self):
        createFiles(getBBPath(), getBBCategoriesFileName(), self.CATEGORIES_FILE_HEADER)

    def getCategories(self):
        categories = {}

        print("*" * 10)
        print("Fetching Categories : ")
        print("*" * 10)

        data = getData(self.CATEGORIES_URL)
        cats = data["topcats"]

        for cat in cats:
            top_category = cat["top_category"]
            categories[top_category["id"]] = {"slug": top_category["slug"], "name": top_category["name"]}

            # Writing data to Categories file
            category_data = str(top_category["id"]) + "," + top_category["name"] + "," + top_category["slug"] + "\n"
            writeLineData(getBBCategoriesFileName(), category_data)

        return categories

