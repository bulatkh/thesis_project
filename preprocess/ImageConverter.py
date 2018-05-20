from PIL import Image
import os


class ImageConverter(object):

    def __init__(self, path, type):
        self.path = path
        self.type = type
        self.files = list(filter(lambda x: type in x, os.listdir(path)))

    def rgb2binar(self):
        length = len(self.files)
        counter = 0
        for file in self.files:
            counter += 1
            if counter % 1000 == 0:
                print("Binarization progress: " + str(counter / length * 100) + " %")
            img = Image.open(self.path + file, 'r')
            if img.mode == 'RGBA':
                bg = Image.new("RGB", (278, 278), (255, 255, 255))
                bg.paste(img, (0, 0), mask=img)
                gray = bg.convert('L')
            else:
                gray = img.convert('L')
            binary = gray.point(lambda x: 0 if x < 128 else 255, "1")
            binary.save(self.path + file)

    def make_square(self, min_size=56, fill_color=(255, 255, 255)):
        for file in self.files:
            image = Image.open(self.path + file, 'r')
            x, y = image.size
            size = max(min_size, x, y)
            new_image = Image.new('RGB', (size, size), fill_color)
            new_image.paste(image, (round((size - x) / 2), round((size - y) / 2)))
            new_image.save(self.path + file)


    def resize(self, size):
        length = len(self.files)
        counter = 0
        for file in self.files:
            counter += 1
            if counter % 1000 == 0:
                print("Resizing progress: " + str(counter / length * 100) + " %")
            img = Image.open(self.path + file, 'r')
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(self.path + file)
