from utils.file_io import createFiles, writeLineData, getBBPath, getBBCategoryDataFileName
from utils.http_req_res import getData

class BigBasketDataScraper:
    data_folder_name = "big-basket"
    categories_file_name = "big-basket-categories"

    PRODUCTS_FILE_HEADER = "ITEM NAME,BRAND,UNIT,MRP,ACTUAL PRICE,DISCOUNT,CATEGORY_ID\n"

    DATA_FIRST_PAGE_URL = "https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug="
    DATA_URL = "https://www.bigbasket.com/product/get-products/?slug="

    def __init__(self, category_id, category_slug, category_name):
        self.category_id = category_id
        self.category_name = category_name.replace(",",";")
        self.category_slug = category_slug

        createFiles(getBBPath(), getBBCategoryDataFileName(self.category_slug), self.PRODUCTS_FILE_HEADER)

    def scrape(self):
        print(f"Scraping data for category {self.category_slug} with ID {self.category_id}")
        self.scrapeFirstPage()
        self.scrapeOtherPages()

    def scrapeFirstPage(self):
        print("*" * 10)
        print(f"Fetching data for category {self.category_slug}, page 1")

        data = getData(self.DATA_FIRST_PAGE_URL + self.category_slug)

        product_info = data["tab_info"][0]["product_info"]

        self.total_pages = product_info["tot_pages"]
        total_products = product_info["p_count"]

        print(f"Total Pages : {self.total_pages}")
        print(f"Total Products : {total_products}")

        products = product_info["products"]

        print(f"Products count in this req {len(products)}")

        for j in range(len(products)):
            prod = products[j]
            self.writeProductData(prod)

    def scrapeOtherPages(self):
        for page_num in range(2, self.total_pages + 1):
            print("*" * 10)
            print(f"Fetching data for category {self.category_slug}, page {page_num}")

            data = getData(
                f"{self.DATA_URL}{self.category_slug}&page={page_num}&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc")
            products = data["tab_info"]["product_map"]["all"]["prods"]

            for j in range(len(products)):
                prod = products[j]
                self.writeProductData(prod)

    def writeProductData(self, prod):
        ITEM_NAME = prod['p_desc']
        ITEM_BRAND = prod['p_brand']
        ITEM_QTY = prod['w']
        ITEM_MRP = prod['mrp']
        ITEM_SP = prod['sp']
        ITEM_DISCOUNT = prod['dis_val']

        ITEM_NAME = ITEM_NAME.replace(","," /")

        final_data = str(ITEM_NAME) + "," + str(ITEM_BRAND) + "," + str(ITEM_QTY) + "," + str(
            ITEM_MRP) + "," + str(ITEM_SP) + "," + str(ITEM_DISCOUNT) + "," + str(self.category_id) + "\n"
        writeLineData(getBBCategoryDataFileName(self.category_slug), final_data)

