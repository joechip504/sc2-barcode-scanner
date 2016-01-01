from django.shortcuts 				import render
from django.http 					import HttpResponseRedirect, HttpResponse
from django.template 				import RequestContext
from django.core.urlresolvers 		import reverse
from django.shortcuts 				import render

from .forms  import UploadFileForm
from .models import UploadFile
from .lib_sc2.api import SC2BarcodeScannerAPI

import sys
from .lib_sc2 import tree
sys.modules['tree'] = tree

# Create your views here.

API = SC2BarcodeScannerAPI()

def test(request):
	print('in view "test"') # gets here, doesn't reflect in browser
	return HttpResponse('Hello, world')
	# return render(request, 'main/results.html', {})

def results(request, year, month, day, replay_name):
	print(year, month, day, replay_name)
	return HttpResponse('Hello, world')

	# replay_file_path = 'files' + '/'.join([year, month, day, replay_name])
	# print(replay_file_path)
	# return HttpResponseRedirect(reverse('main:test'))
	# response = API.guess_from_ladder_replay(uploaded_file_name)
	# from pprint import pformat
	# return HttpResponse(pformat(response))

def home(request):
	"""
	"""
	results = {}
	context = {}

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = UploadFile(file = request.FILES['file'])
			new_file.save()
			print(new_file.file.name)
			return HttpResponseRedirect('/results/{}'.format(new_file.file.name))

	else:
		form = UploadFileForm()

	context['form'] = form
	context['results'] = results

	return render(
		request,
		'main/index.html', 
		context, 
		)