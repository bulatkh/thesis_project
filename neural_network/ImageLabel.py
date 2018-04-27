import os
import numpy as np
from scipy import misc
from random import randint


class ImageLabel(object):

    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'

    def __init__(self, path):
        self.path = path

    @staticmethod
    def label_img(alphabet, path):
        i = 0
        char_numbers = {}
        for char in alphabet:
            char_numbers.update({char: i})
            i += 1
        list_label = []
        files = os.listdir(path)
        files = list(filter(lambda x: '.png' in x, files))
        for file in files:
            list_label.append(char_numbers.get(file[0]))
        return list_label

    @staticmethod
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

    @staticmethod
    def fisher_yates_shuffle(files, labels):
        for i in range(len(files) - 1, 0, -1):
            j = randint(0, i)
            ImageLabel.swap(files, i, j)
            ImageLabel.swap(labels, i, j)

    @staticmethod
    def swap(array, i, j):
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp

    def read_images_with_labels(self):
        files = list(filter(lambda x: '.png' in x, os.listdir(self.path)))
        length = len(files)
        labels = ImageLabel.label_img(self.alphabet, self.path)
        ImageLabel.fisher_yates_shuffle(files, labels)
        labels = ImageLabel.make_vector_labels(labels)
        images = []
        counter = 0
        for file in files:
            counter += 1
            if counter % 1000 == 0:
                print("Final preparation progress: " + str(counter / length * 100) + " %")
            img = misc.imread(self.path + file)
            img = 1. - img.astype(np.float32) / 255.
            images.append(img)
        return images, labels
