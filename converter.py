import os
import argparse
import logging

from PIL import Image

# Дефолтные значения для размеровв
DEFAULT_HORIZONTAL = '250x200'
DEFAULT_VERTICAL = '150x200'

# Исключение, вызываемое при неправильном соотношении размеров
# для горизонтального и вертикального преобразования, полученных из командной строке
class InvalidSizeException(Exception):
    pass


def size_parser(vertical_size, horizontal_size, curr_width, curr_heigth):
    """
    Функция разбирающая входной размер командной строки
    :param vertical_size:  Вертикальный размер из командной строки
    :param horizontal_size:  Горизонтальный размер из командной строки
    :param curr_width:  Ширина изображения
    :param curr_heigth: Высота изображения
    :return: Возвращает ширину, высоту в которые надо преобразовать и тип преобразования
    """

    if curr_width >= curr_heigth:
        new_width, new_height = horizontal_size.split('x')
        if int(new_width) < int(new_height):
            raise InvalidSizeException
        else:
            return int(new_width), int(new_height)

    if curr_width < curr_heigth:
        new_width, new_height = vertical_size.split('x')
        if int(new_width) > int(new_height):
            raise InvalidSizeException
        else:
            return int(new_width), int(new_height)


if __name__ == '__main__':

    # Настройка логирования
    logger = logging.Logger(__name__)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(level=logging.INFO)

    # Настройка аргументов командной строки
    args_parser = argparse.ArgumentParser(description='Image size converter')
    args_parser.add_argument('path', type=str, help='Image path')
    args_parser.add_argument('--horizontal', type=str, help='Horizontal size')
    args_parser.add_argument('--vertical', type=str, help='Vertical size')
    args = args_parser.parse_args()

    # Получение пути и имени изображения для сохранения преобразованного изображения
    image_path = args.path
    image_dir, image_name = os.path.split(image_path)

    try:
        image = Image.open(image_path)

    except FileNotFoundError:
        logger.error("Файл изображения не найден")
        
    else:
        curr_image_width, curr_image_height = image.size
        logger.info("Загружено изображение с шириной {0}px и высотой {1}px".format(curr_image_width, curr_image_height))

        new_width, new_height = size_parser(vertical_size=args.vertical or DEFAULT_VERTICAL,
                                                          horizontal_size=args.horizontal or DEFAULT_HORIZONTAL,
                                                          curr_width=curr_image_width,
                                                          curr_heigth=curr_image_height)
        # Генерация нового имени изображения
        bare_name, ext = image_name.split('.')
        resized_image_name = '.'.join([bare_name, 'thumb', ext])

        # Изменение размера изображения и сохранение
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_image.save(os.path.join(image_dir, resized_image_name))
        logger.info("Изображение сохранено с новыми размерами {0}px".format(resized_image.size))