$(document).on('ready', main_discusiones);

function main_discusiones() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('#preguntas button').on('click', enviar_pregunta);

	$('#respuestas button').on('click', enviar_opcionPregunta);

	$('#encuestas button').on('click', enviar_encuesta);

	$('#encuestasPreguntas button').on('click', enviar_encuestaPreguntas);

	$('#preguntas select').on('change', enviarPreguntaToOpciones);

	$('#enviarFechas button').on('click', enviarFechaParaDatos);

	$('#enviarRespuestas button').on('click', enviarRepuestasEncuesta);
	//$('#preguntas').on('click', 'a', cargar_respuestas);
}

google.load('visualization', '1.1', {'packages':['bar']});
var tasksPreguntas = [];
function enviarRepuestasEncuesta() {
	var tasks = respuestaPorPregunta();
	var idinput    = $('#fecha');

	if(idinput.val() != ''){
		$.post('guardar-encuesta-contestada/', { 'fecha': idinput.val(), 'tasks[]': tasks, 'tasksP[]': tasksPreguntas }, actualizar_encuestas);
	} else {
		alert("esta vacio");
	}
}

function respuestaPorPregunta() {
    var tasks = [];
    tasksPreguntas = [];
    $('input:radio:checked').each(function() {
        tasks.push($(this).val());
        tasksPreguntas.push($(this).attr('name'));
    });

    return tasks;
}

function enviarFechaParaDatos() {
	var fechaInicio = $('#fechaInicio');
	var fechaFin = $('#fechaFin');

	if(fechaFin.val() != '' && fechaInicio.val() != '') {
		$.post('mostrar-estadisticas/', { fechaI: fechaInicio.val(), fechaF: fechaFin.val() }, mostrarDatosEstadisticos);
	} else {
		alert("Seleccione un rango de fechas.");
	}
}

function enviar_pregunta() {
	var input = $('#crear-pregunta input:visible');
	var idinput = $('#id');

	if(input.val() != ''){
		$.post('guardar-pregunta/', { pregunta: input.val(), id: idinput.val() }, actualizar_preguntas);
	}
}

function enviar_encuesta() {
	var input = $('#crear-encuesta input:visible');
	var idinput = $('#id');
	if(input.val() != ''){
		$.post('guardar-encuesta/', { nombre: input.val(), id: idinput.val() }, actualizar_encuestas);
	}
}

function enviar_encuestaPreguntas() {
	var tasks = grab_selected();
	var idinput    = $('#idEncuesta');
	if(idinput.val() != ''){
    $.post('guardar-preguntasEncuesta/', { 'id': idinput.val(), 'tasks[]': tasks }, actualizar_encuestas);
    } else {
    	alert("esta vacio");
	}
	//if(input.val() != ''){
	//	$.post('guardar-encuesta/', { nombre: input.val(), id: idinput.val() }, actualizar_encuestas);
	//}
}

function grab_selected() {
    var tasks = [];
    $('input:checkbox[name=type]:checked').each(function() {
        tasks.push($(this).val());
    });
    return tasks;
}

function enviar_opcionPregunta() {
	var input      = $('#crear-respuesta input:visible');
	var idinput    = $('#id');
	var idPregunta = $('#preguntas select');

	if(input.val() != ''){
		$.post('guardar-respuesta/', { pregunta: idPregunta.val(), id: idinput.val(), opcion: input.val() }, enviarPreguntaToOpciones);
	}
}

function actualizar_preguntas (data) {
	var ul = $('#preguntas ul');

	ul.html('');
	$('#crear-pregunta input:visible').val('');

	$.each(data.preguntas, function(i, elemento){
		$('<li class="well well-sm"><a data-id="' + elemento.id + '">' + elemento.preg + '</a></li>').appendTo(ul);
	});
}

function mostrarDatosEstadisticos (data) {
	var totalP = $('#totalP');
	var div = $('#datosEstadisticos');
	div.html('');
	var idTemp = 0;
	$.each(data.dataTotal, function(i, elemento){
		if (idTemp != elemento.pregunta) {
			idTemp = elemento.pregunta;
			$('<div class="alert alert-info" role="alert"><strong>' + elemento.pregunta + '</strong></div>').appendTo(div);
		}
		$('<div class="row"><div class="col-lg-6"><input class="form-control" type="text" disabled placeholder="Respuesta: ' + elemento.respuesta + ' Total: ' +  elemento.totalR + '"disabled></div></div>').appendTo(div);
	});
	drawChart(data);
}

function drawChart(dataE) {
		//var array = ([['Year', 'Sales', 'Expenses', 'Profit'],['2014', 1000, 400, 200],['2015', 1170, 460, 250]]);
		//alert(array[1]+"");
		//array.push(['2017', 1170, 460, 250]);
		var preguntaId = 0;
		var index = 0;
		var array2 = [];
		var arrayPR = [];
		var arrayRespuestas = ['Preguntas'];
		$.each(dataE.dataTotal, function(i, elemento){
			if( !arrayRespuestas.contains(elemento.respuesta)) {
				arrayRespuestas.push(elemento.respuesta);
			}
		});
		array2.push(arrayRespuestas);
		$.each(dataE.dataTotal, function(i, elemento){
			if (preguntaId != elemento.pregunta) {
				if (index > 0) {
					array2.push(arrayPR);
				}
				index = 1;
				arrayPR = [];
				arrayPR.push('preguntas :' + elemento.pregunta);
				preguntaId = elemento.pregunta;
			}
			for (var i = 1; i < arrayRespuestas.length; i++) {
				if (arrayRespuestas[i] == elemento.respuesta) {
					arrayPR[i] = elemento.totalR
				} else if (arrayPR[i] == null){
					arrayPR[i] = 0;
				}
			}
		});
		array2.push(arrayPR);

		var data = google.visualization.arrayToDataTable(array2);

        var options = {
          chart: {
            title: 'Gráfica de la encuesta',
            //subtitle: 'Sales, Expenses, and Profit: 2014-2017',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

        chart.draw(data, options);
      }

Array.prototype.contains = function(element) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == element) {
            return true;
        }
    }
    return false;
}

function actualizar_encuestas (data) {
	var ul = $('#encuestas ul');

	ul.html('');
	$('#crear-encuesta input:visible').val('');

	$.each(data.encuestas, function(i, elemento){
		$('<li class="well well-sm"><a data-id="' + elemento.id + '" href="encuesta/' + elemento.id + '">' + elemento.nombre + '</a></li>').appendTo(ul);
	});
}

function enviarPreguntaToOpciones() {
	var idP = $('#preguntas select');
	$.post('lista-opciones/', { pregunta: idP.val() }, listarOpciones);
}

function listarOpciones (data) {
	var ul = $('#respuestas ul');

	ul.html('');
	$('#crear-respuesta input:visible').val('');

	$.each(data.respuestas, function(i, elemento){
		$('<li><a data-id="' + elemento.id + '">' + elemento.preg + '</a></li>').appendTo(ul);
	});
}