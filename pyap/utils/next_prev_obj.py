def get_next_prev(model, obj):
    try:
        next = model.objects.filter(created__gt=obj.created).order_by('created')[0]
    except IndexError:
        next = None
    try:
        prev = model.objects.filter(created__lt=obj.created).order_by('-created')[0]
    except IndexError:
        prev = None

    return {
        'next': next,
        'prev': prev
    }
