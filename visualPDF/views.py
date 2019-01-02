from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from .forms import PdfForm
from .models import PdfFunction

# Create your views here.
def form(request):
    """this view renders form fields from forms.py and if data is posted creates session and redirects you
    to the form_plot view
    Session.objects.all().delete() delets session when new form is requested"""
    Session.objects.all().delete()
    if request.method == 'POST':
        form = PdfForm(request.POST)
        if form.is_valid():
            request.session['functions'] = form.cleaned_data['functions']
            request.session['compare_with'] = form.cleaned_data['compare_with']
            request.session['Q2'] = form.cleaned_data['Q2']
            request.session['xmin'] = form.cleaned_data['xmin']
            request.session['xmax'] = form.cleaned_data['xmax']
            request.session['points'] = form.cleaned_data['points']
            request.session['ymin'] = form.cleaned_data['ymin']
            request.session['ymax'] = form.cleaned_data['ymax']
            request.session['g'] = form.cleaned_data['g']
            request.session['u'] = form.cleaned_data['u']
            request.session['d'] = form.cleaned_data['d']
            request.session['scale'] = form.cleaned_data['scale']
            request.session['error'] = form.cleaned_data['error']

            return redirect('form_plot')
    else:
        form = PdfForm()
    return render(request, 'visualPDF/form.html', {'form':form})

def form_plot(request):
    """this view collects data from created session and renders picture in browsers new window.
    It is done by creating PdfFunction object and using plot or error plot module from that objects"""
    functions = request.session['functions']
    compare_with = request.session['compare_with']
    Q2 = request.session['Q2']
    xmin = request.session['xmin']
    xmax = request.session['xmax']
    points = request.session['points']
    ymin = request.session['ymin']
    ymax = request.session['ymax']
    g = request.session['g']
    u = request.session['u']
    d = request.session['d']
    scale = request.session['scale']
    error = request.session['error']

    pdf = PdfFunction(functions, compare_with, Q2, xmin, xmax, points, ymin, ymax, g, u, d, scale)
    if error == 'clean':
        picture = pdf.plot()
    else:
        picture = pdf.errorplot()
    return render(request, 'visualPDF/form_plot.html',{'picture':picture})

def form_detail(request):
    """this view is currently used for testing"""
    detail = []
    functions = request.session['functions']
    compare_with = request.session['compare_with']
    Q2 = request.session['Q2']
    xmin = request.session['xmin']
    xmax = request.session['xmax']
    points = request.session['points']
    ymin = request.session['ymin']
    ymax = request.session['ymax']
    g = request.session['g']
    u = request.session['u']
    d = request.session['d']
    detail = [functions, compare_with, Q2, xmin, xmax, points, ymin, ymax, g, u, d]

    return render(request, 'visualPDF/form_detail.html',{'detail':detail})
