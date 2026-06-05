import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "compress_web_images.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compress_web_images", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CompressWebImagesTest(unittest.TestCase):
    def test_scaled_dimensions_cap_width_and_preserve_aspect_ratio(self):
        module = load_module()

        self.assertEqual(module.scaled_dimensions(7008, 4672, 2048), (2048, 1366))

    def test_scaled_dimensions_leave_small_images_unchanged(self):
        module = load_module()

        self.assertEqual(module.scaled_dimensions(1600, 1067, 2048), (1600, 1067))

    def test_collect_images_finds_jpg_and_jpeg_recursively(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "nested"
            nested.mkdir()
            (root / "a.jpg").write_bytes(b"jpg")
            (nested / "b.JPEG").write_bytes(b"jpeg")
            (root / "ignore.png").write_bytes(b"png")

            found = [path.relative_to(root) for path in module.collect_images(root)]

        self.assertEqual(found, [Path("a.jpg"), Path("nested/b.JPEG")])


if __name__ == "__main__":
    unittest.main()
