import os


def createFiles(fileName, fileHeader=None):
    access_rights = 0o755

    path = fileName.rsplit("/", 1)[0]

    if not os.path.exists(path):
        try:
            os.mkdir(path, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

    file = open(fileName, "w+", encoding="utf8")
    if fileHeader is not None:
        file.write(fileHeader)
    file.close()


def getBBFolderName():
    return "big-basket"


def getBBPath():
    path = os.getcwd() + "/" + getBBFolderName()
    return path


def getBBCategoriesFileName(extension="csv"):
    categories_file_name = "big-basket-categories"

    categories_file_name = getBBPath() + "/" + categories_file_name + "." + extension
    return categories_file_name


def getBBCategoryDataFileName(category_slug, extension="csv", pageNum="1"):
    if extension == "csv":
        data_file_name = getBBPath() + "/" + category_slug + "/data." + extension
    else:
        data_file_name = getBBPath() + "/" + category_slug + "/data-" + pageNum + "." + extension
    return data_file_name


def writeLineData(file_name, data):
    file = open(file_name, "a", encoding="utf8")
    file.write(data)
    file.close()
