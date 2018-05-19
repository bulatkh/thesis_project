from PIL import Image
import os


class TableParser(object):
    def __init__(self, path, des_path):
        self.path = path
        self.files = list(filter(lambda x: ".jpg" in x, os.listdir(self.path)))
        self.des_path = des_path

    def cut_table(self):
        for file in self.files:
            img = Image.open(self.path + file, 'r')
            width, height = img.size
            img.crop((40, 80, width - 146, height - 170)).save(self.path + file)

    def cut_chars(self):
        counter = 0
        for file in self.files:
            img = Image.open(self.path + file, 'r')
            width, height = img.size
            one_char_width = round(width / 10)
            one_char_height = round(height / 14)
            for i in range(0, width - one_char_width, one_char_width):
                for j in range(0, height - one_char_height, one_char_height):
                    counter += 1
                    img.crop((i + 1, j + 1, i + one_char_width - 1, j + one_char_height - 1)).save(self.des_path + str(counter) + '.jpg')

    def center_chars(self, border_size):
        files = os.listdir(self.des_path)
        files = list(filter(lambda x: ".jpg" in x, files))
        for file in files:
            img = Image.open(self.des_path + file, 'r')
            width, height = img.size
            img.crop((border_size, border_size, width - border_size, height - border_size)).save(self.des_path + file)

    def cut_upper_part(self, cut_size):
        files = os.listdir(self.des_path)
        files = list(filter(lambda x: ".jpg" in x, files))
        for file in files:
            img = Image.open(self.des_path + file, 'r')
            width, height = img.size
            img.crop((0, cut_size, width, height)).save(self.des_path + file)

    def cut_upper_part(self, cut_size):
        files = os.listdir(self.des_path)
        files = list(filter(lambda x: ".jpg" in x, files))
        for file in files:
            img = Image.open(self.des_path + file, 'r')
            width, height = img.size
            img.crop((0, cut_size, width, height)).save(self.des_path + file)

    def cut_left_part(self, cut_size):
        files = os.listdir(self.des_path)
        files = list(filter(lambda x: ".jpg" in x, files))
        for file in files:
            img = Image.open(self.des_path + file, 'r')
            width, height = img.size
            img.crop((cut_size, 0, width, height)).save(self.des_path + file)



if __name__ == '__main__':
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    tables_path = 'C:\\Users\\User\\Desktop\\Thesis\\tables\\'
    des_path = 'C:\\Users\\User\\Desktop\\Thesis\\own_data\\'
    for char in alphabet:
        parser = TableParser(tables_path + char + '\\', des_path + char + '\\')
        # parser.cut_chars()
        # parser.center_chars(7)
        # parser.cut_upper_part(10)
        parser.cut_left_part(10)
