def sort_by_params(request, object_list):
    """
    Сортировка по GET параметрам запрса
    """
    # новинки
    is_new = request.GET.get('is_new', '')
    if is_new:
        object_list = object_list.order_by(is_new)

    # по цене
    price = request.GET.get('price', '')
    if price:
        reverse = True if request.GET.get('price')[:1] == '-' else False
        object_list = list(object_list)
        object_list.sort(key=lambda o: o.get_price(), reverse=reverse)

    # по тэгам
    tag = request.GET.get('tag', '')
    if tag:
        object_list = list(object_list.filter(tags__in=tag))
    return object_list
