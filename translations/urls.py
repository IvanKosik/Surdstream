from django.urls import path, include

from . import views


app_name = 'translations'
urlpatterns = [
    # ex: /translations/
    path('', views.index, name='index'),
    # ex: /translations/new/
    path('new/', views.add_translation, name='add_translation'),
    # ex: /translations/5/
    path('<int:word_id>/', views.detail, name='detail'),
    # ex: /translations/9/vote/
    path('<int:video_id>/vote/', views.vote, name='vote'),

    #remove_this
    path('remove_this/', views.remove_this, name='remove_this'),
    path('upload_video/', views.upload_video, name='upload_video'),
]
