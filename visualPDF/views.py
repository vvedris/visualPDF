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
            functions = form.cleaned_data['functions']
            compare_with = form.cleaned_data['compare_with']
            Q2 = form.cleaned_data['Q2']
            xmin = form.cleaned_data['xmin']
            xmax = form.cleaned_data['xmax']
            points = form.cleaned_data['points']
            ymin = form.cleaned_data['ymin']
            ymax = form.cleaned_data['ymax']
            g = form.cleaned_data['g']
            u = form.cleaned_data['u']
            d = form.cleaned_data['d']
            scale = form.cleaned_data['scale']
            error = form.cleaned_data['error']

            pdf = PdfFunction(functions, compare_with, Q2, xmin, xmax, points, ymin, ymax, g, u, d, scale)

            if error == 'clean':
                picture = pdf.plot()
            else:
                picture = pdf.errorplot()

            return render(request, 'visualPDF/form.html', {'form':form, 'picture':picture})
    else:
        form = PdfForm()

    return render(request, 'visualPDF/form.html', {'form':form})
