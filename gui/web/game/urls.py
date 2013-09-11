from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^game$', views.game, name='game'),
    # url(r'^pusher/auth$', views.auth, name='auth'),
    url(r'^continue$', views.continue_game, name='continue'),
)