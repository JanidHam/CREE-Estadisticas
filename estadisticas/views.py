import json
import pdb
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import HttpResponse, Http404
from django.db.models import Count

from .models import Pregunta, OpcionesPreguntas, Encuesta, EncuestaContestada
# Create your views here.
def home(request):
	return render_to_response('estadisticas/base.html', context_instance=RequestContext(request))

def preguntas(request):
	"""
		if request.method == 'POST':
			form = Nombredelformularioquecree(request.POST)
			if form.is_valid():
	"""
	preguntas = Pregunta.objects.all().order_by('-id')
	return render_to_response('estadisticas/preguntas.html', { 'preguntas': preguntas }, context_instance=RequestContext(request))

def encuestas(request):
	encuestas = Encuesta.objects.all().order_by('-id')
	# preguntas = Pregunta.objects.exclude(id__in=Encuesta.objects.get(id=1).preguntas.all())
	# preguntasEncueta = Encuesta.objects.get(id=1).preguntas.all()
	return render_to_response('estadisticas/encuestas.html', { 'encuestas': encuestas }, context_instance=RequestContext(request))

def encuestasPreguntas(request, id):
	# pdb.set_trace()
	encuesta = Encuesta.objects.get(id=id)
	preguntas = Pregunta.objects.exclude(id__in=Encuesta.objects.get(id=id).preguntas.all())
	preguntasEncueta = Encuesta.objects.get(id=id).preguntas.all()
	return render_to_response('estadisticas/encuestaPreguntas.html', { 'preguntas': preguntas, 'preguntasE': preguntasEncueta, 'encuestaH': encuesta }, context_instance=RequestContext(request))

def contestarEncuesta(request, id):
	# pdb.set_trace()
	encuesta = Encuesta.objects.filter(id=id)
	preguntas = Encuesta.objects.get(id=id).preguntas.all()#Pregunta.objects.exclude(id__in=Encuesta.objects.get(id=id).preguntas.all())
	data = list()
	for pregunta in preguntas:
		opcionPregunta = OpcionesPreguntas.objects.filter(pregunta_id=pregunta.id)
		for opcion in opcionPregunta:
			data.append({'id': opcion.id, 'opcion': opcion.opcion, 'idPregunta': pregunta.id})
	return render_to_response('estadisticas/contestarEncuesta.html', { 'preguntas': preguntas, 'data': data, 'encuestaH': encuesta }, context_instance=RequestContext(request))

def estadisticasEncuesta(request, id):
	contestacionEncuesta = EncuestaContestada.objects.filter(encuesta_id=id)
	preguntas = Pregunta.objects.exclude(id__in=Encuesta.objects.get(id=id).preguntas.all())
	preguntasEncueta = Encuesta.objects.get(id=id).preguntas.all()
	return render_to_response('estadisticas/datosEstasdisticos.html', { 'preguntas': preguntas, 'preguntasE': preguntasEncueta }, context_instance=RequestContext(request))

def respuestas(request):
	preguntas = Pregunta.objects.all().order_by('-id')
	opcionesPregunta = OpcionesPreguntas.objects.filter(pregunta_id=1)
	return render_to_response('estadisticas/respuestas.html', { 'preguntas': preguntas, 'opciones': opcionesPregunta }, context_instance=RequestContext(request))

def listarOpcionesPreguntas(request):
	if request.is_ajax():
		if request.POST['pregunta']:
			opcionesPregunta = OpcionesPreguntas.objects.filter(pregunta_id=request.POST['pregunta'])
			data = list()
			for preg in opcionesPregunta:
				data.append({ 'id': preg.pk, 'preg': preg.opcion })

			return HttpResponse(
				json.dumps({ 'respuestas': data }),
				content_type="application/json; charset=uft8")


def guardarPregunta(request):
	if request.is_ajax():
		# pdb.set_trace()
		if request.POST['id']:
			pregunta = Pregunta(pregunta=request.POST['pregunta'])
			pregunta.save()
		else:
			pregunta = Pregunta(pregunta=request.POST['pregunta'])
			pregunta.save()

			preguntas = Pregunta.objects.all().order_by('-id')

			data = list()
			for preg in preguntas:
				data.append({ 'id': preg.pk, 'preg': preg.pregunta })

			return HttpResponse(
				json.dumps({ 'preguntas': data }),
				content_type="application/json; charset=uft8"
				)
	else:
		raise Http404

