from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Pregunta)
admin.site.register(OpcionesPreguntas)
admin.site.register(Encuesta)
admin.site.register(EncuestaContestada)