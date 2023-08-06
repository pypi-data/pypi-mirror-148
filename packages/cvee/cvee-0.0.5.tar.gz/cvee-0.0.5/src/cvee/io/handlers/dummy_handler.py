from cvee.io.handlers.base import BaseFileHandler


class DummyHandler(BaseFileHandler):
    def load_from_fileobj(self, file, **kwargs):
        raise RuntimeError("Some packages are missed")

    def save_to_fileobj(self, file, obj, **kwargs):
        raise RuntimeError("Some packages are missed")

    def load_from_path(self, filepath, mode="r", **kwargs):
        raise RuntimeError("Some packages are missed")

    def save_to_path(self, filepath, obj, mode="w", **kwargs):
        raise RuntimeError("Some packages are missed")
