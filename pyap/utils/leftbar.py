def get_leftbar(model, obj):
    """
    Формирует Древовидную структуру объекта, всю семью.
    :param model:
    :param obj:
    :return: dict
    """
    root_obj = obj.get_root()
    return {
        'obj': obj,
        'root_obj': root_obj,
        'obj_list': model.objects._mptt_filter(root_obj.get_family()).exclude(is_show=False),
        'all': model.objects.filter(is_show=True),
    }
