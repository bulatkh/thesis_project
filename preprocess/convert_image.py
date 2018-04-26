from PIL import Image
import os


class ImageConverter(object):

    def __init__(self, path):
        self.path = path
        self.files = list(filter(lambda x: ".png" in x, os.listdir(path)))

    def rgb2binar_alpha_png(self):
        length = len(self.files)
        counter = 0
        for file in self.files:
            counter += 1
            if counter % 1000 == 0:
                print("Binarization progress: " + str(counter / length * 100) + " %")
            img = Image.open(self.path + file, 'r')
            bg = Image.new("RGB", (278, 278), (255, 255, 255))
            bg.paste(img, (0, 0), mask=img)
            gray = bg.convert('L')
            binary = gray.point(lambda x: 0 if x < 128 else 255, "1")
            binary.save(self.path + file)

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
