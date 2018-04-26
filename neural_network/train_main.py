from numpy import array
from neural_network import model
from neural_network import label_images as li

train_path = 'C:\\Users\\User\\Desktop\\\\Thesis\\data\\train\\'
test_path = 'C:\\Users\\User\\Desktop\\\\Thesis\\data\\test\\'
val_path = 'C:\\Users\\User\\Desktop\\\\Thesis\\data\\val\\'
print("-")
train_images_label = li.ImageLabel(train_path)
train_images, train_labels = train_images_label.read_images_with_labels()
print("-")
test_images_label = li.ImageLabel(test_path)
test_images, test_labels = test_images_label.read_images_with_labels()
print("-")
val_images_label = li.ImageLabel(val_path)
val_images, val_labels = val_images_label.read_images_with_labels()
print("--")

test_labels = array(test_labels)
train_labels = array(train_labels)
test_images = array(test_images)
train_images = array(train_images)
val_images = array(val_images)
val_labels = array(val_labels)

print("Training started!")
model.create_nn_and_train(56, 32, 5, 2, 0.001, train_images, train_labels, test_images, test_labels, val_images,
                          val_labels)



