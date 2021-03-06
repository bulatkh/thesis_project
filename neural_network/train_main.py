from numpy import array
from neural_network import model, ImageLabel as li
import time

dataset_path = input()
train_path = dataset_path + 'train\\'
test_path = dataset_path + 'test\\'
val_path = dataset_path + 'val\\'

label_start_time = time.time()
print("-")
train_images_label = li.ImageLabel(train_path, '.png')
train_images, train_labels = train_images_label.read_images_with_labels()
print("-")
test_images_label = li.ImageLabel(test_path, '.png')
test_images, test_labels = test_images_label.read_images_with_labels()
print("-")
val_images_label = li.ImageLabel(val_path, '.png')
val_images, val_labels = val_images_label.read_images_with_labels()
print("--")
label_finish_time = time.time()
print('Время маркировки изображений: ' + str(label_finish_time - label_start_time))


test_labels = array(test_labels)
train_labels = array(train_labels)
test_images = array(test_images)
train_images = array(train_images)
val_images = array(val_images)
val_labels = array(val_labels)


print("Training started!")
model.create_nn_and_train(56, 32, 3, 2, 64, 0.001, train_images, train_labels, test_images, test_labels, val_images,
                          val_labels)


