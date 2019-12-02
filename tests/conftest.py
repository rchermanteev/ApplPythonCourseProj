import pytest
import os
import numpy as np


@pytest.fixture(scope="function")
def init_exist_img():
    print("\n   > Case setup")
    path_in = "./tests/data/img1.jpg"
    path_out = "./tests/data/out_img.jpg"
    yield (path_in, path_out)
    print("\n   > Case teardown")
    if os.path.exists(path_out):
        os.remove(path_out)


@pytest.fixture(scope="function")
def init_not_exist_img():
    print("\n   > Case setup")
    path_in = "./tests/data/qwerty.jpg"
    path_out = "./tests/data/out_img.jpg"
    yield (path_in, path_out)
    print("\n   > Case teardown")
    if os.path.exists(path_out):
        os.remove(path_out)
