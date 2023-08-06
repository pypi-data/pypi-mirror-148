import inspect
from django.shortcuts import render

def controllor(func):
    def deal(request):
        context = func(request)
        _package = inspect.getfile(func).split('\\')[-2]
        template_name = _package + '/' + func.__name__ + ".html"
        return render(request, template_name, context)
    return deal