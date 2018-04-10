# -*- coding: utf-8 -*-
from transliterate import translit


def translaton_field(name):
    """Вернуть английское представление переданной строки"""
    return translit(''.join(
        name.replace(' ', '_')
            .replace('/', '-')
            .replace('№', '')
            .replace('.', '')
            .replace('(', '')
            .replace(')', '')
            .replace('ь', '')
    ), 'ru', reversed=True).lower()

