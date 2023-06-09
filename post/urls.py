from django.urls import path
from .views import post_list, post_detail, post_share, \
    contact_us, home_view, post_add, about_us, services_view, faqs_view, laws_view, services
app_name = 'post'

urlpatterns = [
    path('', home_view, name='home'),
    path('about-us/', about_us, name='about'),
    path('services/', services, name='services'),
    path('post/', post_list, name='post_list'),
    path('add_post/', post_add, name='post_add'),
    path('contact/', contact_us, name='contact'),
    path('faqs/', faqs_view, name='faqs'),
    path('laws/<slug:law_slug>/', laws_view, name='laws'),
    path('services/<slug:service_slug>/', services_view, name='service'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('post/<slug:post_slug>/', post_detail, name='post_detail'),
    path('post/<slug:post_slug>/share/', post_share, name='post_share'),
]
