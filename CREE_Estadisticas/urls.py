from django.conf.urls import patterns, include, url

from estadisticas import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CREE_Estadisticas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'estadisticas.views.home', name='home'),
    url(r'^guardar-pregunta/$', 'discusion.views.guardar_pregunta', name='guardar_pregunta'),
)
