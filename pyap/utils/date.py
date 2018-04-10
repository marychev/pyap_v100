from django.utils import timezone


def is_end_datetime(begin_datetime, end_datetime):
    """
    Определить, входит ли текущая дата в диапазон указанных (начало/конец)
    :param begin_datetime (datetime) - Дата, когда событие должно начаться. (Дата начала)
    :param end_datetime (datetime) - Дата, когда событие должно прерваться. (Дата окончанмия)
    :return boolean - True если указанная дата не больше текущей даты.
    """
    return True if begin_datetime < timezone.now() < end_datetime else False


def get_timezone_begin(end_datetime, days):
    """
    Получить начальную дату. Расчет: Указанная дата минус кол-во дней.
    :param end_datetime: {datetime}: Дата от которыой вычитается кол-во дней. (напр. дата какого либо события)
    :param days: {int}: Кол-во дней
    :return: {datetime}: Дата начала
    """
    return end_datetime - timezone.timedelta(days=days)
