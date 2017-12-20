import unittest

from converter import size_parser
from converter import InvalidSizeException


class TestSizeParser(unittest.TestCase):

    def test_horizontal_size(self):
        """
        Проверка получения размеров и определение режима для горизонтальных изображений
        :return:
        """
        self.assertEqual(size_parser('150x200', '250x200', 1992, 1028), (250, 200))

    def test_vertical_size(self):
        """
        Проверка получения размеров и определение режима для вертикальных изображений
        :return:
        """
        self.assertEqual(size_parser('150x200', '250x200', 1028, 1992), (150,200))

    def test_exception(self):
        """
        Проверка на вызов исключения при неправильно введенных параметрах
        :return:
        """
        self.assertRaises(InvalidSizeException, size_parser, '450x200', '250x200', 1028, 1092)