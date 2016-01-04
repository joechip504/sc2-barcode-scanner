from django.shortcuts 				import render
from django.shortcuts 				import render_to_response
from django.http 					import HttpResponseRedirect
from django.http 					import HttpResponseRedirect, HttpResponse
from django.template 				import RequestContext
from django.core.urlresolvers 		import reverse
from django.shortcuts 				import render
from django.contrib                 import messages

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

def results(request, replay_id):
	try:
		replay = UploadFile.objects.get(pk = replay_id)
	except UploadFile.DoesNotExist:
		return HttpResponse('Not found')

	response 		= API.guess_from_ladder_replay(replay.file.name)
	summary_info 	= API.get_summary_info(replay.file.name)

	from pprint import pprint
	pprint(summary_info)

	if not response:
		return HttpResponse('Problem processing file')

	context = {
		'response' 		: response,
		'summary_info'  : summary_info,
		'match_title' 	: ' vs. '.join(response.keys())
	}

	return render(request, 'main/results.djhtml', context)

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
			print(new_file.pk)
			return HttpResponseRedirect('/results/{}'.format(new_file.pk))

	else:
		form = UploadFileForm()

	context['form'] = form
	context['results'] = results

	return render(
		request,
		'main/index.html',
		context,
		)
