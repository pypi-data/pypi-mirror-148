import inspect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models.query import QuerySet
from django_moo.utils import QToDict
from django.db.models import Model
from django.urls import path, re_path
from django.urls import get_resolver

def controllor(func):
    def deal(request, *args, **kwargs):
        context = func(request, *args, **kwargs)
        _package = inspect.getfile(func).split('\\')[-2]
        template_name = _package + '/' + func.__name__ + ".html"
        if isinstance(context, dict):
            return render(request, template_name, context)
        if isinstance(context, QuerySet):
            return render(request, template_name, {"ones":context})
        if isinstance(context, Model):
            return render(request, template_name, {"one": context})
        else:
            return HttpResponse(str(context))
    return deal

def rest_controllor(func):
    def deal(request):
        queryset = func(request)
        if queryset is None:
            return JsonResponse([], safe=False)
        elif isinstance(queryset, dict):
            return JsonResponse(queryset)
        elif isinstance(queryset, Model) or isinstance(queryset, QuerySet):
            data = QToDict(queryset, request).get_result()
            if type(data) == list:
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse(data)
        else:
            return JsonResponse(queryset, safe=False)
    return deal

def url_pattern(url_path, regex=False, **kwargs):
    def middle(func):
        def inner(request, *args, **kwargs):
            name = kwargs.get('name') or func.__name__
            if regex:
                p = re_path(url_path, func, name=name)
            else:
                p = path(url_path, func, name=name)
            urlpatterns = get_resolver().url_patterns
            if p not in urlpatterns:
                urlpatterns.append(p)
        return inner
    return middle