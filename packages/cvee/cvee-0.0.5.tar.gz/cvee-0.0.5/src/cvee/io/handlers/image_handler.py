import cv2

from cvee.io.handlers.base import BaseFileHandler


# TODO: write test cases
class ImageHandler(BaseFileHandler):
    def load_from_fileobj(self, file, **kwargs):
        raise NotImplementedError()

    def save_to_fileobj(self, file, obj, **kwargs):
        raise NotImplementedError()

    def load_from_path(self, filepath, **kwargs):
        img_bgr = cv2.imread(filepath)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_rgb

    def save_to_path(self, filepath, obj, **kwargs):
        img_rgb = cv2.cvtColor(obj, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filepath, img_rgb)
