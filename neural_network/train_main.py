from numpy import array
from neural_network import model, label_images

train_path = 'C:\\Users\\User\\Desktop\\\\Thesis\\data\\train\\'
test_path = 'C:\\Users\\User\\Desktop\\\\Thesis\\data\\test\\'
val_path = 'C:\\Users\\User\\Desktop\\\\Thesis\\data\\val\\'
print("-")
train_images, train_labels = label_images.read_images_with_labels(train_path)
print("-")
test_images, test_labels = label_images.read_images_with_labels(test_path)
print("-")
val_images, val_labels = label_images.read_images_with_labels(val_path)
print("--")


test_labels = array(test_labels)
train_labels = array(train_labels)
test_images = array(test_images)
train_images = array(train_images)
val_images = array(val_images)
val_labels = array(val_labels)

# 1. Зашумить изображения - расширить датасет
# 2. Шаг обучения - придумать, как должен меняться
# 3. Найти наилучшую архитектуру сети (количество слоев, размеры сверточных окон, размеры изоб.)
# 4. Допилить во входные параметры алгоритм оптимизации, размер батча, размер полносвязного слоя)

# first_batch_lab = test_labels[:32]
# first_batch_img = test_images[:32]
# batched_train_img, batched_train_lab = prepare.batch_dataset(train_images, train_labels)
# batched_test_img, batched_test_lab = prepare.batch_dataset(test_images, test_labels)
# print(train_labels)
# batched_train_img = array(batched_train_img).reshape(32, 28, 28, 1)
# batched_test_img = array(batched_test_img).reshape(32, 28, 28, 1)
print("Training started!")
model.create_nn_and_train(56, 32, 5, 2, 0.001, train_images, train_labels, test_images, test_labels, val_images, val_labels)



