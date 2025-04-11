# settings.py
DOUBLE_TROPHIES =False
DOUBLE_TOKENS =False

# Функции для получения значений
def get_double_trophies():
    return DOUBLE_TROPHIES

def get_double_tokens():
    return DOUBLE_TOKENS

def set_double_trophies(value: bool):
    global DOUBLE_TROPHIES
    DOUBLE_TROPHIES = value
    print(f"DOUBLE_TROPHIES установлено на {DOUBLE_TROPHIES}")  # Для отладки

def set_double_tokens(value: bool):
    global DOUBLE_TOKENS
    DOUBLE_TOKENS = value
    print(f"DOUBLE_TOKENS установлено на {DOUBLE_TOKENS}")  # Для отладки