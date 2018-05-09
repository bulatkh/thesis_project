from PIL import Image
from text_recognition import Predictor
import os


class FormParser(object):
    def __init__(self, filename):
        self._filename = filename
        self._second_name_path = ''
        self._name_path = ''

    @property
    def filename(self):
        return self._filename

    @property
    def second_name_path(self):
        return self._second_name_path

    @second_name_path.setter
    def second_name_path(self, path):
        self._second_name_path = path

    @property
    def name_path(self):
        return self._name_path

    @name_path.setter
    def name_path(self, path):
        self._name_path = path

    def get_chars(self):
        img = Image.open(self.filename, 'r')
        os.mkdir(self.filename[:-4])
        images = []
        images.append(img.crop((147, 224, 1610, 300)))
        images.append(img.crop((162, 465, 1590, 545)))
        counter = 0
        self.second_name_path = self.filename[:-4] + '\\second_name\\'
        self.name_path = self.filename[:-4] + '\\name\\'
        os.mkdir(self.second_name_path)
        os.mkdir(self.name_path)
        for img in images:
            img.show()
            width, height = img.size
            one_width = round(width / 20)
            for i in range(0, width - one_width, one_width):
                    if counter < 20:
                        img.crop((i, 0, i + one_width, height)).save(
                            self.second_name_path + str(counter) + '.jpg')
                    else:
                        img.crop((i, 0, i + one_width, height)).save(
                            self.name_path + str(counter) + '.jpg')
                    counter += 1

    @staticmethod
    def cut_borders(path):
        files = os.listdir(path)
        files = list(filter(lambda x: '.jpg' in x, files))
        for file in files:
            img = Image.open(path + file, 'r')
            width, height = img.size
            img.crop((7, 7, width - 7, height - 7)).save(path + '\\' + file)

    @staticmethod
    def delete_empty(path):
        files = os.listdir(path)
        files = list(filter(lambda x: '.jpg' in x, files))
        for file in files:
            tmp_img = Image.open(path + '\\' + file, 'r')
            tmp_img = tmp_img.convert('L')
            binary = tmp_img.point(lambda pix: 0 if pix < 128 else 255, "1")
            pixels = list(binary.getdata())
            sum = 0
            for pixel in pixels:
                if pixel == 0:
                    sum += 1
            if sum / len(pixels) < 0.05:
                os.remove(path + '\\' + file)

    @staticmethod
    def recognize_chars(path, nn_path):
        files = os.listdir(path)
        files = list(filter(lambda x: '.jpg' in x, files))
        files = [int(file[:-4]) for file in files]
        files.sort()
        predictor = Predictor.Predictor(path, nn_path)
        final_answer = []
        for file in files:
            file = str(file) + '.jpg'
            _, prediction = predictor.make_prediction(path + '\\' + file, nn_path)
            recognized_char, _ = predictor.analyze_prediction(prediction)
            final_answer.append(recognized_char)
        return ''.join(final_answer)

    def get_full_name(self, nn_path):
        second_name = FormParser.recognize_chars(self._second_name_path, nn_path)
        first_name = FormParser.recognize_chars(self._name_path, nn_path)
        return first_name, second_name


if __name__ == '__main__':
    form_path = 'C:\\Users\\User\\Desktop\\Thesis\\forms\\1.jpg'
    nn_path = 'C:\\Users\\User\\Desktop\\Thesis\\trained_nn\\kaggle\\bigbatch.ckpt-4126'
    parser = FormParser(form_path)
    parser.get_chars()
    parser.cut_borders(parser.name_path)
    parser.cut_borders(parser.second_name_path)
    parser.delete_empty(parser.name_path)
    parser.delete_empty(parser.second_name_path)
    first, second = parser.get_full_name(nn_path)
    print(first + ' ' + second)
