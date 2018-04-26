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