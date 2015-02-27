from django.shortcuts import render, render_to_response, RequestContext

# Create your views here.
def home(request):
	return render_to_response('estadisticas/base.html', context_instance=RequestContext(request))