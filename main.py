import logging
import sys
import os

# ── 1. Настройка логирования ─────────────────────────────
LOG_FORMAT = "%(asctime)s | [%(levelname)-7s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Убедимся, что папка logs существует
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
    ],
)

from validator import validate_registration, mask_password


# ── 2. Основная функция ──────────────────────────────────
def process_request(login: str, password: str, confirm: str):
    """
    Обрабатывает один запрос регистрации и логирует события.
    """
    # В логах пароли маскируем!
    masked_pwd = mask_password(password)
    masked_cnf = mask_password(confirm)
    logging.info(
        f"Запрос регистрации: login='{login}', "
        f"password={masked_pwd}, confirm={masked_cnf}"
    )

    try:
        result, message = validate_registration(login, password, confirm)

        if result:
            logging.info(f"Успешная регистрация: login='{login}'")
        else:
            logging.warning(
                f"Ошибка регистрации: login='{login}', причина='{message}'"
            )

        # Вывод результата в консоль (по заданию)
        print(result)
        print(message)

        return result, message

    except Exception:
        # Если что-то упало — логируем traceback
        logging.exception("Непредвиденная ошибка при обработке запроса")
        print(False)
        print("Внутренняя ошибка сервера")
        return False, "Внутренняя ошибка"


# ── 3. Точка входа ───────────────────────────────────────
def main():
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    # Пример: читаем три строки из stdin (как в задании)
    try:
        login = input("Введите логин: ").strip()
        password = input("Введите пароль: ")
        confirm = input("Подтвердите пароль: ")
    except EOFError:
        logging.error("Не удалось прочитать входные данные")
        return

    process_request(login, password, confirm)
    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()