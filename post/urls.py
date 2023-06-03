from django.urls import path
from .views import post_list, post_detail, post_share, \
    contact_us, success_view, home_view, post_add, about_us

app_name = 'post'

urlpatterns = [
    path('', home_view, name='home'),
    path('about-us/', about_us, name='about'),
    path('post/', post_list, name='post_list'),
    path('add_post/', post_add, name='post_add'),
    path('contact/', contact_us, name='contact_us'),

    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('success/', success_view, name='success'),
    path('post/<slug:post_slug>/', post_detail, name='post_detail'),
    path('post/<slug:post_slug>/share/', post_share, name='post_share'),
]
