import cv2
import numpy as np
import collections
import math as m


def cut_symbol(outer_img, inner_img):
    """
    :param outer_img: list[tuple(coordinate_x: int, width: int),
                            tuple(coordinate_y: int, height: int),
                            img: numpy.ndarray]
    :param inner_img: list[tuple(coordinate_x: int, width: int),
                            tuple(coordinate_y: int, height: int),
                            img: numpy.ndarray]
    :return: list[tuple(coordinate_x: int, width: int),
                            tuple(coordinate_y: int, height: int),
                            img: numpy.ndarray] (if the image is processed)
            or

            None (in other situation)
    """
    inn_x = inner_img[0][0]
    inn_y = inner_img[1][0]
    inn_w = inner_img[0][1]
    inn_h = inner_img[1][1]
    out_x = outer_img[0][0]
    out_y = outer_img[1][0]
    out_w = outer_img[0][1]
    out_h = outer_img[1][1]

    if outer_img[2].shape != inner_img[2].shape:
        print("Изображения имеют разную размерность")
        return

    if not ((out_x <= inn_x <= inn_x + inn_w <= out_x + out_w) and (out_y <= inn_y <= inn_y + inn_h <= out_y + out_h)):
        print("Изображение, указанное как внутреннее, внутренним не является")
        return

    size_input_img = outer_img[2].shape[0]
    # Определяем какой параметр при приведении изображения к виду, например,
    # 28х28 (size_input_img) остался без изменения
    reference_size = max(out_w, out_h)

    conversion_factor = size_input_img / reference_size

    # Определим начало координат
    x_0_conv = conversion_factor * out_x + 1
    y_0_conv = conversion_factor * out_y + 1

    # Определим координаты символа, который вырезаем, в координатах изображения, из которого вырезаем
    if out_w > out_h:
        x_conv = m.ceil(conversion_factor * inn_x - x_0_conv)
        y_conv = m.ceil(conversion_factor * inn_y - y_0_conv + (size_input_img - conversion_factor * out_h) / 2)
    else:
        x_conv = m.ceil(conversion_factor * inn_x - x_0_conv + (size_input_img - conversion_factor * out_w) / 2)
        y_conv = m.ceil(conversion_factor * inn_y - y_0_conv)

    # Прибавляю 1, чтобы точно убрать артефакты, которые могут возникнуть при удалении изображения.
    # (Вероятно, не лучшее решение)
    x_fin_conv = m.ceil(x_conv + inn_w * conversion_factor) + 1
    y_fin_conv = m.ceil(y_conv + inn_h * conversion_factor) + 1

    processed_outer_img = outer_img[2]
    # Закрашиваем область, в которой находится символ, который надо вырезать
    processed_outer_img[y_conv:y_fin_conv, x_conv:x_fin_conv] *= 0

    return [outer_img[0], outer_img[1], processed_outer_img]


def letters_extract(path_to_img: str, output_path: str, out_size=28):
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

    # Находим контуры на изображении
    contours, hierarchy = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Выделяем преобладающие по иерархии контуры (это и будут символы)
    _hier = [hierarchy[0][i][3] for i in range(len(contours))]
    _hier_num = max(list(collections.Counter(_hier).items()), key=lambda x: x[1])[0]

    letters = []

    # Формируем изображение для дальнейшей классификации
    for idx, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        size_max = max(w, h)
        if hierarchy[0][idx][3] == _hier_num and size_max > 30:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (70, 0, 0), 1)
            letter_crop = ~img_erode_out[y : y + h, x : x + w]
            letter_square = 0 * np.ones(shape=[size_max, size_max], dtype=np.uint8)
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

    cv2.imwrite(output_path, img)
    return letters, img
