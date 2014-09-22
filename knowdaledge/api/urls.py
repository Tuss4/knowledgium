from django.conf.urls import patterns, url


import coder_api
import content_api

urlpatterns = patterns('', 
    url(
        r'^coder/?$',
        coder_api.CoderDetailView.as_view(),
        name='current_coder',
    ),
    url(
        r'^coder/register/?$',
        coder_api.RegisterCoderView.as_view(),
        name='create_coder',
    ),
    url(
        r'^coder/login/?$',
        coder_api.LoginCoderView.as_view(),
        name='login_coder',
    ),

    # Content URLs
    url(
        r'^content/all/?$',
        content_api.ContentListCreateView.as_view(),
        name='content_list_create',
    ),
    url(
        r'^content/(?P<pk>\d+)/?$',
        content_api.ContentDetailView.as_view(),
        name='content_detail',
    ),
    url(
        r'^category/all/?$',
        content_api.CategoryListCreateView.as_view(),
        name='category_list_create',
    ),
    url(
        r'^category/(?P<pk>\d+)/?$',
        content_api.CategoryDetailView.as_view(),
        name='category_detail',
    ),
)
