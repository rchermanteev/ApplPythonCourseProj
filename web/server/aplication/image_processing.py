from preprocessing import preprocessing
from classification.classifier import model, symbol_dict
import numpy as np

digits = [i for i in range(8, 18)]
let = [i for i in range(74, 100)]
minus_equal = [5, 18]


def is_upper_right(img1, img2):
    # ось у вниз!
    # (0,0) верхний левый угол изображения
    # x, y - координаты верхнего левого угла
    if img1[1][0] + img1[1][1]/4 > img2[1][0] + img2[1][1]:
        if img1[0][0] + img2[0][1] < img2[0][0]:
            return True
    return False


def is_inside(outer_img, inner_img):
    # проверяем Х
    # if img2[0][0] > img1[0][0] and img2[0][0] + img2[0][1] < img1[0][0] + img1[0][1]:
        # проверяем У
    #    if img2[1][0] > img1[1][0] and img2[1][0] + img2[1][1] < img1[1][0] + img1[1][1]:
    #        return True
    # return False
    inn_x = inner_img[0][0]
    inn_y = inner_img[1][0]
    inn_w = inner_img[0][1]
    inn_h = inner_img[1][1]
    out_x = outer_img[0][0]
    out_y = outer_img[1][0]
    out_w = outer_img[0][1]
    out_h = outer_img[1][1]
    return (out_x <= inn_x <= inn_x + inn_w <= out_x + out_w) and (out_y <= inn_y <= inn_y + inn_h <= out_y + out_h)



class ImageProcessor:

    def __init__(self, path, out_path, size=34):
        self.path = path
        self.out_path = out_path
        self.letters = None
        self.classes = None
        self.size = size

    def preproc_image(self):
        self.letters, _ = preprocessing.letters_extract(self.path, self.out_path, out_size=self.size)
        for i in range(len(self.letters)):
            for j in range(i+1, len(self.letters)):
                if is_inside(self.letters[i], self.letters[j]):
                    cutted = preprocessing.cut_symbol(self.letters[i], self.letters[j])
                    self.letters[i] = cutted


    def classify_character(self):
        imgs = [i[2] for i in self.letters]
        n = len(imgs)
        imgs = np.concatenate(imgs)
        imgs = np.ones((n, self.size, self.size, 1)) - imgs.reshape(n, self.size, self.size, 1) / 255
        prediction = model.predict(imgs)
        self.classes = np.argmax(prediction, axis=1)

    def pars_expression(self):
        s = symbol_dict[self.classes[0]]
        prev_letter = self.letters[0]
        prev_class = self.classes[0]
        if self.classes[0] not in digits and self.classes[0] not in let:
            s += ' '
        for i in range(1, len(self.letters)):
            cls = self.classes[i]
            smbl = symbol_dict[cls]
            # знак равно иногда распознается как два минуса
            if prev_class in minus_equal and self.classes[i] in minus_equal:
                s = s[:-3]
                s += ' = '
            else:
                # если выше и левее предыдущего, то добавляем '^'
                if is_upper_right(prev_letter, self.letters[i]):
                    s += '^'
                if cls not in digits and cls not in let:
                    s += ' '
                    s += smbl
                    s += ' '
                else:
                    s += smbl
            prev_letter = self.letters[i]
            prev_class = self.classes[i]
        return s

    def run(self):
        self.preproc_image()
        self.classify_character()
        result = self.pars_expression()
        return result


if __name__ == '__main__':
    p = ImageProcessor('photo6.jpg', 'out.jpg')
    print(p.run())
