from django.shortcuts import get_object_or_404, render


def index(request):
    context = {
        'hello': 'hello world',
    }
    return render(request, 'init/index.html', context)

