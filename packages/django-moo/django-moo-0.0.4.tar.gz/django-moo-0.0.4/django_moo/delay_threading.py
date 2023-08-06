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
    #{1}#

t = threading.Thread(target=delay_conduct)
t.start()