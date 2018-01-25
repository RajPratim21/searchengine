from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name='reset_password_reset1'),
   	url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),	
	url(r'^crawler$', views.start, name='start'),
	url(r'^config$', views.config, name='config'),
	url(r'^add_config$', views.add_config, name='add_config'),
	url(r'^signup$', views.signup, name='signup'),
        url(r'^get_suggestion$', views.get_suggestion, name='get_suggestion'),
	url(r'^login/$', 'django.contrib.auth.views.login',kwargs={'template_name': 'crawler/login.html'}, ),
	url(r'^home$', views.home, name='home'),
	url(r'^crawler_heavy$', views.crawl_page, name='crawl_page'),
	url(r'^$', views.signup, name='signup'),
	url(r'^logout/$', views.logout_page,name='logout_page'),
	url(r'^config/$', views.configuration,name='config_page'),
	#url(r'^password_reset/$', views.my_password_reset_view,name='password_reset_view'),
	url(r'^newsenv/$', views.newsenv,name='newsenv'),
	#url(r'^newsai/$', views.newsai,name='newsai'),
	url(r'^news/$', views.news,name='newsenergy'),
	url(r'^liked_card$',views.liked_card,name='liked_card'),
	url(r'^add_keyword$',views.add_keyword,name='add_keyword'),
]
