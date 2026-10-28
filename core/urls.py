from django.urls import path


from . import views


urlpatterns = [


    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('llms.txt', views.llms_txt, name='llms_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('en/', views.team_portfolio_en, name='team_portfolio_en'),


    path('', views.home, name='home'),


    path('signup/', views.signup, name='signup'),


    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),


    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/view/', views.track_post_view, name='track_post_view'),


    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),


    path('profile/<str:username>/', views.profile, name='profile'),


    path('load-more-posts/', views.load_more_posts, name='load_more_posts'),


    path('ai/', views.funmig_ai_redirect, name='ai_assistant'),
    path('funmigai/', views.funmig_ai_redirect, name='funmigai_sso'),


    path('ai/create-new-chat/', views.funmig_ai_redirect, {'path': 'tools/chat'}, name='create_new_chat'),


    path('ai/delete-session/', views.funmig_ai_redirect, {'path': 'tools/chat'}, name='delete_chat_session'),


    path('ai/archive-session/', views.funmig_ai_redirect, {'path': 'tools/chat'}, name='archive_chat_session'),


    path('ai/session/<int:session_id>/', views.funmig_ai_redirect, {'path': 'tools/chat'}, name='get_session_messages'),


    path('ai/activate-trial/', views.funmig_ai_redirect, {'path': 'plans'}, name='activate_trial'),


    path('pricing/', views.funmig_ai_redirect, {'path': 'plans'}, name='pricing_plans'),


    path('payment/request/', views.funmig_ai_redirect, {'path': 'plans'}, name='request_manual_payment'),


    path('payment/jibit/callback/', views.funmig_ai_redirect, {'path': 'plans'}, name='jibit_payment_callback'),


    path('payment/upload/<int:pk>/', views.funmig_ai_redirect, {'path': 'plans'}, name='upload_receipt'),


    path('admin/grant-access/', views.funmig_ai_redirect, {'path': 'admin'}, name='grant_free_access'),


    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),


    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),


    path('blog/create/', views.create_blog_post, name='create_blog'),
    path('blog/upload-media/', views.upload_blog_media, name='upload_blog_media'),


    path('blog/', views.blog_list, name='blog_list'),


    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),


    path('blog/<slug:slug>/delete/', views.delete_blog_post, name='blog_post_delete'),


    path('blog/<slug:slug>/edit/', views.edit_blog_post, name='blog_edit'),


    path('upload-temp/', views.upload_file_temp, name='upload_file_temp'),


    path('clear-chat/', views.funmig_ai_redirect, {'path': 'tools/chat'}, name='clear_chat'),


    path('check-new-posts/', views.check_new_posts, name='check_new_posts'),


    path('post/create-ajax/', views.create_post_ajax, name='create_post_ajax'),


    path('post/<int:post_id>/save/', views.toggle_save_post, name='toggle_save_post'),


    path('posts/saved/', views.saved_posts, name='saved_posts'),


    path('notifications/', views.notifications_center, name='notifications_center'),


    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),


    path('explore/', views.explore, name='explore'),


    path('trending/', views.trending, name='trending'),


    path('communities/', views.community_list, name='community_list'),


    path('communities/create/', views.community_create, name='community_create'),


    path('communities/<slug:slug>/', views.community_detail, name='community_detail'),


    path('communities/<slug:slug>/join/', views.community_join, name='community_join'),


    path('communities/<slug:slug>/leave/', views.community_leave, name='community_leave'),


    path('hashtag/<str:tag_name>/', views.hashtag_detail, name='hashtag_detail'),


    path('ticket/new/', views.create_ticket, name='create_ticket'),


    path('ticket/list/', views.ticket_list, name='ticket_list'),


    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),


    path('admin/tickets/', views.admin_ticket_list, name='admin_ticket_list'),


    path('admin/ticket/<int:ticket_id>/', views.admin_ticket_detail, name='admin_ticket_detail'),


    path('admin/ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),


    path('ai/save-info/', views.funmig_ai_redirect, {'path': 'account'}, name='save_user_info'),


    path('api/user-tokens/', views.funmig_ai_redirect, {'path': 'account'}, name='get_user_tokens'),


    path('about/', views.about, name='about'),


    path('manage_banner/', views.manage_banner, name='manage_banner'),


    path('get_active_banner/', views.get_active_banner, name='get_active_banner'),


    path('manage_announcements/', views.manage_announcements, name='manage_announcements'),


    path('get_active_announcement/', views.get_active_announcement, name='get_active_announcement'),


    path('follow/<str:username>/', views.follow_user, name='follow_user'),


    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),


    path('followers/<str:username>/', views.followers_list, name='followers_list'),


    path('following/<str:username>/', views.following_list, name='following_list'),


    path('search/', views.search, name='search'),


    path('push/subscribe/', views.subscribe_push, name='subscribe_push'),


    path('push/unsubscribe/', views.unsubscribe_push, name='unsubscribe_push'),


    path('install/', views.install, name='install'),


    path('download/android/', views.download_android_apk, name='download_android_apk'),


    path('admin/payments/', views.funmig_ai_redirect, {'path': 'account'}, name='admin_payment_requests'),


]
