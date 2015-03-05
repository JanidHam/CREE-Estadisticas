# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('fechaCreacion', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EncuestaContestada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('respuesta', models.CharField(max_length=255)),
                ('fechaContestacion', models.DateField()),
                ('encuesta', models.ForeignKey(related_name='encuesta', to='estadisticas.Encuesta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpcionesPreguntas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opcion', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pregunta', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='opcionespreguntas',
            name='pregunta',
            field=models.ForeignKey(related_name='preguntaId', to='estadisticas.Pregunta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuestacontestada',
            name='pregunta',
            field=models.ForeignKey(related_name='preguntaEncuesta', to='estadisticas.Pregunta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuesta',
            name='preguntas',
            field=models.ManyToManyField(related_name='preguntas', to='estadisticas.Pregunta'),
            preserve_default=True,
        ),
    ]
