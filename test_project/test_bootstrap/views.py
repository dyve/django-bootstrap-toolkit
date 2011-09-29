from django.shortcuts import render_to_response
from django.template.context import RequestContext
from test_bootstrap.forms import TestForm

def test_form(request):
    form = TestForm()
    return render_to_response('form.html', RequestContext(request, {
        'form': form,
    }))