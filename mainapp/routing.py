from django.urls import re_path,path

from . import consumers
print(consumers.StockConsumer)

websocket_urlpatterns = [
    re_path(r"ws/stock/(?P<room_name>\w+)/$", consumers.StockConsumer.as_asgi()),
]