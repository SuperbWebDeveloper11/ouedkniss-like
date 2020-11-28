from django.urls import include, path
# from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_for_html_rendering as html_rendering_views
from .views import views_for_comments as comment_views
from .views import views_for_images as image_views

app_name = 'announce'

urlpatterns = [

    # announces urls 
    path('', html_rendering_views.AnnounceList.as_view(), name='announce_list'),
    path('add/', html_rendering_views.AnnounceCreate.as_view(), name='announce_add'),
    path('<int:pk>/detail/', html_rendering_views.AnnounceDetail.as_view(), name='announce_detail'),
    path('<int:pk>/update/', html_rendering_views.AnnounceUpdate.as_view(), name='announce_update'),
    path('<int:pk>/delete/', html_rendering_views.AnnounceDelete.as_view(), name='announce_delete'),


    ####################### urls for creating comments with jQuery #######################
    # comments urls 
    path('<int:pk>/comments/', comment_views.CommentList.as_view(), name='comment_list'),
    path('<int:pk>/comments/add/', comment_views.CommentCreate.as_view(), name='comment_create'),
    path('<int:pk>/comments/<int:comment_pk>/update/', comment_views.CommentUpdate.as_view(), name='comment_update'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', comment_views.CommentDelete.as_view(), name='comment_delete'),

    ####################### urls for creating images with jQuery #######################
    # images urls 
    path('<int:pk>/images/', image_views.ImageList.as_view(), name='image_list'),
    path('<int:pk>/images/add/', image_views.ImageCreate.as_view(), name='image_create'),
    path('<int:pk>/images/<int:image_pk>/update/', image_views.ImageUpdate.as_view(), name='image_update'),
    path('<int:pk>/images/<int:image_pk>/delete/', image_views.ImageDelete.as_view(), name='image_delete'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)

