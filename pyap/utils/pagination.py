from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


PER_PAGE = 2


def get_pagination(request, object_list):
    """
    Получить список объектов с пагинацией
    :param request: request object
    :param object_list: список объектов для пагинации
    :return: object list {django.Paginator}
    """
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', PER_PAGE)
    paginator = Paginator(object_list, per_page)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return object_list
