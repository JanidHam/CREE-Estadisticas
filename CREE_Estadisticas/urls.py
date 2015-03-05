from django.conf.urls import patterns, include, url

from estadisticas import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CREE_Estadisticas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^home/', 'estadisticas.views.home', name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^preguntas/$', views.preguntas, name='preguntas'),
    url(r'^respuestas/$', views.respuestas, name='respuestas'),
    url(r'^encuestas/$', views.encuestas, name='encuestas'),
    url(r'^encuestas/encuesta/(?P<id>\d+)/$', 'estadisticas.views.encuestasPreguntas', name='encuestaPreguntas'),
    url(r'^encuestas/encuesta/(?P<id>\d+)/guardar-preguntasEncuesta/$', 'estadisticas.views.guardarPreguntasEncuesta', name='guardarPreguntasEncuesta'),
    url(r'^encuestas/contestar/(?P<id>\d+)/$', 'estadisticas.views.contestarEncuesta', name='contestarEncuesta'),
    url(r'^encuestas/encuesta/contestar/(?P<id>\d+)/guardar-contestarEncuesta/$', 'estadisticas.views.guardarContestarEncuesta', name='guardarContestarEncuesta'),
    url(r'^encuestas/guardar-encuesta/$', views.guardarEncuesta, name='guardarEncuesta'),
    url(r'^respuestas/lista-opciones/$', views.listarOpcionesPreguntas, name='lista_opciones'),
    url(r'^respuestas/guardar-respuesta/$', views.guardarOpcionPregunta, name='lista_opciones'),
    url(r'^preguntas/guardar-pregunta/$', 'estadisticas.views.guardarPregunta', name='guardar_pregunta'),
)
