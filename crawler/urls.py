from django.conf.urls import url
from . import views

urlpatterns = [
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
	url(r'^newsagri/$', views.newsagri,name='newsagri'),
	url(r'^newsenv/$', views.newsenv,name='newsenv'),
	url(r'^newsai/$', views.newsai,name='newsai'),
	url(r'^news/$', views.news,name='newsenergy'),
	#url(r'^temppage$',views.temppage,name='temppagee'),
	#url(r'^get_themes$',views.get_themes,name='get_themes'),
]
