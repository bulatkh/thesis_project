from PIL import Image
import os

dir_path = 'C:\\Users\\User\\Desktop\\Thesis\\tables\\'


def cut_table(dir_path):
    files = os.listdir(dir_path)
    files = list(filter(lambda x: ".jpg" in x, files))
    for file in files:
        img = Image.open(dir_path + file, 'r')
        width, height = img.size
        img.crop((40, 80, width - 146, height - 170)).save(dir_path + file)


def cut_chars(dir_path):
    files = os.listdir(dir_path)
    files = list(filter(lambda x: ".jpg" in x, files))
    counter = 0
    os.mkdir(dir_path + 'data', mode=0o777)
    data_path = ''
    for file in files:
        img = Image.open(dir_path + file, 'r')
        width, height = img.size

        data_path = dir_path + 'data' + '\\'
        for i in range(0, width - 146, 146):
            for j in range(0, height - 149, 149):
                counter += 1
                img.crop((i, j, i + 146, j + 149)).save(data_path + str(counter) + '.jpg')
    return data_path


def center_chars(data_path):
    files = os.listdir(data_path)
    files = list(filter(lambda x: ".jpg" in x, files))
    for file in files:
        img = Image.open(data_path + file, 'r')
        width, height = img.size
        img.crop((10, 10, width - 10, height - 10)).save(data_path + file)


#cut_table(dir_path)
data_path = cut_chars(dir_path)
center_chars(data_path)
