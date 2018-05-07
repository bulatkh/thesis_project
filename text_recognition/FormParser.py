from PIL import Image
from text_recognition import Predictor
import os


class FormParser(object):
    def __init__(self, filename):
        self.filename = filename

    def get_chars(self):
        img = Image.open(self.filename, 'r')
        os.mkdir(self.filename[:-4])
        images = []
        images.append(img.crop((134, 221, 1596, 300)))
        images.append(img.crop((144, 465, 1581, 540)))
        counter = 0
        for img in images:
            img.show()
            width, height = img.size
            one_width = round(width / 20)
            for i in range(0, width - one_width, one_width):
                    img.crop((i, 0, i + one_width, height)).save(self.filename[:-4] + '\\' + str(counter) + '.jpg')
                    counter += 1

    def cut_borders(self):
        files = os.listdir(self.filename[:-4])
        files = list(filter(lambda x: '.jpg' in x, files))
        for file in files:
            img = Image.open(self.filename[:-4] + '\\' + file, 'r')
            width, height = img.size
            img.crop((7, 7, width - 7, height - 7)).save(self.filename[:-4] + '\\' + file)

    def delete_empty(self):
        files = os.listdir(self.filename[:-4])
        files = list(filter(lambda x: '.jpg' in x, files))
        for file in files:
            tmp_img = Image.open(self.filename[:-4] + '\\' + file, 'r')
            tmp_img.convert('L')
            binary = tmp_img.point(lambda pix: 0 if pix < 128 else 255, "1")
            pixels = list(binary.getdata())
            sum = 0
            for pixel in pixels:
                if pixel == 0:
                    sum += 1
            if sum / len(pixels) < 0.05:
                os.remove(self.filename[:-4] + '\\' + file)

    def recognize_chars(self, nn_path):
        files = os.listdir(self.filename[:-4])
        files = list(filter(lambda x: '.jpg' in x, files))
        files = [int(file[:-4]) for file in files]
        files.sort()
        predictor = Predictor.Predictor(self.filename[:-4], nn_path)
        final_answer = []
        for file in files:
            file = str(file) + '.jpg'
            _, prediction = predictor.make_prediction(self.filename[:-4] + '\\' + file, nn_path)
            recognized_char, _ = predictor.analyze_prediction(prediction)
            final_answer.append(recognized_char)
        return ''.join(final_answer)


if __name__ == '__main__':
    form_path = 'C:\\Users\\User\\Desktop\\Thesis\\forms\\1.jpg'
    nn_path = 'C:\\Users\\User\\Desktop\\Thesis\\trained_nn\\kaggle\\bigbatch.ckpt-4126'
    parser = FormParser(form_path)
    parser.get_chars()
    parser.cut_borders()
    parser.delete_empty()
    answer = parser.recognize_chars(nn_path)
    print(answer)
