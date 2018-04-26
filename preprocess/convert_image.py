from PIL import Image
import os

size = 56, 56


def rgb2binar(path):
    files = os.listdir(path)
    files = list(filter(lambda x: ".png" in x, files))
    length = len(files)
    counter = 0
    for file in files:
        counter += 1
        if counter % 1000 == 0:
            print("Binarization progress: " + str(counter / length * 100) + " %")
        img = Image.open(path + file, 'r')
        bg = Image.new("RGB", (278, 278), (255, 255, 255))
        bg.paste(img, (0, 0), mask=img)
        gray = bg.convert('L')
        binary = gray.point(lambda x: 0 if x < 128 else 255, "1")
        binary.save(path + file)


def resize(path, size):
    files = os.listdir(path)
    files = list(filter(lambda x: ".png" in x, files))
    length = len(files)
    counter = 0
    for file in files:
        counter += 1
        if counter % 1000 == 0:
            print("Resizing progress: " + str(counter / length * 100) + " %")
        img = Image.open(path + file, 'r')
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(path + file)
