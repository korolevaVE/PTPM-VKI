import logging
import sys
import os
from geometry import calculate_triangle

def init_logger():
    # Проверяем наличие папки logs, чтобы не было ошибки выполнения
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),          # В консоль
            logging.FileHandler("logs/file_txt.log", encoding="utf-8") # В файл
        ]
    )

def main():
    init_logger()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    print("\n--- Программа расчета треугольника ---")
    side_a = input("Введите длину стороны A: ")
    side_b = input("Введите длину стороны B: ")
    side_c = input("Введите длину стороны C: ")

    logging.debug(f"Получены входные данные: A='{side_a}', B='{side_b}', C='{side_c}'")

    try:
        # Вызываем нашу логику
        res_type, res_coords = calculate_triangle(side_a, side_b, side_c)

        # Проверяем успешность по признакам из методички
        if res_coords[0] == (-1, -1) or res_coords[0] == (-2, -2):
            # Неуспешный запрос
            logging.error(f"Неуспешный запрос. Параметры: A={side_a}, B={side_b}, C={side_c}. Результат: {res_type}, Координаты: {res_coords}")
        else:
            # Успешный запрос
            logging.info(f"Успешный запрос. Параметры: A={side_a}, B={side_b}, C={side_c}. Результат: {res_type}, Координаты: {res_coords}")

        print(f"\nРезультат: {res_type}")
        print(f"Координаты вершин: {res_coords}")

    except Exception as ex:
        # Если произошло непредвиденное падение программы
        logging.error(f"Критический сбой при обработке параметров A={side_a}, B={side_b}, C={side_c}")
        logging.exception("Трассировка стека исключения:")

if __name__ == "__main__":
    main()

