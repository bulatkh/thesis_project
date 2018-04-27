from PIL import Image
import os


def rename_all(old_path, new_path):
    ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    for char in ALPHABET:
        print(char + " перемещается..")
        files = os.listdir(old_path + char)
        files = list(filter(lambda x: ".png" in x, files))
        i = 1
        for file in files:
           old_file = os.path.join(old_path + char, file)
           new_file = os.path.join(new_path, char + '%s.png' % i)
           os.rename(old_file, new_file)
           i += 1


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


def separate_prop(train_prop, test_prop, val_prop, path):
    ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    files = os.listdir(path)
    os.mkdir(path + 'train', mode=0o777)
    os.mkdir(path + 'test', mode=0o777)
    os.mkdir(path + 'val', mode=0o777)
    for char in ALPHABET:
        files_ch = list(filter(lambda x: char in x, files))
        l = len(files_ch)
        i = 0
        for file in files_ch:
            if i < l * train_prop:
                old_file = os.path.join(path, file)
                new_file = os.path.join(path + 'train', file)
                os.rename(old_file, new_file)
                i += 1
            elif i < l * train_prop + l * test_prop:
                old_file = os.path.join(path, file)
                new_file = os.path.join(path + 'test', file)
                os.rename(old_file, new_file)
                i += 1
            else:
                old_file = os.path.join(path, file)
                new_file = os.path.join(path + 'val', file)
                os.rename(old_file, new_file)