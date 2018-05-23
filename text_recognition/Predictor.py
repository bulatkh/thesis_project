import tensorflow as tf
import numpy as np
from scipy import misc
from matplotlib import pyplot as plt
from PIL import Image
import os
import random


class Predictor(object):
    def __init__(self, nn_path, data_path):
        self.nn_path = nn_path
        self.data_path = data_path

    @staticmethod
    def make_square(image, min_size=56, fill_color=(255, 255, 255)):
        x, y = image.size
        size = max(min_size, x, y)
        new_image = Image.new('RGB', (size, size), fill_color)
        new_image.paste(image, (round((size - x) / 2), round((size - y) / 2)))
        return new_image

    @staticmethod
    def make_prediction(image_path, nn_path):
        sample = Image.open(image_path)
        sample = Predictor.make_square(sample)
        sample = sample.convert('L')
        size = 56, 56
        sample.thumbnail(size, Image.ANTIALIAS)
        binary = sample.point(lambda pix: 0 if pix < 128 else 255, "1")
        binary.save(image_path)

        image = misc.imread(image_path)
        sample = 1. - image.astype(np.float32) / 255.
        sample = np.array(sample)

        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(nn_path + '.meta')
            saver.restore(sess, nn_path)
            x = tf.placeholder(tf.float32, [56, 56], name='x')
            x_image = tf.reshape(x, [-1, 56, 56, 1], name='image')
            W = tf.get_collection('weights')
            b = tf.get_collection('biases')

            conv_0_logit = tf.add(tf.nn.conv2d(x_image, W[0], strides=[1, 1, 1, 1], padding='SAME'), b[0], name='logit')
            h_conv_0 = tf.nn.relu(conv_0_logit, name='relu')

            h_pool_0 = tf.nn.max_pool(h_conv_0, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                                      padding='SAME')

            conv_1_logit = tf.add(tf.nn.conv2d(h_pool_0, W[1], strides=[1, 1, 1, 1], padding='SAME'), b[1],
                                  name='logit')
            h_conv_1 = tf.nn.relu(conv_1_logit, name='relu')

            h_pool_1 = tf.nn.max_pool(h_conv_1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                                      padding='SAME')

            conv_2_logit = tf.add(tf.nn.conv2d(h_pool_1, W[2], strides=[1, 1, 1, 1], padding='SAME'), b[2],
                                  name='logit')
            h_conv_2 = tf.nn.relu(conv_2_logit, name='relu')

            h_pool_2 = tf.nn.max_pool(h_conv_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                                      padding='SAME')

            h_pool_2_flat = tf.reshape(h_pool_2, [-1, 7 * 7 * 128], name='flatten')

            fc_0_logit = tf.add(tf.matmul(h_pool_2_flat, W[3]), b[3], name='logit')
            h_fc_0 = tf.nn.relu(fc_0_logit, name='relu')

            logit_out = tf.add(tf.matmul(h_fc_0, W[4]), b[4], name='logit')

            prediction = sess.run(tf.nn.softmax(logit_out), feed_dict={x: sample})
        return image, prediction

    @staticmethod
    def plot_prediction(image, prediction):
        ans = np.argmax(prediction)
        fig = plt.figure(figsize=(10, 4))

        ax = fig.add_subplot(2, 1, 1)
        ax.imshow(image, cmap='gray')
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))

        ax = fig.add_subplot(2, 1, 2)
        bar_list = ax.bar(np.arange(32), prediction[0], align='center')
        bar_list[ans].set_color('g')
        ax.set_xlim([-1, 32])
        ax.grid('on')
        alphabet_list = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
         'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        plt.xticks(np.arange(32), alphabet_list)
        plt.show()

    @staticmethod
    def analyze_prediction(prediction, mode='print'):
        alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        ans = np.argmax(prediction)
        char_counter = 0
        char_dict = {}
        for char in alphabet:
            char_dict.update({char_counter: char})
            char_counter += 1

        ans_char = char_dict.get(ans)
        res_list = []
        if mode == 'print':
            print('----------------------------------')
            print("Ответ нейронной сети: " + char_dict.get(ans))
        prediction_counter = 0
        for res in prediction[0]:
            if round(res, 2) > 0.1:
                if mode == 'print':
                    print('Вероятность буквы ' + str(char_dict.get(prediction_counter)) + ': ' + str(round(res * 100, 2)) + '%')
                res_list.append(char_dict.get(prediction_counter))
            prediction_counter += 1
        return ans_char, res_list

    def count_accuracy(self, number, type, char='0'):
        files = os.listdir(self.data_path)
        files = list(filter(lambda x: type in x, files))
        if char != '0':
            files = list(filter(lambda x: char in x, files))
        random.shuffle(files)
        files = files[:number]
        number_of_images = len(files)
        counter_accuracy = 0
        counter_in_results = 0
        for file in files:
            image, prediction = Predictor.make_prediction(data_path + file, self.nn_path)
            ans, res_list = Predictor.analyze_prediction(prediction)
            # Predictor.plot_prediction(image, prediction)
            print('Правильный ответ: ' + file[:1])
            if str(ans) in file:
                counter_accuracy += 1
            for res in res_list:
                if res in file:
                    counter_in_results += 1
        accuracy = counter_accuracy / number_of_images
        accuracy_in_results = counter_in_results / number_of_images
        print('----------------------------------')
        print("Точность распознавания: " + str(accuracy * 100) + "%")
        print('----------------------------------')
        print("Правильный ответ есть в отклике цепи в: " + str(accuracy_in_results * 100) + "%")


if __name__ == '__main__':
    saved_nn = 'C:\\Users\\User\\Desktop\\Thesis\\trained_nn\\own_data\\own_data.ckpt-4404'
    data_path = 'C:\\Users\\User\\Desktop\\Thesis\\datasets\\own_data\\val\\'
    # files = list(filter(lambda x: '.jpg' in x, os.listdir(data_path)))
    # random.shuffle(files)
    # short_list = files[:100]
    # for file in short_list:
    #     image, prediction = Predictor.make_prediction(data_path + file, saved_nn)
    #     # Predictor.plot_prediction(image, prediction)
    #     Predictor.analyze_prediction(prediction)
    # # predictor_kaggle = Predictor(saved_nn, data_path)
    # # predictor_kaggle.count_accuracy()
    predictor_own_data = Predictor(saved_nn, data_path)
    predictor_own_data.count_accuracy(100, '.jpg', 'А')
