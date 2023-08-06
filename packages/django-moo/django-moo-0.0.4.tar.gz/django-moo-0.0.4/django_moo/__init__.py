import django
import os
from django.conf import settings
from django_moo.utils import get_user_all_apps_name

__title__ = 'Django Moo'
__version__ = '0.0.0'
__author__ = 'Xiaomo Lee'

VERSION = __version__
DIR_PATH = __file__.split("__init__.py")[0]

class FileOperator:
    def get_file_data(self, filename):
        f= open(f'{DIR_PATH}/{filename}', 'r', encoding='utf-8')
        content = f.read()
        f.close()
        return content
    
    def write_file_data(self, filename, content):
        f= open(f'{DIR_PATH}/{filename}', 'w', encoding='utf-8')
        f.write(content)
        f.close()

fo = FileOperator() 
content = fo.get_file_data('delay_threading.py')
# fo.write_file_data("dalay_threading_.py", content)

s = '''
    from {} import views as {}_views
    for m in dir({}_views):
        try:
            getattr({}_views, m)(request)
        except:
            pass
''' 

ss = '' 

apps_name = get_user_all_apps_name()
for app_name in apps_name:
    ss += s.format(app_name, app_name, app_name, app_name)

content = content.replace("#{1}#", ss)
# print(content.replace("#{1}#", ss))
fo.write_file_data("dalay_threading_.py", content)

import django_moo.dalay_threading_