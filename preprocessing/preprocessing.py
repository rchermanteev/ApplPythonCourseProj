import cv2
import numpy as np
import collections


def letters_extract(path_to_img: str, out_size=28):
    """
    :param path_to_img: str
    :param out_size: int
    :return: letters: list[tuple(coordinate_x: int, width: int),
                            tuple(coordinate_y: int, height: int),
                            img: numpy.ndarray]
    """

    img = cv2.imread(path_to_img)
    gray = cv2.cvtColor(
        img, cv2.COLOR_BGR2GRAY
    )  # Переводим изображение в оттенки серого
    blur = cv2.medianBlur(gray, 3)  # Добавляем размытие, чтобы избавится от шума

    _, thresh = cv2.threshold(
        blur, 120, 255, cv2.THRESH_BINARY
    )  # Бинаризуем изображение по порогу

    # Размазываем символы на изображении, чтобы увеличить точность обнаружения
    img_erode = cv2.erode(thresh, np.ones((15, 15), np.uint8), iterations=1)
    img_erode_out = cv2.erode(thresh, np.ones((10, 10), np.uint8), iterations=1)

    contours, hierarchy = cv2.findContours(  # Находим контуры на изображении
        img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    # Выделяем преобладающие по иерархии контуры (это и будут символы)
    _hier = [hierarchy[0][i][3] for i in range(len(contours))]
    _hier_num = max(list(collections.Counter(_hier).items()), key=lambda x: x[1])[0]

    letters = []

    # Формируем изображение для дальнейшей классификации
    for idx, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        size_max = max(w, h)
        if hierarchy[0][idx][3] == _hier_num and size_max > 30:
            cv2.rectangle(img, (x, y), (x + w, y + h), (70, 0, 0), 1)
            letter_crop = ~img_erode_out[y : y + h, x : x + w]
            letter_square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)
            if w > h:
                y_pos = size_max // 2 - h // 2
                letter_square[y_pos : y_pos + h, 0:w] = letter_crop
            elif w < h:
                x_pos = size_max // 2 - w // 2
                letter_square[0:h, x_pos : x_pos + w] = letter_crop
            else:
                letter_square = letter_crop

            letters.append(
                (
                    (x, w),
                    (y, h),
                    cv2.resize(
                        letter_square,
                        (out_size, out_size),
                        interpolation=cv2.INTER_AREA,
                    ),
                )
            )

    # Сортируем символы по координатам y и x
    letters.sort(key=lambda y: y[1][0], reverse=False)
    letters.sort(key=lambda x: x[0][0], reverse=False)

    return letters
