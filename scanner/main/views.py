from django.shortcuts 				import render
from django.http 					import HttpResponseRedirect
from django.template 				import RequestContext
from django.core.urlresolvers 		import reverse
from django.shortcuts 				import render_to_response

from .forms 	import UploadFileForm
from .models import UploadFile

# Create your views here.

def home(request):
	"""
	"""
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = UploadFile(file = request.FILES['file'])
			new_file.save()
			return HttpResponseRedirect(reverse('main:home'))

	else:
		form = UploadFileForm()

	return render_to_response(
		'main/index_results.html', 
		{'form' : form}, 
		context_instance = RequestContext(request)
		)