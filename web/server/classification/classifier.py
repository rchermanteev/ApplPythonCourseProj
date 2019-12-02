import pickle

MODEL_PATH = '/home/cloud/ApplPythonCourseProj/web/server/classification/model34.obj'
CLASSES_PATH = '/home/cloud/ApplPythonCourseProj/web/server/classification/classes.txt'
# MODEL_PATH = '/home/anatoly/HDD/Corses/ApplPythonCourseProj/web/server/classification/model.obj'
# CLASSES_PATH = '/home/anatoly/HDD/Corses/ApplPythonCourseProj/web/server/classification/classes.txt'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

symbol_dict = {}
with open(CLASSES_PATH, 'r') as f:
    i = 0
    for line in f:
        symbol_dict[i] = line.strip()
        i += 1
