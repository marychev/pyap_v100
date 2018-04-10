import uuslug
import datetime


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    today = datetime.date.today()
    filename = "%s.%s" % (uuslug.slugify(".".join(filename.split('.')[:-1])), ext)
    return 'uploads/%s/%s/%s' % (today.year, today.month, filename)


def create_get_request(key, list_param, list_count):
    """
    Заполнить GET запрос существующими параметрами

    :param key: {string} гет-параметр (Прим: &param=)
    :param list_param: {list} - список занчение для key (Прим: [12, 52, 89] - список IDS)
    :param list_count: {int} - кол-во занчений в списке (Прим: 3)
    :return: {string} - '&param=12&param=52&param=89'
    """
    str_list = [key+'%s' % val for val in list_param]
    val_param = "".join(str_list)
    # пустые значения для GET параметра, нужны для заполнеия пустых значений если запрос длинный(прим. фильтр)
    null_param = str(key * (list_count - len(list_param)))
    return val_param + null_param
