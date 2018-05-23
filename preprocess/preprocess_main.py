from preprocess import os_manipulation, ImageConverter
import time

initial_path = 'C:\\Users\\User\\Desktop\\Thesis\\own_data\\own_data\\'
data_path = 'C:\\Users\\User\\Desktop\\Thesis\\datasets\\own_data_3\\'
size = 56, 56

start_time = time.time()
print("Предобработка изображений..")
print("Поворот:")
os_manipulation.rotate_images(initial_path, -10, 11, 2, '.jpg')
print("Переименование и перемещение..")
os_manipulation.rename_all(initial_path, data_path, '.jpg')
print("Конвертация изображений..")

image_converter = ImageConverter.ImageConverter(data_path, '.jpg')
image_converter.make_square()
image_converter.rgb2binar()
image_converter.resize(size)
print("Разделение на тренировочные, тестовые и валидационные..")
os_manipulation.separate_prop(0.8, 0.1, 0.1, data_path)
finish_time = time.time()
print('Время первичной предобработки: ' + str(finish_time - start_time) + ' секунд.')