def guardarEncuesta(request):
	if request.is_ajax():
		if request.POST['id']:
			encuesta = Encuesta(nombre=request.POST['nombre'])
			encuesta.save()
		else:
			encuesta = Encuesta(nombre=request.POST['nombre'])
			encuesta.save()

			encuestas = Encuesta.objects.all().order_by('-id')

			data = list()
			for e in encuestas:
				data.append({'id': e.id, 'nombre': e.nombre})

			return HttpResponse(
				json.dumps({ 'encuestas': data }),
				content_type="application/json; charset=uft8"
				)
	else:
		raise Http404

def guardarPreguntasEncuesta(request, id):
	if request.is_ajax():
		if request.POST['id']:
			encuesta = Encuesta.objects.get(id=request.POST['id'])
			preguntasEncuesta = Encuesta.objects.get(id=request.POST['id']).preguntas.all()
			for p in preguntasEncuesta:
				encuesta.preguntas.remove(p.id)
			tasks = request.POST.getlist('tasks[]')
			# pdb.set_trace()
			for t in tasks:
				encuesta.preguntas.add(t)
			dataPreguntas = list()
			dataPregutnasE = list()
			preguntas = Pregunta.objects.exclude(id__in=Encuesta.objects.get(id=id).preguntas.all())
			preguntasEncueta = Encuesta.objects.get(id=id).preguntas.all()
			for p in preguntas:
				dataPreguntas.append({'id': p.id, 'pregunta': p.pregunta})
			for pE in preguntasEncueta:
				dataPregutnasE.append({'id': pE.id, 'pregunta': pE.pregunta})
			return HttpResponse(
				json.dumps({ 'preguntas': dataPreguntas, 'preguntasE': dataPregutnasE }),
				content_type="application/json; charset=uft8"
				)
	else:
		raise Http404

def guardarContestarEncuesta(request, id):
	if request.is_ajax():
		#pdb.set_trace()
		encuesta = Encuesta.objects.get(id=id)
		tasksId = request.POST.getlist('tasksP[]')
		tasksRespuesta = request.POST.getlist('tasks[]')
		contador = 0
		for t in tasksId:
			pregunta = Pregunta.objects.get(id=t)
			encuestaContestada = EncuestaContestada(encuesta=encuesta, pregunta=pregunta, respuesta=tasksRespuesta[contador], fechaContestacion=request.POST['fecha'])
			encuestaContestada.save()
			++contador
		redirect('encuestas')
		return HttpResponse(
			'succes'
			)
	else:
		raise Http404

def mostrarEstadisticas(request, id):
	if request.is_ajax():
		#pdb.set_trace()
		fechainicio = request.POST['fechaI']
		fechafin = request.POST['fechaF']
		contestacionEncuesta = EncuestaContestada.objects.filter(encuesta_id=id, fechaContestacion__gte=fechainicio, fechaContestacion__lte=fechafin)
		#contestacionEncuesta.values('pregunta').annotate(Count('pregunta'))
		dataPreguntasEncuensta = list()
		#dataPreguntasEncuensta = contestacionEncuesta.values('pregunta').annotate(totalPregunta=Count('pregunta'))
		dataDT = contestacionEncuesta.values('pregunta', 'respuesta').annotate(totalR=Count('respuesta'))
		for p in dataDT:
		 	dataPreguntasEncuensta.append(p)
		#pdb.set_trace()

		return HttpResponse(
			json.dumps({ 'dataTotal': dataPreguntasEncuensta }),
			content_type="application/json; charset=uft8"
			)
	else:
		raise Http404


def guardarOpcionPregunta(request):
	if request.is_ajax():
		# pdb.set_trace()
		if request.POST['id']:
			opcionPregunta = OpcionesPreguntas(opcion=request.POST['opcion'])
			opcionPregunta.save()
		else:
			opcionPregunta = OpcionesPreguntas(opcion=request.POST['opcion'], pregunta_id=request.POST['pregunta'])
			opcionPregunta.save()

			opciones = OpcionesPreguntas.objects.filter(pregunta_id=request.POST['pregunta']).order_by('-id')

			data = list()
			for opc in opciones:
				data.append({ 'id': opc.pk, 'opcion': opc.opcion })

			return HttpResponse(
				json.dumps({ 'opcionesPregunta': data }),
				content_type="application/json; charset=uft8"
				)
	else:
		raise Http404