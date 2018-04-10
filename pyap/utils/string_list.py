"""
Преобразование со строковыми списками
"""


def transform_to_int_list(strlist):
    """
    Преобразовать строковый список в числовой
    :param strlist {list} - ['1', '2', 'n', ...]
    :return intlist {list} - [1, 2, n, ...]
    """
    intlist = []
    for s in strlist:
        if s != '':
            intlist.append(int(s))
    return intlist


# class GeneratorFoo(object):
#     """
#     Сгенерировать функцию  из строковой переменной.
#     Имя перменной(стр) станет именем функции И аргументом(доступным внуири ф-ции).
#     """
#     def __init__(self, *args):
#         def make_getter(arg):
#             def func():
#                 print('func: ', func, 'arg: ', arg)
#             return func
#
#         for arg in args:
#             setattr(self, 'get_' + arg, make_getter(arg))