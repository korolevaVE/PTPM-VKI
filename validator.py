import re

# Чёрный список логинов
BLACKLIST = {"admin", "root", "user", "test", "guest"}

# Регулярные выражения для логина
PHONE_PATTERN = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
STRING_PATTERN = re.compile(r"^[A-Za-z0-9_]{5,}$")


def validate_login(login: str):
    """Возвращает (True, "") при успехе или (False, "причина")."""
    if not login or not login.strip():
        return False, "Логин пуст"

    # Если похож на телефон
    if login.startswith("+"):
        if not PHONE_PATTERN.match(login):
            return False, "Неверный формат телефона"
        return True, ""

    # Если похож на email (содержит @)
    if "@" in login:
        if not EMAIL_PATTERN.match(login):
            return False, "Неверный формат email"
        return True, ""

    # Иначе — обычная строка
    if not STRING_PATTERN.match(login):
        return False, "Логин: минимум 5 символов, только латиница, цифры и _"

    # Проверка чёрного списка (без учёта регистра)
    if login.lower() in BLACKLIST:
        return False, "Логин находится в чёрном списке"

    return True, ""


def validate_password(password: str):
    """Проверка пароля по всем правилам."""
    if len(password) < 7:
        return False, "Пароль короче 7 символов"

    # Проверка на недопустимые символы (латиница запрещена)
    # Разрешаем: кириллица, цифры, спецсимволы
    allowed_pattern = re.compile(r"^[А-Яа-яЁё0-9!@#$%^&*()_\-+=<>,.?/\\|{}\[\]:;\"'`~]+$")
    if not allowed_pattern.match(password):
        return False, "Пароль содержит недопустимые символы (латиница запрещена)"

    has_upper = any(ch.isupper() for ch in password if ch.isalpha())
    has_lower = any(ch.islower() for ch in password if ch.isalpha())
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(not ch.isalnum() for ch in password)

    if not has_upper:
        return False, "Пароль должен содержать заглавную букву"
    if not has_lower:
        return False, "Пароль должен содержать строчную букву"
    if not has_digit:
        return False, "Пароль должен содержать цифру"
    if not has_special:
        return False, "Пароль должен содержать спецсимвол"

    return True, ""


def mask_password(password: str) -> str:
    """
    Маскирование пароля для логов.
    Одинаковые пароли → одинаковый хэш.
    Разные пароли → разный хэш.
    """
    import hashlib
    return "***" + hashlib.sha256(password.encode("utf-8")).hexdigest()[:8] + "***"


def validate_registration(login: str, password: str, confirm: str):
    """
    Комплексная валидация регистрации.
    Возвращает (result: bool, message: str).
    """
    # Логин
    ok, msg = validate_login(login)
    if not ok:
        return False, msg

    # Пароль
    ok, msg = validate_password(password)
    if not ok:
        return False, msg

    # Совпадение паролей
    if password != confirm:
        return False, "Пароль и подтверждение не совпадают"

    return True, ""