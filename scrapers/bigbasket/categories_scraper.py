import json

from utils.http_req_res import getData
from utils.file_io import createFiles, writeLineData, getBBCategoriesFileName


class BigBasketCategoriesScraper:
    CATEGORIES_URL = "https://www.bigbasket.com/auth/get_menu/?city_id=1"
    CATEGORIES_FILE_HEADER = "CATEGORY ID,CATEGORY NAME,CATEGORY SLUG,URL\n"

    def __init__(self):
        createFiles(getBBCategoriesFileName(), self.CATEGORIES_FILE_HEADER)
        createFiles(getBBCategoriesFileName("json"))

    def getCategories(self):
        categories = {}

        print("*" * 10)
        print("Fetching Categories : ")
        print("*" * 10)

        data = getData(self.CATEGORIES_URL)
        writeLineData(getBBCategoriesFileName("json"), json.dumps(data))

        cats = data["topcats"]

        for cat in cats:
            top_category = cat["top_category"]
            categories[top_category["id"]] = {"slug": top_category["slug"], "name": top_category["name"]}

            # Writing data to Categories file
            category_data = str(top_category["id"]) + "," + top_category["name"].replace(",","") + "," + top_category["slug"] + "," + top_category["url"] + "\n"
            writeLineData(getBBCategoriesFileName(), category_data)

            # Fetching Sub-Categories
            sub_cats = cat["sub_cats"][0]
            for sub_cat in sub_cats:
                sub_category = sub_cat["sub_category"]
                category_data = str(top_category["id"]) + "," + sub_category[0].replace(",","") + "," + sub_category[1] + "," + sub_category[2] + "\n"
                writeLineData(getBBCategoriesFileName(), category_data)

                for cat in sub_cat["cats"]:
                    catie = cat["cat"]
                    category_data = str(top_category["id"]) + "," + catie[0].replace(",","") + "," + catie[1] + "," + \
                                    catie[2] + "\n"
                    writeLineData(getBBCategoriesFileName(), category_data)

        return categories
