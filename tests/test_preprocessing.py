from preprocessing.preprocessing import letters_extract, cut_symbol
import cv2
import numpy as np
import pytest


class TestLettersExtract:
    def test_read_exist_file(self, init_exist_img):
        letters, img_res = letters_extract(*init_exist_img)

        assert type(letters) == list

        img_res_test = cv2.imread(init_exist_img[1])

        assert img_res_test is not None

        assert img_res_test.shape == img_res.shape

        assert all([[[np.isclose(img_res_test[i, j, k], img_res[i, j, k]) for i in range(len(img_res_test))]
                     for j in range(len(img_res_test[0]))] for k in range(len(img_res_test[0][0]))])

        for letter in letters:
            assert len(letter) == 3
            assert len(letter[0]) == 2 and len(letter[1]) == 2
            assert letter[2].shape[0] == letter[2].shape[1]

    def test_read_not_exist_file(self, init_not_exist_img):
        with pytest.raises(cv2.error):
            _, _ = letters_extract(*init_not_exist_img)


MOCK_IMG = np.array([[0, 0], [0, 0]])

letters_out = [[(0, 10), (0, 20), MOCK_IMG], [(0, 20), (10, 20), MOCK_IMG], [(5, 10), (0, 50), MOCK_IMG]]
letters_in = [[(1, 2), (3, 5), MOCK_IMG], [(5, 10), (10, 5), MOCK_IMG], [(5, 10), (5, 10), MOCK_IMG]]
letters_in_not_correct = [[(10, 20), (10, 20), MOCK_IMG], [(6, 3), (0, 3), MOCK_IMG], [(6, 100), (6, 100), MOCK_IMG]]

params_correct = [(letters_out[i], letters_in[i])for i in range(len(letters_out))]
params_not_correct = [(letters_out[i], letters_in_not_correct[i])for i in range(len(letters_out))]


class TestCutSymbol:
    @pytest.mark.parametrize('outer,inner', params_correct)
    def test_correct_cut(self, outer, inner):
        assert type(cut_symbol(outer, inner)) == list

    @pytest.mark.parametrize('outer,inner', params_not_correct)
    def test_not_correct_cut(self, outer, inner):
        assert cut_symbol(outer, inner) is None
