class ImageProcessor:

    def __init__(self, path):
        self.path = path

    def preproc_image(self):
        with open(self.path):
            print(f"image preprocessed call for {self.path}")

    def classify_character(self):
        pass

    def pars_expression(self):
        return "x^2+2*x+5"

    def run(self):
        self.preproc_image()
        self.classify_character()
        result = self.pars_expression()
        return result
