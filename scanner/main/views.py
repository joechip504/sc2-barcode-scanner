from django.shortcuts 				import render
from django.shortcuts 				import render_to_response
from django.http 					import HttpResponseRedirect
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

def home(request):
	"""
	"""
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = UploadFile(file = request.FILES['file'])
			new_file.save()
			import os
			print(os.getcwd())
			candidate_dict = API.guess_from_ladder_replay(new_file.file.name)
			from pprint import pprint
			pprint(candidate_dict)
			return render_to_response('main/index_results.html',
           		{'form': form, 'candidate_dict': candidate_dict})

	else:
		form = UploadFileForm()

	return render(
		request,
		'main/index_results.html',
		{'form' : form},
		)
