from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^crawler$', views.start, name='start'),
	url(r'^signup$', views.signup, name='signup'),
	url(r'^login/$', 'django.contrib.auth.views.login',kwargs={'template_name': 'crawler/login.html'}, ),
	url(r'^home$', views.home, name='home'),
	url(r'^crawler_heavy$', views.crawl_page, name='crawl_page'),
	url(r'^$', views.signup, name='signup'),
	url(r'^logout/$', views.logout_page,name='logout_page'),
	url(r'^config/$', views.configuration,name='config_page'),
	url(r'^news/$', views.news,name='news'),
	url(r'^newcrawlerwired$', views.newcrawlwired, name='newcrawl'),
	url(r'^newcrawlermash$', views.newcrawlmash, name='newcrawl'),
	url(r'^newcrawlertc$', views.newcrawltc, name='newcrawl'),
	url(r'^newcrawlerso$', views.newcrawlso, name='newcrawl'),
	url(r'^newcrawlerse$', views.newcrawlse, name='newcrawl'),
	url(r'^newcrawlerQ$', views.newcrawlQ, name='newcrawl'),
	url(r'^newcrawlerwsj$', views.newcrawlwsj, name='newcrawl'),
	url(r'^newcrawlerespn$', views.newcrawlespn, name='newcrawl'),
	url(r'^newcrawlertv$', views.newcrawltv, name='newcrawl'),
	url(r'^newcrawlerabc$', views.newcrawlabc, name='newcrawl'),
	url(r'^newcrawlerign$', views.newcrawlign, name='newcrawl'),
	url(r'^newcrawlerhindu$', views.newcrawlhindu, name='newcrawl'),
	url(r'^newcrawlerppl$', views.newcrawlppl, name='newcrawl'),
	
	url(r'^newcrawlerwikiagri$', views.newwikicrawlagri, name='newcrawl'),
	url(r'^newcrawlerwikitech$', views.newwikicrawltech, name='newcrawl'),
	url(r'^newcrawlerwikisports$', views.newwikicrawlsports, name='newcrawl'),
	url(r'^newcrawlerwikibiz$', views.newwikicrawlbiz, name='newcrawl'),
	url(r'^newcrawlerwikippl$', views.newwikicrawlppl, name='newcrawl'),
	url(r'^newcrawlerwikienergy$', views.newwikicrawlenergy, name='newcrawl'),
	url(r'^newcrawlerwikiwm$', views.newwikicrawlwm, name='newcrawl'),
	url(r'^newcrawlerwiki$', views.newwikicrawl, name='newcrawl'),
	
]
