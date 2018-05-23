from PIL import Image
import os


def rename_all(old_path, new_path, type):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    for char in alphabet:
        print(char + " перемещается..")
        files = os.listdir(old_path + char)
        files = list(filter(lambda x: type in x, files))
        i = 1
        for file in files:
           old_file = os.path.join(old_path + char, file)
           new_file = os.path.join(new_path, char + str(i) + type)
           os.rename(old_file, new_file)
           i += 1


def rotate_images(path, left, right, step, type):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    for char in alphabet:
        files = os.listdir(path + char)
        files = list(filter(lambda x: type in x, files))
        counter = 0
        print(char + " поворачивается..")
        for file in files:
            img = Image.open(path + char + "\\" + file)
            counter += 1
            for i in range(left, right, step):
                if i != 0:
                    new_img = Image.new("RGB", img.size, (255, 255, 255))
                    img = img.convert("RGBA").rotate(i)
                    new_img.paste(img, img)
                    if type == '.png':
                        new_img.save(path + char + "\\" + str(counter) + '_' + str(i) + type, "PNG")
                    elif type == '.jpg':
                        new_img.save(path + char + "\\" + str(counter) + '_' + str(i) + type, "JPEG")


def separate_prop(train_prop, test_prop, val_prop, path):
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    files = os.listdir(path)
    os.mkdir(path + 'train', mode=0o777)
    os.mkdir(path + 'test', mode=0o777)
    os.mkdir(path + 'val', mode=0o777)
    for char in alphabet:
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