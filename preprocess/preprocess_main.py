from preprocess import os_manipulation, ImageConverter

initial_path = 'C:\\Users\\User\\Desktop\\Thesis\\Cyrillic\\Cyrillic\\'
data_path = 'C:\\Users\\User\\Desktop\\Thesis\\data\\'
size = 56, 56

print("Предобработка изображений..")
print("Поворот:")
os_manipulation.rotate_images(initial_path, -24, 24, 2)
print("Переименование и перемещение..")
os_manipulation.rename_all(initial_path, data_path)
print("Конвертация изображений..")
image_converter = ImageConverter.ImageConverter(data_path)
image_converter.rgb2binar_alpha_png()
image_converter.resize(size)
print("Разделение на тренировочные, тестовые и валидационные..")
os_manipulation.separate_prop(0.8, 0.1, 0.1, data_path)
