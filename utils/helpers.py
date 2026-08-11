import random

from faker import Faker

fake = Faker()

def random_flag() -> bool:
    """вспомогательная функция для генерации случайного значения флагов"""
    return random.choice([True, False])