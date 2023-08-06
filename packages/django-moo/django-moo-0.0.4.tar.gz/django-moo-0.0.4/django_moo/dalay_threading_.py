from pydoc import resolve
import threading
import time
from urllib import request
from django.urls import get_resolver, path

def delay_conduct():
    time.sleep(1)
    print("[django_moo] the url_pattern is ready...")
    resolve = get_resolver()
    from django.http import HttpRequest
    request = HttpRequest()
    
    from study_record import views as study_record_views
    for m in dir(study_record_views):
        try:
            getattr(study_record_views, m)(request)
        except:
            pass

    from myapp import views as myapp_views
    for m in dir(myapp_views):
        try:
            getattr(myapp_views, m)(request)
        except:
            pass


t = threading.Thread(target=delay_conduct)
t.start()