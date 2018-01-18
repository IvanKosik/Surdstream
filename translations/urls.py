from django.urls import path, include

from . import views


app_name = 'translations'
urlpatterns = [
    # ex: /translations/
    path('', views.index, name='index'),
    # ex: /translations/5/
    path('<int:word_id>/', views.detail, name='detail'),
]
