from django.urls import path


from . import views


urlpatterns = [


    path('', views.chat_list, name='chat_list'),


    path('create/', views.create_group, name='create_group'),


    path('discover/', views.discover_groups, name='discover_groups'),


    path('discover/join/<int:group_id>/', views.join_public_group, name='join_public_group'),


    path('room/<int:group_id>/', views.chat_room, name='chat_room'),


    path('join/<str:token>/', views.join_group_via_link, name='join_group_via_link'),


    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),


    path('room/<int:group_id>/create-link/', views.create_invite_link, name='create_invite_link'),


    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),


    path('leave/<int:group_id>/', views.leave_group, name='leave_group'),


    path('start-private/', views.start_private_chat, name='start_private_chat'),


    path('notifications/', views.notifications_list, name='notifications_list'),


    path('notifications/clear/', views.clear_notifications, name='clear_notifications'),


    path('get-new-messages/<int:group_id>/<int:last_id>/', views.get_new_messages, name='get_new_messages'),


    path('get-older-messages/<int:group_id>/<int:before_id>/', views.get_older_messages, name='get_older_messages'),


    path('typing-status/<int:group_id>/', views.typing_status, name='typing_status'),


]

