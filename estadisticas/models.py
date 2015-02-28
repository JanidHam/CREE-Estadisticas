from django.db import models

# Create your models here.
class Pregunta(models.Model):
	pregunta = models.CharField(max_length=255)

	def __unicode__(self):
		return self.pregunta

class OpcionesPreguntas(models.Model):
	pregunta  = models.ForeignKey(Pregunta, related_name='preguntaId')
	opcion = models.CharField(max_length=255)

	def __unicode__(self):
		return self.opcion

class Encuesta(models.Model):
	nombre = models.CharField(max_length=255)
	fechaCreacion = models.DateField(auto_now=True)
	preguntas = models.ManyToManyField(Pregunta, related_name='preguntas')

	def __unicode__(self):
		return self.nombre

class EncuestaContestada(models.Model):
	encuesta = models.ForeignKey(Encuesta, related_name='encuesta')
	pregunta = models.ForeignKey(Pregunta, related_name='preguntaEncuesta')
	respuesta = models.CharField(max_length=255)
	fechaContestacion = models.DateField()