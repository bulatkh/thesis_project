# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 18:25:19 2018

@author: bulbu_000
"""
import os
######
# Делим изображение на тренировочные, тестировочные и валидационные. Параметры - пропорции и путь к папке, где они лежат.
######

def separate_prop(train_prop, test_prop, val_prop, path):
    ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    files = os.listdir(path)
    os.mkdir(path + 'train', mode=0o777)
    os.mkdir(path + 'test', mode=0o777)
    os.mkdir(path + 'val', mode=0o777)
    for char in ALPHABET:
        files_ch = list(filter(lambda x: char in x, files))
        #print(files_ch)
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