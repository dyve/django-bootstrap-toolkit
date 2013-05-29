from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bootstrap_toolkit.widgets import BootstrapUneditableInput

from .forms import TestForm, TestModelForm, TestInlineForm, WidgetsForm, FormSetInlineForm

from django.views.generic import FormView
from django.views.generic import TemplateView


class TemplateFormView(FormView):
    template_name = 'form_using_template.html'
    form_class = TestForm
    success_url = '.'

    def form_valid(self, form):
        # do something with data here
        return super(TemplateFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TemplateFormView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        if self.request.method == 'POST':
            context['form'] = TestForm(self.request.POST)
        elif self.request.method == 'GET':
            context['form'] = TestForm()
        return context


def demo_form_with_template(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    modelform = TestModelForm()
    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


class DemoFormView(FormView):
    template_name = 'form.html'
    form_class = TestForm
    success_url = '.'

    def form_valid(self, form):
        # do something with data here
        messages.success(self.request, 'I am a success message.')
        return super(DemoFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DemoFormView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        if self.request.method == 'POST':
            context['form'] = TestForm(self.request.POST)
        elif self.request.method == 'GET':
            context['form'] = TestForm()
        #context['form'].fields['title'].widget = BootstrapUneditableInput()
        return context


def demo_form(request):
    messages.success(request, 'I am a success message.')
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    form.fields['title'].widget = BootstrapUneditableInput()
    return render_to_response('form.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


class DemoFormInlineView(FormView):
    template_name = 'form_inline.html'
    form_class = TestForm
    success_url = '.'

    def form_valid(self, form):
        # do something with data
        messages.success(self.request, 'Search results?')
        return super(DemoFormInlineView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DemoFormInlineView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'inline')
        if context['layout'] != 'inline':
            context['layout'] = 'search'
        if self.request.method == 'POST':
            context['form'] = TestInlineForm(self.request.POST)
        elif self.request.method == 'GET':
            context['form'] = TestInlineForm()
        return context


def demo_form_inline(request):
    layout = request.GET.get('layout', '')
    if layout != 'search':
        layout = 'inline'
    form = TestInlineForm()
    return render_to_response('form_inline.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


class DemoFormSetView(FormView):
    template_name = 'formset.html'
    form_class = FormSetInlineForm
    success_url = '.'

    def form_valid(self, form):
        # do something with data here
        messages.success(self.request, 'This is a success message.')
        return super(DemoFormSetView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DemoFormSetView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'inline')
        DemoFormSet = formset_factory(FormSetInlineForm)
        if self.request.method == 'POST':
            context['formset'] = DemoFormSet(self.request.POST,
                                             self.request.FILES)
        elif self.request.method == 'GET':
            context['formset'] = DemoFormSet()
        return context


def demo_formset(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'inline'
    DemoFormSet = formset_factory(FormSetInlineForm)
    if request.method == 'POST':
        formset = DemoFormSet(request.POST, request.FILES)
        formset.is_valid()
    else:
        formset = DemoFormSet()
    return render_to_response('formset.html', RequestContext(request, {
        'formset': formset,
        'layout': layout,
    }))


class DemoTabsView(TemplateView):
    template_name = 'tabs.html'

    def get_context_data(self, **kwargs):
        context = super(DemoTabsView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'tabs')
        context['tabs'] = [
            {
                'link': "#",
                'title': 'Tab 1',
            },
            {
                'link': "#",
                'title': 'Tab 2',
            }
        ]
        return context


def demo_tabs(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'tabs'
    tabs = [
        {
         'link': "#",
         'title': 'Tab 1',
        },
        {
         'link': "#",
         'title': 'Tab 2',
        }
    ]
    return render_to_response('tabs.html', RequestContext(request, {
        'tabs': tabs,
        'layout': layout,
        }))


class DemoPaginationView(TemplateView):
    template_name = 'pagination.html'

    def get_context_data(self, **kwargs):
        context = super(DemoPaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append(u'Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            context['lines'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context['lines'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context['lines'] = paginator.page(paginator.num_pages)
        return context


def demo_pagination(request):
    lines = []
    for i in range(10000):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_lines = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('pagination.html', RequestContext(request, {
        'lines': show_lines,
    }))


def demo_widgets(request):
    layout = request.GET.get('layout', 'vertical')
    form = WidgetsForm()
    return render_to_response('form.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))
