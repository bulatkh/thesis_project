from preprocess import convert_image, rename, rotate_images, separate


initial_path = 'C:\\Users\\User\\Desktop\\Thesis\\Cyrillic\\Cyrillic\\'
data_path = 'C:\\Users\\User\\Desktop\\Thesis\\data\\'
size = 56, 56



print("Предобработка изображений..")
print("Поворот:")
rotate_images.rotate_images(initial_path, -24, 24, 2)
print("Переименование и перемещение..")
rename.rename_all(initial_path, data_path)
print("Конвертация изображений..")
convert_image.rgb2binar(data_path)
convert_image.resize(data_path, size)
print("Разделение на тренировочные, тестовые и валидационные..")
separate.separate_prop(0.8, 0.1, 0.1, data_path)
