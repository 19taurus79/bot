import re


def remove_words_until_uppercase(s):
    # Регулярний вираз для пошуку першого слова, яке починається з великої літери
    match = re.search(r"\b[A-ZА-ЯІЇЄ][a-zа-яіїє]*.*", s)
    if match:
        # Повертаємо рядок, починаючи з першого слова з великої літери
        return s[match.start() :]
    return s
