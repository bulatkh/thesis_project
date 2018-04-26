# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 20:40:45 2018

@author: bulbu_000
"""

from random import randint

def fisher_yates_shuffle(filenames, labels):
    for i in range(len(filenames) - 1, 0, -1):
        j = randint(0, i)
        swap(filenames, i, j)
        swap(labels, i, j)
        
def swap(array, i , j):
    tmp = array[i]
    array[i] = array[j]
    array[j] = tmp        
        
#array = [0, 1, 2, 3, 4, 5, 6, 7]
#arrayy = [0, 1, 2, 3, 4, 5, 6, 7]

#fisher_yates_shuffle(array, arrayy)
#print(array)
#print(arrayy)