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
	//$('#preguntas').on('click', 'a', cargar_respuestas);
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
    } else 
    alert("esta vacio")
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