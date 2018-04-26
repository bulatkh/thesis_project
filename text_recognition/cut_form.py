from PIL import Image
import os


def get_name(path, filename):
    os.mkdir(path + filename[:-4])
    img = Image.open(path + filename, 'r')
    img.crop((98, 221, 1566, 304)).save(path + filename[:-4] + '\\' + 'lastname' + filename)
    img.crop((114, 465, 1551, 540)).save(path + filename[:-4] + '\\' + 'firstname' + filename)
    return path + filename[:-4] + '\\'


def cut_chars(path):
    files = os.listdir(path)
    files = list(filter(lambda x: '.jpg' in x, files))
    new_folders = []
    for file in files:
        os.mkdir(path + file[:-4])
        new_folders.append(path + file[:-4] + '\\')
        img = Image.open(path + file, 'r')
        width, height = img.size
        one_width = round(width / 20)
        counter = 0
        for i in range(0, width - one_width, one_width):
            img.crop((i, 0, i + one_width, height)).save(path + file[:-4] + '\\' + file[:-4] + str(counter) + '.jpg')
            counter += 1
    return new_folders


def cut_borders(path):
    files = os.listdir(path)
    files = list(filter(lambda x: '.jpg' in x, files))
    for file in files:
        img = Image.open(path + file, 'r')
        width, height = img.size
        img.crop((7, 7, width - 7, height - 7)).save(path + file)


path = 'C:\\Users\\User\\Desktop\\Thesis\\forms\\'
filename = '1.jpg'
form_path = get_name(path, filename)
new_paths = cut_chars(form_path)
for path in new_paths:
    cut_borders(path)
