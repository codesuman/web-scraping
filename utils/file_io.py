import os

def createFiles(path, fileName, fileHeader):
    access_rights = 0o755

    if not os.path.exists(path):
        try:
            os.mkdir(path, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

    file = open(fileName, "w+", encoding="utf8")
    file.write(fileHeader)
    file.close()

def getBBFolderName():
    return "big-basket"

def getBBPath():
    path = os.getcwd() + "/" + getBBFolderName()
    return path

def getBBCategoriesFileName():
    categories_file_name = "big-basket-categories"

    categories_file_name = getBBPath() + "/" + categories_file_name + ".csv"
    return categories_file_name


def getBBCategoryDataFileName(category_slug):
    data_file_name = getBBPath() + "/" + getBBFolderName() + "_" + category_slug + ".csv"

    return data_file_name

def writeLineData(file_name, data):
    file = open(file_name, "a", encoding="utf8")
    file.write(data)
    file.close()