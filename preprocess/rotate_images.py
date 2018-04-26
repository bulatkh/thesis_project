from PIL import Image
import os


def rotate_images(path, left, right, step):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    for char in alphabet:
        files = os.listdir(path + char)
        files = list(filter(lambda x: ".png" in x, files))
        counter = 0
        print(char + " поворачивается..")
        for file in files:
            img = Image.open(path + char + "\\" + file)
            counter += 1
            for i in range(left, right, step):
                if i != 0:
                    new_img = img.rotate(i)
                    new_img.save(path + char + "\\" + str(counter) + str(i) + ".png", "PNG")