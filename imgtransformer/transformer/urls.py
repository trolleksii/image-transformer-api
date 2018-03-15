from django.urls import re_path

from .views import BWView, IndexView, ResizeView, RotateView

app_name = 'transformer'

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^bw/$', BWView.as_view(), name='bw'),
    re_path(r'^resize/(?P<pct>\d{1,3})/$', ResizeView.as_view(), name='resize'),
    re_path(r'^rotate/(?P<direction>cw|ccw)/(?P<degree>\d{1,3})/$', RotateView.as_view(), name='rotate'),
]
