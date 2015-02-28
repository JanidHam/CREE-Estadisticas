from django.shortcuts import render, render_to_response, RequestContext

from .models import Pregunta
# Create your views here.
def home(request):
	return render_to_response('estadisticas/base.html', context_instance=RequestContext(request))

def preguntas(request):
	preguntas = Pregunta.objects.all()
	return render_to_response('estadisticas/preguntas.html', { 'preguntas': preguntas }, context_instance=RequestContext(requests))