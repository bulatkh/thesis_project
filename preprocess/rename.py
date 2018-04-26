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