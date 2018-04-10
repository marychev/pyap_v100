def get_client_ip(request):
    """
    Получить IP адрес пользователя
    :param request: request object
    :return: string (пр.127.0.0.1)
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip