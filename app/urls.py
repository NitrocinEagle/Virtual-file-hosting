from django.conf.urls import url
from .views import FileBrowser


urlpatterns = [
    url(r'^$', FileBrowser.as_view(), name='file_browser'),
]
