from PIL import Image
import os


class FormParser(object):
    def __init__(self, path):
        self.path = path

    def get_name(self, filename):
        os.mkdir(self.path + filename[:-4])
        img = Image.open(self.path + filename, 'r')
        img.crop((98, 221, 1566, 304)).save(self.path + filename[:-4] + '\\' + 'lastname' + filename)
        img.crop((114, 465, 1551, 540)).save(self.path + filename[:-4] + '\\' + 'firstname' + filename)
        return self.path + filename[:-4] + '\\'

    def cut_chars(self):
        files = os.listdir(self.path)
        files = list(filter(lambda x: '.jpg' in x, files))
        new_folders = []
        for file in files:
            os.mkdir(self.path + file[:-4])
            new_folders.append(self.path + file[:-4] + '\\')
            img = Image.open(self.path + file, 'r')
            width, height = img.size
            one_width = round(width / 20)
            counter = 0
            for i in range(0, width - one_width, one_width):
                img.crop((i, 0, i + one_width, height)).save(self.path + file[:-4] + '\\' + file[:-4] + str(counter) + '.jpg')
                counter += 1
        return new_folders

    def cut_borders(self):
        files = os.listdir(self.path)
        files = list(filter(lambda x: '.jpg' in x, files))
        for file in files:
            img = Image.open(self.path + file, 'r')
            width, height = img.size
            img.crop((7, 7, width - 7, height - 7)).save(self.path + file)


path = 'C:\\Users\\User\\Desktop\\Thesis\\forms\\'

