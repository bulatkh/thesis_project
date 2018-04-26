# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 18:26:07 2018

@author: bulbu_000
"""

import os
import numpy as np
from scipy import misc
from neural_network import fisher_yates

ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'


def label_img(path):
    i = 0
    char_numbers = {}
    for char in ALPHABET:
        char_numbers.update({char: i})
        i += 1
    list_label = []
    files = os.listdir(path)
    files = list(filter(lambda x: '.png' in x, files))
    for file in files:
        list_label.append(char_numbers.get(file[0]))
    return list_label


def make_vector_labels(list_label):
    vector_labels = []
    number_of_labels = max(list_label) + 1
    zeros = []
    for i in range(number_of_labels):
        zeros.append(0) 
    for label in list_label:
        vector_tmp = zeros.copy()
        vector_tmp[label] = 1
        vector_labels.append(vector_tmp)
    return vector_labels


def read_images_with_labels(path):
    files = list(filter(lambda x: ".png" in x, os.listdir(path)))
    length = len(files)
    labels = label_img(path)
    fisher_yates.fisher_yates_shuffle(files, labels)
    labels = make_vector_labels(labels)
    images = []
    counter = 0
    for file in files:
        counter += 1
        if counter % 1000 == 0:
            print("Final preparation progress: " + str(counter / length * 100) + " %")
        img = misc.imread(path + file)
        img = 1. - img.astype(np.float32) / 255.
        images.append(img)
    return images, labels
