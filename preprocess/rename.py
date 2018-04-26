# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 18:21:48 2018

@author: bulbu_000
"""

import os

######
# Переименовываем файлы и складываем в одну папку
######


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


# old_path = 'C:\\Users\\User\\Desktop\\Thesis\\Cyrillic\\Cyrillic\\'
# new_path = 'C:\\Users\\User\\Desktop\\Thesis\\data\\'
# rename_all(old_path, new_path)
