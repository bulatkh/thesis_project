from PIL import Image
import os


class TableParser(object):
    def __init__(self, path):
        self.path = path
        self.files = list(filter(lambda x: ".jpg" in x, os.listdir(self.path)))

    def cut_table(self):
        for file in self.files:
            img = Image.open(self.path + file, 'r')
            width, height = img.size
            img.crop((40, 80, width - 146, height - 170)).save(self.path + file)

    def cut_chars(self):
        counter = 0
        os.mkdir(self.path + 'data', mode=0o777)
        data_path = ''
        for file in self.files:
            img = Image.open(self.path + file, 'r')
            width, height = img.size

            data_path = self.path + 'data' + '\\'
            for i in range(0, width - 146, 146):
                for j in range(0, height - 149, 149):
                    counter += 1
                    img.crop((i, j, i + 146, j + 149)).save(data_path + str(counter) + '.jpg')
        return data_path

    @staticmethod
    def center_chars(data_path):
        files = os.listdir(data_path)
        files = list(filter(lambda x: ".jpg" in x, files))
        for file in files:
            img = Image.open(data_path + file, 'r')
            width, height = img.size
            img.crop((10, 10, width - 10, height - 10)).save(data_path + file)
