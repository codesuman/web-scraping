import requests
import json
import os


class GrofersDataScraper:
    folder_name = "grofers"
    access_rights = 0o755

    PRODUCTS_FILE_HEADER = "ITEM NAME,RATING,UNIT,MRP,ACTUAL PRICE,OFFER,SBC OFFER\n"
    PRODUCTS_META_FILE_HEADER = "CATEGORY ID,CATEGORY PATH,EXPECTED DATA COUNT,ACTUAL DATA COUNT\n"

    req_url = "https://grofers.com/v4/search/merchants/26015/products/"

    def __init__(self, categoryDict):
        self.categoryDict = categoryDict
        self.path = os.getcwd() + "/" + self.folder_name
        self.file_name = self.path + "/" + self.folder_name + ".csv"
        self.meta_file_name = self.path + "/" + self.folder_name + "_meta.csv"

        self.createFiles(self.file_name, self.PRODUCTS_FILE_HEADER)
        self.createFiles(self.meta_file_name, self.PRODUCTS_META_FILE_HEADER)

    def createFiles(self, fileName, fileHeader):
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path, self.access_rights)
            except OSError:
                print("Creation of the directory %s failed" % self.path)
            else:
                print("Successfully created the directory %s" % self.path)

        file = open(fileName, "w+", encoding="utf8")
        file.write(fileHeader)
        file.close()

    def scrape(self):
        for category_id, category_path in self.categoryDict.items():
            print(f"GET :: Grofers for category ID : {category_id}")

            initialData = self.getData(category_id, '10')
            initialResultCount = initialData["meta"]["result_count"]

            print(f"OK :: Total products count : {initialResultCount} ")

            data = self.getData(category_id, initialResultCount)
            products = data["result"]["products"]

            # This can be a good assertion condition
            # To check if entire data set is retrieved :
            # initialResultCount === len(products)

            meta_data = category_id + "," + category_path + "," + str(initialResultCount) + "," + str(len(products)) + "\n"

            file = open(self.meta_file_name, "a", encoding="utf8")
            file.write(meta_data)
            file.close()

            self.writeDataToFile(products)

    def getData(self, categoryID, nextVal):
        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'app_client': 'consumer_web'
        }

        params = (
            ('l0_cat', categoryID),
            ('start', '0'),
            ('next', nextVal),
        )

        response = requests.get(self.req_url, headers=headers, params=params)

        file = open(self.path + "/" + categoryID+".json", "w+", encoding="utf8")
        file.write(response.text)
        file.close()

        return json.loads(
            response.text)  # json.loads - takes a JSON string and convert it back to a dictionary structure

    def writeDataToFile(self, prods):
        prodsCount = len(prods)
        for i in range(prodsCount):
            variant_info_data = prods[i]["variant_info"]
            for j in range(len(variant_info_data)):
                vid = variant_info_data[j]
                ITEM_NAME = vid["line_1"]
                RATING = vid["rating"]
                UNIT = vid["unit"]
                MRP = vid["mrp"]
                PRICE = vid["price"]
                OFFER = vid["offer"]
                SBC_OFFER = vid["sbc_offer"]
                final_data = str(ITEM_NAME) + "," + str(RATING) + "," + str(UNIT) + "," + str(MRP) + "," + str(
                    PRICE) + "," + str(OFFER) + "," + str(SBC_OFFER) + "\n"

                file = open(self.file_name, "a", encoding="utf8")
                file.write(final_data)
                file.close()
