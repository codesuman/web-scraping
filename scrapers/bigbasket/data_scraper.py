import requests
import json
import os

class BigBasketDataScraper:
    data_folder_name = "big-basket"
    categories_folder_name = "big-basket-categories"
    access_rights = 0o755

    PRODUCTS_FILE_HEADER = "ITEM NAME,BRAND,UNIT,MRP,ACTUAL PRICE,DISCOUNT,CATEGORY,CATEGORY_ID\n"
    CATEGORIES_FILE_HEADER = "CATEGORY ID,CATEGORY SLUG,TOTAL PAGES,TOTAL PRODUCTS\n"

    CATEGORIES_URL = "https://www.bigbasket.com/auth/get_menu/?city_id=1"
    DATA_FIRST_PAGE_URL = "https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug="
    DATA_URL = "https://www.bigbasket.com/product/get-products/?slug="

    def __init__(self):
        self.categories = {}
        self.path = os.getcwd() + "/" + self.data_folder_name
        self.data_file_name = self.path + "/" + self.data_folder_name + ".csv"
        self.categories_file_name = self.path + "/" + self.categories_folder_name + ".csv"

        self.createFiles(self.data_file_name, self.PRODUCTS_FILE_HEADER)
        self.createFiles(self.categories_file_name, self.CATEGORIES_FILE_HEADER)


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
        self.getCategories()

        for category_id, category_slug  in self.categories.items():
            print(f"{category_id} : {category_slug}")
            if category_slug == "foodgrains-oil-masala": # TODO : AFTER TESTING : Remove this if check
                self.scrapeFirstPage(category_slug, category_id)
                # self.scrapeOtherPages(category_slug, category_id) # TODO : AFTER TESTING : Remove this if check

    def getCategories(self):
        print("*" * 10)
        print("Fetching Categories : ")
        print("*" * 10)

        data = self.getData(self.CATEGORIES_URL)
        categories = data["topcats"]

        for cat in categories:
            top_category = cat["top_category"]
            self.categories[top_category["id"]] = top_category["slug"]

    def scrapeFirstPage(self, category_slug, category_id):
        print("*" * 10)
        print(f"Fetching data for category {category_slug}, page 1")

        data = self.getData(self.DATA_FIRST_PAGE_URL + category_slug)

        product_info = data["tab_info"][0]["product_info"]

        self.total_pages = product_info["tot_pages"]
        self.total_products = product_info["p_count"]

        # Writing data to Categories file
        final_data = str(category_id) + "," + category_slug + "," + str(self.total_pages) + "," + str(self.total_products) + "\n"
        self.writeLineData(self.categories_file_name, final_data)

        products = product_info["products"]

        print(f"Total Products in this req {len(products)}")

        for j in range(len(products)):
            prod = products[j]
            self.writeProductData(prod, category_id)

    def scrapeOtherPages(self, category_slug, category_id):
        print(f"Total Pages : {self.total_pages}")
        print(f"Total Products : {self.total_products}")

        for page_num in range(2, self.total_pages + 1):
            print("*" * 10)
            print(f"Fetching data for category {category_slug}, page {page_num}")

            data = self.getData(
                f"{self.DATA_URL}{category_slug}&page={page_num}&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc")
            products = data["tab_info"]["product_map"]["all"]["prods"]

            for j in range(len(products)):
                prod = products[j]
                self.writeProductData(prod, category_id)

    def writeProductData(self, prod, category_id):
        ITEM_NAME = prod['p_desc']
        ITEM_BRAND = prod['p_brand']
        ITEM_QTY = prod['w']
        ITEM_MRP = prod['mrp']
        ITEM_SP = prod['sp']
        ITEM_DISCOUNT = prod['dis_val']
        CATEGORY = prod['tlc_n']

        final_data = str(ITEM_NAME) + "," + str(ITEM_BRAND) + "," + str(ITEM_QTY) + "," + str(
            ITEM_MRP) + "," + str(ITEM_SP) + "," + str(ITEM_DISCOUNT) + str(CATEGORY) + str(category_id) + "\n"
        self.writeLineData(self.data_file_name, final_data)

    def writeLineData(self, file_name, data):
        file = open(file_name, "a", encoding="utf8")
        file.write(data)
        file.close()

    def getData(self, req_url):
        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'app_client': 'consumer_web'
        }

        response = requests.get(req_url, headers=headers)

        return json.loads(
            response.text)  # json.loads - takes a JSON string and convert it back to a dictionary structure

