from django.urls import re_path


from chat import consumers


websocket_urlpatterns = [


    re_path(r'ws/calls/$', consumers.CallNotificationConsumer.as_asgi()),


    re_path(r'ws/chat/(?P<group_id>\d+)/$', consumers.ChatConsumer.as_asgi()),


]

